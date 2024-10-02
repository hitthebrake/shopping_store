from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Product

class RegisterForms(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2' ]

class AddItemForms(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'stock']


class AddCategoryForms(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']