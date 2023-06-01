from django.db import models
from authentication.models import MyUser
from product.models import Product
from userprofile.models import UserProfile

# Create your models here.

STATUS_CHOICES = (
    ("Ordered", "Ordered"),
    ("Paid", "Paid"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
)


class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    user_address = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    order_time = models.DateTimeField(
        auto_now_add=True,
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Ordered")

    def __int__(self):
        return int(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.price
