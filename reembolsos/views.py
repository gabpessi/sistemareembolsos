from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReembolsoForm, ComprovanteReembolsoForm
from .models import Reembolso
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Q
from django.db.models import Sum
from datetime import datetime

def is_admin(user):
    return user.is_superuser

@login_required
def solicitar_reembolso(request):
    if request.method == 'POST':
        form = ReembolsoForm(request.POST, request.FILES)
        if form.is_valid():
            reembolso = form.save(commit=False)
            reembolso.solicitante = request.user  # Associa o solicitante ao usuário logado
            reembolso.save()

            # Enviar e-mail para confirmar o recebimento do pedido de reembolso
            assunto = 'Pedido de Reembolso Recebido'
            mensagem = f'Olá {reembolso.nome},\n\nSeu pedido de reembolso foi recebido e está sendo processado. Aguarde até que ele seja concluído.\n\nAtenciosamente,\nEquipe do Einstein'
            email_remetente = settings.DEFAULT_FROM_EMAIL
            email_destinatario = [reembolso.email]  # O e-mail do solicitante

            # Cria e envia o e-mail
            email = EmailMessage(
                assunto,
                mensagem,
                email_remetente,
                email_destinatario
            )
            email.send()

            return redirect('solicitante_dashboard')  # Redireciona para o dashboard do solicitante
    else:
        form = ReembolsoForm()

    return render(request, 'reembolsos/solicitar_reembolso.html', {'form': form})


@user_passes_test(is_admin)
@login_required
def listar_reembolsos(request):
    reembolsos = Reembolso.objects.filter(concluido=False)
     # Obtendo os parâmetros de filtro da URL
    departamento = request.GET.get('departamento')
    categoria = request.GET.get('categoria')
    busca_nome = request.GET.get('busca_nome')
    ordem_data = request.GET.get('ordem_data')

    # Aplicando os filtros
    if departamento:
        reembolsos = reembolsos.filter(departamento=departamento)
    
    if categoria:
        reembolsos = reembolsos.filter(categoria=categoria)
    
    if busca_nome:
        reembolsos = reembolsos.filter(
            Q(nome__icontains=busca_nome) | Q(descricao_produto__icontains=busca_nome)
        )
    
   
    if ordem_data == 'maisRecente':
        reembolsos = reembolsos.order_by('-data_pagamento')
    elif ordem_data == 'maisAntigo':
        reembolsos = reembolsos.order_by('data_pagamento')

    
    
    return render(request, 'reembolsos/listar_reembolsos.html', {'reembolsos': reembolsos})

@user_passes_test(is_admin)
@login_required
def concluir_reembolso(request, reembolso_id):
    reembolso = get_object_or_404(Reembolso, id=reembolso_id)

    if request.method == 'POST':
        form = ComprovanteReembolsoForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva o comprovante no reembolso
            reembolso.comprovante_reembolso = request.FILES['comprovante_reembolso']
            reembolso.concluido = True  
            reembolso.save()  # Salva as alterações

             # Enviar e-mail para o solicitante
            assunto = 'Reembolso Concluído'
            mensagem = f'Olá {reembolso.nome},\n\nSeu pedido de reembolso foi processado e concluído com sucesso. Veja o comprovante em anexo.\n\nAtenciosamente,\nEquipe do Einstein'
            email_remetente = settings.DEFAULT_FROM_EMAIL
            email_destinatario = [reembolso.email]  

            # Cria o e-mail
            email = EmailMessage(
                assunto,
                mensagem,
                email_remetente,
                email_destinatario
            )

            # Verifica se há um comprovante anexado e envia o e-mail com o anexo
            if reembolso.comprovante_reembolso:
                caminho_comprovante = reembolso.comprovante_reembolso.path
                email.attach_file(caminho_comprovante)

            # Envia o e-mail
            email.send()



            return redirect('listar_reembolsos_concluidos')  
    else:
        form = ComprovanteReembolsoForm()

    return render(request, 'reembolsos/concluir_reembolso.html', {'reembolso': reembolso, 'form': form})

