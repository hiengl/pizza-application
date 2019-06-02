from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name_cate = models.CharField(max_length=100)
    def __str__(self):
        return self.name_cate 

class Topping(models.Model):
    name_top = models.CharField(max_length=100)
    def __str__(self):
        return self.name_top

class PizzaMenu(models.Model):
    id_cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    dish = models.CharField(max_length=100)
    small_price = models.DecimalField(max_digits = 5, decimal_places = 2)
    large_price = models.DecimalField(max_digits = 5, decimal_places = 2)
    def __str__(self):
        return self.dish

class PastaAndSalads(models.Model):
    id_cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    dish = models.CharField(max_length=100)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    def __str__(self):
        return self.dish


class OrderItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item_id = models.CharField(max_length=16)
    item = models.CharField(max_length=100)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)

    def get_cart_total(self):
        return sum([dish.price for dish in OrderItem.objects.filter(owner=self.owner, is_ordered=False)])
            
    def __str__(self):
       return f"{self.item} {self.price}"


class OrderInfor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    time_order = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.order_id}"




