from django.db import models
from profiles.models import SuplierProfile  # ou FornecedorProfile, depende de como nomeaste

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    UNIDADE_VENDA_CHOICES = [
        ('m²', 'Metro Quadrado'),
        ('saco', 'Saco'),
        ('m³', 'Metro Cúbico'),
        ('un', 'Unidade'),
    ]

    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='produtos/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_venda = models.CharField(max_length=10, choices=UNIDADE_VENDA_CHOICES)
    estoque = models.PositiveIntegerField()
    fornecedor = models.ForeignKey(SuplierProfile, on_delete=models.CASCADE, related_name='produtos')

    def __str__(self):
        return self.nome
