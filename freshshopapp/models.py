from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name= models.CharField(max_length=255)
    description= models.TextField()
    price= models.DecimalField(max_digits=10, decimal_places=2)
    image= models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

