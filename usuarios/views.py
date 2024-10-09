from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def solicitante_dashboard(request):
    return render(request, 'usuarios/solicitante_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'usuarios/admin_dashboard.html')

