from urllib import request
from django.http import HttpResponse
from pyexpat.errors import messages
from django.contrib.auth.decorators import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from .forms import *
from django.contrib.auth.models import Group


# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Customer')
            group.user_set.add(user)
            login(request, user)
            return redirect('customer_view')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'signup.html', {'form': form})
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='Manager').exists():
                    return redirect('manager_view')
                elif user.groups.filter(name='Customer').exists():
                    return redirect('customer_view')
    else:
        form = AuthenticationForm()
    return render (request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('landing_page')

def menu_view(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'menu.html', {'categories': categories, 'menu_items': menu_items})
    

@login_required(login_url = 'login')
def manager_view(request):
    if not request.user.groups.filter(name='Manager').exists():
        return HttpResponse("You don't have permission.")

    orders = Order.objects.all()
    menu_items = MenuItem.objects.all()

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            form = ItemForm()  
            message = "Item added successfully!"
            return render(request, 'manager.html', {'form': form , 'message': message , 'orders': orders, 'menu_items': menu_items})
    else:
        form = ItemForm()
    return render(request, 'manager.html', {'form': form , 'orders': orders, 'menu_items': menu_items})

@login_required(login_url='login')
def delete_menu_item(request, item_id):
    if not request.user.groups.filter(name='Manager').exists():
        return HttpResponse("You don't have permission.")

    MenuItem.objects.filter(id=item_id).delete()
    return redirect('manager_view')

@login_required(login_url='login')
def edit_menu_item(request, item_id):
    if not request.user.groups.filter(name='Manager').exists():
        return HttpResponse("You don't have permission.")

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        available = request.POST.get('available') == 'on'
        MenuItem.objects.filter(id=item_id).update(name=name, description=description, price=price, category_id=category_id, available=available)
    return redirect('manager_view')

@login_required(login_url='login')
def customer_view(request):
    if not request.user.groups.filter(name='Customer').exists():
        return HttpResponse("Not allowed.")
    orders = Order.objects.all().filter(customer=request.user)
    return render(request, 'customer.html', {'orders': orders})

@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(customer=request.user)
            order.items.set(form.cleaned_data['items'])
            order.save()
            return redirect('customer_view')
    else:
        form = OrderForm()
    return render(request, 'place_order.html', {'form': form})