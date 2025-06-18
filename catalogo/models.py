from django.db import models

class Category(models.Model):
    name = models.CharField("Name", max_length=100)
    slug = models.SlugField("Slug",  unique=True)
    description = models.TextField("Description", blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True,
        help_text="Parent category"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name= models.CharField("Name", max_length=255)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to='products/')
    Category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    in_stock = models.IntegerField("Stock")
    unit_sale= models.CharField("Unit of Sale", max_length=50)
    supplier = models.ForeignKey(
        'profiles.SuplierProfile',
        on_delete=models.CASCADE,
        related_name='products'
    )

# Create your models here.
