from django.db import models

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Pago'),
        ('SHIPPED', 'Enviado'),
        ('DELIVERED', 'Entregue'),
        ('CANCELED', 'Cancelado'),
    ]

    client = models.ForeignKey(
        'profiles.ClientProfile',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    create_at = models.DateTimeField("Data do Pedido", auto_now_add=True)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    total = models.DecimalField("Total", max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id} - {self.client.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'catalogo.Product',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField("Quantidade")
    unity_price = models.DecimalField("Preço Unitário", max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(
        'profiles.SuplierProfile',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"
