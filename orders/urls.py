from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("menu", views.food_list, name="foodlist"),
    path("menu/<int:food_id>/<price>", views.add_to_cart, name="addtocart"),
    path("menu/<int:item_id>", views.delete_from_cart, name="deletefromcart"),
    path("shopping_cart", views.shopping_cart, name="shoppingcart"),
    path("order_infor", views.order_infor, name="orderinfor")
]