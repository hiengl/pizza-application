from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from orders.models import Category, Topping, PizzaMenu, PastaAndSalads, OrderItem, OrderInfor
import datetime

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    return redirect('foodlist')


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse("foodlist"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


def register_view(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        email_address = request.POST.get("email_address")
        if not username:
            raise ValueError('The given username must be set.')
        user = User.objects.create_user(username=username, email=email_address, password=password) 
        user.firstname = request.POST.get("firstname")
        user.lastname = request.POST.get("lastname")
        user.save()
        return render(request, "orders/login.html", {"message": "Please login."})
    return render(request, 'orders/register.html', {"message": "Create an account."})


@login_required
def food_list(request):
    #user_infor = get_object_or_404(User, user=request.user)
    current_order = []
    total = 0
    if OrderItem.objects.filter(owner=request.user, is_ordered=False):
        current_order = OrderItem.objects.filter(owner=request.user, is_ordered=False)
        total = sum([item.price for item in current_order])
 
    context = {
        "category_list": Category.objects.all(),
        "current_order": current_order,
        "total": total
    }
    return render(request, "orders/food_list.html", context)


@login_required()
def add_to_cart(request, **kwargs):
    # get the user information
    #user_infor = get_object_or_404(User, user=request.user)
    # filter food by id and price
    if PizzaMenu.objects.filter(id=kwargs.get('food_id'), small_price=kwargs.get('price')):
        item = PizzaMenu.objects.get(id=kwargs.get('food_id'), small_price=kwargs.get('price'))
    elif PizzaMenu.objects.filter(id=kwargs.get('food_id'), large_price=kwargs.get('price')):
        item = PizzaMenu.objects.get(id=kwargs.get('food_id'), large_price=kwargs.get('price'))
    else:
        item = PastaAndSalads.objects.get(id=kwargs.get('food_id'), price=kwargs.get('price'))

    # create orderitem of the selected dish
    item_id = kwargs.get('price')[:4] + datetime.datetime.now().strftime('%y%m%d%H%M%S')
    order_item, status = OrderItem.objects.get_or_create(owner=request.user,
                                                         item=str(item),
                                                         price=kwargs.get('price'),
                                                         item_id=item_id)
    order_item.save()
    return redirect(reverse('foodlist'))


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.get(pk=item_id)
    if item_to_delete:
        if item_to_delete.quantity > 1:
            item_to_delete.quantity -= 1
            item_to_delete.save()
        else:
            item_to_delete.delete()
    return redirect(reverse('foodlist'))


@login_required()
def shopping_cart(request):
    #user_infor = get_object_or_404(User, user=request.user)
    current_order = []
    total = 0
    if OrderItem.objects.filter(owner=request.user, is_ordered=False):
        current_order = OrderItem.objects.filter(owner=request.user, is_ordered=False)
        #total = sum([item.price for item in current_order])
        total = current_order[0].get_cart_total()
 
    context = {
        "current_order": current_order,
        "total": total
    }
    return render(request, 'orders/shopping_cart.html', context)
    
    
@login_required()
def order_infor(request, **kwargs):
    #user_infor = get_object_or_404(User, user=request.user)
    current_order = []
    total = 0
    if OrderItem.objects.filter(owner=request.user, is_ordered=False):
        current_order = OrderItem.objects.filter(owner=request.user, is_ordered=False)
        total = sum([item.price for item in current_order])
        for ite in current_order:
            ite.is_ordered = True
            ite.save()

    # create order
    if total > 0:
        order_id = request.user.username[:3] + datetime.datetime.now().strftime('%y%m%d%H%M%S')
        order, status = OrderInfor.objects.get_or_create(user=request.user, order_id=order_id, amount=total)
        order.save()
        context = {
            "order": order,
            "orders": OrderInfor.objects.filter(status=False)
        }
        return render(request, 'orders/order_infor.html', context)