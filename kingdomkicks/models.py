from django.core.validators import RegexValidator
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=254, default='')


class Product(models.Model):
    name = models.CharField(max_length=254, default='')
    sku = models.CharField(max_length=254, default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images')
    category = models.CharField(max_length=254, default='')
    size = models.CharField(max_length=254, default='')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Checkout(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email_address = models.EmailField(max_length=254)
    delivery_location = models.TextField()
    product_ids = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
