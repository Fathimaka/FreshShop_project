from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from freshshopapp import views
urlpatterns = [
    path('', views.home, name='home'),  # This makes base.html the first page
    path('accounts/', include('django.contrib.auth.urls')),  # Login and Logout routes
    path('register/', views.register, name='register'),
    path('view-product/', views.view_product, name='view_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    
]