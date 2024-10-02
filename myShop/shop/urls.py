from django.urls import path, re_path

from . import views

app_name = 'shop'

urlpatterns = [
    path("", views.product_list, name='product_list'),
    path('add_item/', views.add_item, name='add_item'),
    path('add_category/', views.add_category, name="add_category"),
    path('registration/', views.sign_up, name="sign-up"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path("<slug:category_slug>/", views.product_list, name='product_list_by_category'),
    path("<int:id>/<slug:slug>/", views.product_detail, name='product_detail'),
]
