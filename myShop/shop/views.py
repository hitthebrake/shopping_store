from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Category, Product
from .forms import RegisterForms, AddCategoryForms, AddItemForms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from cart.forms import CartAddProductForm

def user_login(request):
    if request.method=='POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("shop:product_list"))
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form":form })

@require_POST
def user_logout(request):
    logout(request)
    return redirect(reverse('shop:login'))

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = product.filter(category=category)
    return render(request, 'shop/product/list.html', {'product':product, 'category':category, 'categories':categories})



def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product':product, 'cart_product_form':cart_product_form})


@login_required(login_url="shop:login", redirect_field_name="/add_item")
@permission_required('shop.add_product', login_url='shop:login', raise_exception=True)
def add_item(request):
    if request.method == "POST":
        form = AddItemForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('shop:product_list'))
    else:
        form = AddItemForms()
    return render(request, "shop/product/add_item.html", {'form':form})


@login_required(login_url="shop:login", redirect_field_name="/add_item")
@permission_required('shop.add_category', login_url='shop:login', raise_exception=True)
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("shop:product_list"))
    else:
        form = AddCategoryForms()
    return render(request, "shop/product/add_category.html", {'form':form})



def sign_up(request):
    if request.method=="POST":
        form = RegisterForms(request.POST)
        if form.is_valid():
            user = form.save()
            df, created = Group.objects.get_or_create(name="default")
            df.user_set.add(user)
            login(request, user)
            return redirect(reverse("shop:product_list"))
    form = RegisterForms()
    return render(request, "registration/sign_up.html", {"form":form})



  

# Create your views here.
