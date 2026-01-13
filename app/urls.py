from django.contrib import admin
from django.urls import path
from .views import *
from .models import *


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('menu/', menu_view, name='menu'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('manager/', manager_view, name='manager_view'),
    path('customer/', customer_view, name='customer_view'),
    path('place_order/', place_order, name='place_order'),
    path('delete_menu_item/<int:item_id>/', delete_menu_item, name='delete_menu_item'),
    path('edit_menu_item/<int:item_id>/', edit_menu_item, name='edit_menu_item'),
]