@user_passes_test(is_admin)
@login_required
def listar_reembolsos_concluidos(request):
    
    reembolsos_concluidos = Reembolso.objects.filter(concluido=True)

    
    departamento = request.GET.get('departamento')
    categoria = request.GET.get('categoria')
    busca_nome = request.GET.get('busca_nome')
    ordem_data = request.GET.get('ordem_data')

    if departamento:
        reembolsos_concluidos = reembolsos_concluidos.filter(departamento=departamento)
    
    if categoria:
        reembolsos_concluidos = reembolsos_concluidos.filter(categoria=categoria)
    
    if busca_nome:
        reembolsos_concluidos = reembolsos_concluidos.filter(
            Q(nome__icontains=busca_nome) | Q(descricao_produto__icontains=busca_nome)
        )
    
    # Ordenando por data de pagamento
    if ordem_data == 'maisRecente':
        reembolsos_concluidos = reembolsos_concluidos.order_by('-data_pagamento')
    elif ordem_data == 'maisAntigo':
        reembolsos_concluidos = reembolsos_concluidos.order_by('data_pagamento')

    
    return render(request, 'reembolsos/listar_reembolsos_concluidos.html', 
                  {'reembolsos_concluidos': reembolsos_concluidos})



@user_passes_test(is_admin)
@login_required
def remover_reembolso(request, reembolso_id):
    reembolso = get_object_or_404(Reembolso, id=reembolso_id)
    
    reembolso.delete()  
    return redirect('listar_reembolsos')  

@user_passes_test(is_admin)
@login_required
def remover_reembolso_concluido(request, reembolso_id):
    reembolso = get_object_or_404(Reembolso, id=reembolso_id)
    
    reembolso.delete()
    return redirect('listar_reembolsos_concluidos') 
    

@user_passes_test(is_admin)
@login_required
def editar_reembolso(request, reembolso_id):
    reembolso = get_object_or_404(Reembolso, id=reembolso_id)  # Busca o reembolso pelo ID
    
    if request.method == 'POST':
        form = ReembolsoForm(request.POST, request.FILES, instance=reembolso)  # Preenche o form com os dados enviados
        if form.is_valid():
            form.save()  # Salva as mudanças
            return redirect('listar_reembolsos')  # Redireciona de volta para a lista de reembolsos
    else:
        form = ReembolsoForm(instance=reembolso)  # Preenche o form com os dados atuais
    
    return render(request, 'reembolsos/editar_reembolso.html', {'form': form, 'reembolso': reembolso})


@user_passes_test(is_admin)
@login_required
def relatorio_reembolsos(request):
    # Filtra apenas reembolsos concluídos
    reembolsos_concluidos = Reembolso.objects.filter(concluido=True)

    # Inicializa o dicionário do relatório mensal
    relatorio_mensal = {}

   
    for reembolso in reembolsos_concluidos:
        
        mes_ano = reembolso.data_pagamento.strftime('%m/%Y')
        
        # Se o mês/ano já está no dicionário, soma o valor; caso contrário, cria uma nova entrada
        if mes_ano in relatorio_mensal:
            relatorio_mensal[mes_ano] += reembolso.valor_nf
        else:
            relatorio_mensal[mes_ano] = reembolso.valor_nf

    # Ordena o relatório do mais recente para o mais antigo
    relatorio_mensal = dict(sorted(relatorio_mensal.items(), key=lambda x: datetime.strptime(x[0], '%m/%Y'), reverse=True))

    # Calcula a somatória total dos reembolsos concluídos
    soma_total = reembolsos_concluidos.aggregate(Sum('valor_nf'))['valor_nf__sum'] or 0

    # Passa os dados para o template
    context = {
        'relatorio_mensal': relatorio_mensal,
        'soma_total': soma_total,
    }
    return render(request, 'reembolsos/relatorio_reembolsos.html', context)
