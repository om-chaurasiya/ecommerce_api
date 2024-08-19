# cart/urls.py
from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView,ProductListView,ProductDetailView

urlpatterns = [
    path('cart/', CartView.as_view(), name='my-cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
