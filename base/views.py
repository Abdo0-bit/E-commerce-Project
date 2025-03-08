from django.shortcuts import render , redirect , get_object_or_404
from .models import Product , Cart , CartItem , Shipping
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login , logout 
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm , CheckoutForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

def register(request):
    
    if request.method == 'POST' :
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request , user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()
    context = {"form" : form}
    return render(request, 'register.html', context)


def user_login(request) :
    
    if request.method == 'POST' :
        form = AuthenticationForm(request , data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request , user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    context = {"form":form}
    return render(request , 'login.html' , context)

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request, "You've been logged out successfully!")
    return redirect('home')

def home(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) )
    else:
        products = Product.objects.all()
        
    context = {'products': products, 'query': query}
    return render(request, 'home.html', context)
def product_details(request , pk) :
    
    product = get_object_or_404(Product , pk = pk)
    
    if request.method == 'POST' :
        
        if not request.user.is_authenticated:
            return redirect('login')
        cart , _ = Cart.objects.get_or_create(user=request.user)
        cart_item  , item_created  = CartItem.objects.get_or_create(cart=cart , product= product)    
    
        if not item_created  :
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request,'Added to Cart')

    context = {'product' : product}
    
    return render(request , 'product_details.html' , context)

@login_required(login_url='login')
def cart(request) :
    
    cart, _ = Cart.objects.get_or_create(user =request.user)
    products_in_cart = cart.cartitem_set.all()
    total_price = sum(item.total_price() for item in products_in_cart)
            
    context = {"products_in_cart" : products_in_cart , "total_price" :total_price}
    return render(request , 'cart.html' , context)



@login_required(login_url='login')
def add_product(request , pk) :
    
    product = get_object_or_404(Product, pk= pk)
    
    if request.method == 'POST' :
        
        cart , _ = Cart.objects.get_or_create(user= request.user)
        item   , created  = CartItem.objects.get_or_create(cart = cart , product = product)
        if not created :
            item.quantity +=1
            item.save()
            
        messages.success(request,'Added to Cart')
        
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    
@login_required(login_url='login')
def delete_product(request, pk): 
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = CartItem.objects.filter(cart=cart, product=product).first()
        
        if item:
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
            messages.success(request, f'Removed {product.name} from cart!')
        else:
            messages.error(request, f'{product.name} is not in your cart!')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')      
def update_quantity(request , pk) :
    product = get_object_or_404(Product , pk=pk)
    cart , _ =Cart.objects.get_or_create(user = request.user)
    item = CartItem.objects.filter(cart = cart , product = product).first()
    
    if request.method == 'POST'  and item :
        action = request.POST.get('action')
        if action == 'increase' :
            item.quantity+=1
            item.save()
            messages.success(request, f'Increased {product.name} quantity!')
            
        elif action == 'decrease' :
            if item.quantity > 1 :
                item.quantity -= 1
                item.save()
                messages.success(request, f'decreased {product.name} quantity!')
            else :
                item.delete()
                messages.success(request, f'Removed {product.name} from cart!')
        
    return redirect('cart')

from .models import Order, OrderItem

@login_required(login_url='login')
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    products_in_cart = cart.cartitem_set.all()

    if not products_in_cart.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')

    shipping = Shipping.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = CheckoutForm(request.POST, instance=shipping)

        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()

            order = Order.objects.create(user=request.user, shipping=shipping)


            for item in products_in_cart:
                if item.product.stock < item.quantity:
                    messages.error(request, f"Not enough stock for {item.product.name}")
                    return redirect('cart')

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                item.product.stock -= item.quantity
                item.product.save()
            cart.cartitem_set.all().delete()

            messages.success(request, "Your order has been placed successfully!")
            return redirect('order_history')

    else:
        form = CheckoutForm(instance=shipping)

    total_price = sum(item.total_price() for item in products_in_cart)

    context = {"form": form ,"products_in_cart": products_in_cart,"total_price": total_price,}

    return render(request, "checkout.html", context)


def order_history(request) :
    orders = Order.objects.filter(user = request.user).prefetch_related('orderitem_set')
    context = {'orders': orders,}
    return render(request, 'order_history.html', context)