from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReembolsoForm, ComprovanteForm
from .models import Reembolso

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

def listar_reembolsos(request):
    reembolsos = Reembolso.objects.all()
    return render(request, 'reembolsos/listar_reembolsos.html', {'reembolsos': reembolsos})

def concluir_reembolso(request, reembolso_id):
    reembolso = get_object_or_404(Reembolso, id=reembolso_id)

    if request.method == 'POST':
        form = ComprovanteForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva o comprovante no reembolso
            reembolso.comprovante_reembolso = request.FILES['comprovante_reembolso']
            reembolso.concluido = True  # Marca como concluído
            reembolso.save()  # Salva as alterações

            # Enviar e-mail aqui

            return redirect('listar_reembolsos_concluidos')  # Redireciona para a lista de reembolsos concluídos
    else:
        form = ComprovanteForm()

    return render(request, 'concluir_reembolso.html', {'reembolso': reembolso, 'form': form})

def listar_reembolsos_concluidos(request):
    reembolsos_concluidos = Reembolso.objects.filter(concluido=True)  # Filtra reembolsos com status 'Concluído'
    return render(request, 'reembolsos/listar_reembolsos_concluidos.html', {'reembolsos_concluidos': reembolsos_concluidos})