from django.contrib import admin

# Register your models here.
from .models import Category, Topping, PizzaMenu, PastaAndSalads, OrderItem, OrderInfor
 
admin.site.register(Category)
admin.site.register(Topping)
admin.site.register(PizzaMenu)
admin.site.register(PastaAndSalads)
admin.site.register(OrderItem)
admin.site.register(OrderInfor)