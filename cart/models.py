from django.db import models
from authentication.models import MyUser
from product.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __int__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.price
