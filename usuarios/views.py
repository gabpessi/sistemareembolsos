from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser


@login_required
def redirecionar_usuario(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('solicitar_reembolso')
    

@login_required
def solicitante_dashboard(request):
    return render(request, 'usuarios/solicitante_dashboard.html')


@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):
    return render(request, 'usuarios/admin_dashboard.html')

@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard') 
    else:
        return redirect('solicitar_reembolso')  