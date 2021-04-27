from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="shopHome"),
    path('about/', views.about, name="aboutUs"),
    path('contact/', views.contact, name="contactUs"),
    path('tracker/', views.tracker, name="tracker"),
    path('products/<int:myid>', views.productView, name="productView"),
    path('checkOut/', views.checkOut, name="checkout"),
    path('search/',views.search, name="search"),
    path('smartphone/', views.smartphone, name="smartphone"),
    path('accessories/', views.accessories, name="accessories"),
    path('television/', views.television, name="television"),
    path('laptops/', views.laptops, name="laptops"),
    path('search/', views.search, name="search"),
    path('bestsellers/', views.bestsellers, name="bestsellers")
]