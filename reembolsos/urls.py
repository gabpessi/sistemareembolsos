from django.urls import path
from . import views

urlpatterns = [
    path('solicitar/', views.solicitar_reembolso, name='solicitar_reembolso'),
    path('listar/', views.listar_reembolsos, name='listar_reembolsos'),
    path('concluir/<int:reembolso_id>/', views.concluir_reembolso, name='concluir_reembolso'),    
    path('listar/concluidos/', views.listar_reembolsos_concluidos, name='listar_reembolsos_concluidos'),
    path('remover/<int:reembolso_id>/', views.remover_reembolso, name='remover_reembolso'),
    path('remover/concluido/<int:reembolso_id>/', views.remover_reembolso_concluido, name='remover_reembolso_concluido'),
    path('editar/<int:reembolso_id>/', views.editar_reembolso, name='editar_reembolso'),
]  

