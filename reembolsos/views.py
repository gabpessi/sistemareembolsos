from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReembolsoForm, ComprovanteReembolsoForm
from .models import Reembolso
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage
from django.conf import settings

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
            return redirect('solicitante_dashboard')
    else:
        form = ReembolsoForm()
    return render(request, 'reembolsos/solicitar_reembolso.html', {'form': form})

@user_passes_test(is_admin)
@login_required
def listar_reembolsos(request):
    reembolsos = Reembolso.objects.filter(concluido=False)
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
            reembolso.concluido = True  # Marca como concluído
            reembolso.save()  # Salva as alterações

             # Enviar e-mail para o solicitante
            assunto = 'Reembolso Concluído'
            mensagem = f'Olá {reembolso.nome},\n\nSeu pedido de reembolso foi processado e concluído com sucesso. Veja o comprovante em anexo.\n\nAtenciosamente,\nEquipe do Einstein'
            email_remetente = settings.DEFAULT_FROM_EMAIL
            email_destinatario = [reembolso.email]  # O e-mail do solicitante

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



            return redirect('listar_reembolsos_concluidos')  # Redireciona para a lista de reembolsos concluídos
    else:
        form = ComprovanteReembolsoForm()

    return render(request, 'reembolsos/concluir_reembolso.html', {'reembolso': reembolso, 'form': form})

@user_passes_test(is_admin)
@login_required
def listar_reembolsos_concluidos(request):
    reembolsos_concluidos = Reembolso.objects.filter(concluido=True)  # Filtra reembolsos com status 'Concluído'
    return render(request, 'reembolsos/listar_reembolsos_concluidos.html', 
    {'reembolsos_concluidos': reembolsos_concluidos})

@user_passes_test(is_admin)
@login_required
def remover_reembolso(request, reembolso_id):
    reembolso = get_object_or_404(Reembolso, id=reembolso_id)
    
    reembolso.delete()  # Remove o reembolso do banco de dados
    return redirect('listar_reembolsos')  # Redireciona para a lista de reembolsos

@user_passes_test(is_admin)
@login_required
def remover_reembolso_concluido(request, reembolso_id):
    reembolso = get_object_or_404(Reembolso, id=reembolso_id)
    
    reembolso.delete()  # Remove o reembolso do banco de dados
    return redirect('listar_reembolsos_concluidos')  # Redireciona para a lista de reembolsos
    

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