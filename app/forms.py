from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app.models import Category, MenuItem

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput(), help_text="" )
    password2 = forms.CharField(label=("Password confirmation"), widget=forms.PasswordInput(), help_text="" )

    class Meta(UserCreationForm.Meta):
        model = User 
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'username', 'email' , 'password1', 'password2') 
        help_texts = {
             'username': None,
             'first_name': None,
             'last_name': None,
             'email': None,
    }
        
class ItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'available']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class OrderForm(forms.Form):
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )