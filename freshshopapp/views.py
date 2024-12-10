from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from freshshopapp.forms import CustomUserCreationForm
from freshshopapp.models import Cart, CartItem, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache


# Create your views here.

def home(request):
    return render(request, 'base.html')  # Render the base.html as the home page

@never_cache
@login_required
def view_product(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request
    product_list = Product.objects.all()
    
    if query:
        product_list = product_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(product_list, 3)  # Paginate with 3 products per page
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'view_product.html', {
        'page_obj': page_obj,
        'query': query,  # Pass the query to the template for display
    })

#register
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            return redirect('login')  # Redirect to login page
        else:
            print(form.errors)  # Debug: Print errors to console
    else:
        form =CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@never_cache
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    product = get_object_or_404(Product, id=product_id)

    # Create the cart if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        # If the product is already in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_product')  # Redirect to the product view or cart page

#view cart
@never_cache
@login_required
def view_cart(request):
    # Ensure a cart exists for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Fetch cart items
    cart_items = CartItem.objects.filter(cart=cart)
    
    # If there are no items in the cart, handle this case
    if not cart_items:
        total_price = 0  # No items in the cart
    else:
        total_price = 0
        for item in cart_items:
            item.individual_total = item.product.price * item.quantity
            total_price += item.individual_total

    # Render the cart page with items and total price
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

#checkout
@never_cache
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not logged in

    # Fetch the user's cart and cart items
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Handle the "Place Order" button
        cart_items.delete()  # Clear the cart
        return render(request, 'order_confirmation.html', {'total_price': total_price})

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@require_POST
@login_required
@never_cache
def remove_from_cart(request):
    item_id = request.POST.get('item_id')  # Get the item ID from the form
    try:
        # Ensure the cart item belongs to the logged-in user's cart
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()  # Remove the item from the cart
    except CartItem.DoesNotExist:
        pass  # Handle case where the item does not exist

    return redirect('view_cart') 
@require_POST
@login_required
@never_cache
def update_cart_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')

    try:
        # Fetch the cart item and ensure it belongs to the logged-in user
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
    except CartItem.DoesNotExist:
        pass  # Handle case where the item does not exist

    return redirect('view_cart')
