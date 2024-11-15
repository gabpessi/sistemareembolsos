from django.db import models
from django.contrib.auth.models import User

class Reembolso(models.Model):
    CATEGORIAS_REEMBOLSO = [
        ('Simulado', 'Simulado'),
        ('Aulão', 'Aulão'),
        ('Eventos', 'Eventos'),
        ('Brindes', 'Brindes'),
        ('Documentos', 'Documentos'),
        ('Domínio do site', 'Domínio do site'),
        ('Google Meets', 'Google Meets'),
        ('Processo Seletivo de Alunos', 'Processo Seletivo de Alunos'),
        ('Processo Seletivo de Organizadores/Docentes', 'Processo Seletivo de Organizadores/Docentes'),
        ('Outro', 'Outro'),
    ]

    CATEGORIAS_DEPARTAMENTO = [
        ('Hogwarts', 'Hogwarts'),
        ('Embaixada', 'Embaixada'),
        ('Times Square- Captação', 'Times Square- Captação'),
        ('Ministério', 'Ministério'),
        ('Times Square- Mkt', 'Times Square- Mkt'),
        ('Vale do Silício', 'Vale do Silício'),
        ('Presidência', 'Presidência'),
        ('Processo Seletivo', 'Processo Seletivo'),
    ]
    
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    departamento = models.CharField(max_length=50, choices=CATEGORIAS_DEPARTAMENTO)
    descricao_produto = models.TextField("Descreva o produto/serviço")
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_REEMBOLSO)
    valor_nf = models.DecimalField("Valor da Nota Fiscal (apenas números)", max_digits=10, decimal_places=2)
    data_pagamento = models.DateField("Data do Pagamento")    
    comprovante_pedido = models.FileField(upload_to='comprovantes/pedido/', null=True, blank=True)  # Comprovante do solicitante
    comprovante_reembolso = models.FileField(upload_to='comprovantes/reembolso/', null=True, blank=True)  # Comprovante do reembolso
    concluido = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nome} - {self.categoria} - R$ {self.valor_nf}"