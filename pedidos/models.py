from django.db import models
from profiles.models import ClientProfile, SuplierProfile
from catalogo.models import Produto  # ou Product, depende do nome do modelo

class Encomenda(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='encomendas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Encomenda #{self.id} - {self.cliente.user.username}"


class EncomendaItem(models.Model):
    encomenda = models.ForeignKey(Encomenda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fornecedor = models.ForeignKey(SuplierProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantidade} x {self.produto.name} (Encomenda #{self.encomenda.id})"

    def subtotal(self):
        return self.quantidade * self.preco_unitario
