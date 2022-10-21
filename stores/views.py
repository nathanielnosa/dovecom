from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from . models import *

from django.core.paginator import Paginator
from django.db.models import Q

from .forms import CheckoutForm
from django.contrib import messages

from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'stores/index.html')

def home(request):
    # sliders
    slides = Carousel.objects.all()
    # products
    products = Product.objects.all().order_by('-created_at')
    # pagination
    pagination = Paginator(products,12)
    page_number = request.GET.get('page')
    product_list = pagination.get_page(page_number)
    
    context={
        'slides':slides,
        'products':products,
        'paginator':product_list
    }
    return render(request, 'stores/home.html',context)

def details(request,id):
    product = Product.objects.get(id=id)
    context={
        'product':product
    }
    return render(request, 'stores/detail.html',context)

# search 
def search(request):
    kword = request.GET.get('kw')
    result = Product.objects.filter(Q(title__icontains = kword) |Q(price__icontains = kword)|Q(description__icontains = kword))
    context={
        'product':result
    }
    return render(request, 'stores/search.html',context)

def addToCart(request,id):
    # get the product
    cart_product  = Product.objects.get(id=id)
    # check if cart exist
    cart_id = request.session.get('cart_id',None)
    if cart_id:
        cart_item = Cart.objects.get(id=cart_id)

        this_product_in_cart = cart_item.cartproduct_set.filter(product = cart_product)

        if this_product_in_cart.exists():
            cartproduct = this_product_in_cart.last()
            cartproduct.quantity +=1
            cartproduct.subtotal += cart_product.price
            cartproduct.save()
            cart_item.total += cart_product.price
            cart_item.save()
        else:
            cartproduct = CartProduct.objects.create(
                cart = cart_item,product = cart_product,rate = cart_product.price,quantity=1,subtotal=cart_product.price)
            cart_item.total += cart_product.price
            cart_item.save()


    else:
        cart_item = Cart.objects.create(total=0)
        request.session['cart_id'] = cart_item.id
        cartproduct = CartProduct.objects.create(cart = cart_item,product = cart_product,rate = cart_product.price,quantity=1,subtotal=cart_product.price)
        cart_item.total += cart_product.price
        cart_item.save()

    return redirect('home')

def myCart(request):

    cart_id = request.session.get('cart_id',None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        cart = None
    context = {
        'cart':cart
    }
    return render(request, 'stores/mycart.html',context )


def manageCart(request,id):
    action = request.GET.get('action')

    cart_obj = CartProduct.objects.get(id=id)
    cart = cart_obj.cart

    if action == 'inc':
        cart_obj.quantity +=1
        cart_obj.subtotal += cart_obj.rate
        cart_obj.save()
        cart.total += cart_obj.rate
        cart.save()
    elif action == 'dcr':
        cart_obj.quantity -=1
        cart_obj.subtotal -= cart_obj.rate
        cart_obj.save()
        cart.total -= cart_obj.rate
        cart.save()

        if cart_obj.quantity == 0:
            cart_obj.delete()

    elif action == 'rmv':
        cart.total -= cart_obj.subtotal
        cart.save()
        cart_obj.delete()
    return redirect('myCart')

def emptyCart(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)

        cart.cartproduct_set.all().delete()
        cart.total = 0
        cart.save()
    return redirect('myCart')


def checkout(request):
    cart_id = request.session.get('cart_id', None)
    cart_obj = Cart.objects.get(id=cart_id)
    form = CheckoutForm()

    # checkout authentication
    if request.user.is_authenticated and request.user.profile:
        pass
    else:
        return redirect('/user/loginuser/?next=/checkout/')
    # getting cart
    if cart_id:
        cart_obj = Cart.objects.get(id=cart_id)

        # assign to cart
        if request.user.is_authenticated and request.user.profile:
            cart_obj.profile = request.user.profile
            cart_obj.save()
        # end
    else:
        cart_obj = None
    
    # form
    if request.method == 'POST':
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.cart = cart_obj
            form.discount = 0
            form.subtotal = cart_obj.total
            form.amount = cart_obj.total
            form.order_status = 'Order Received'
            pay_mth = form.payment_method
            del request.session['cart_id']
            pay_mth = form.payment_method
            form.save()
            order = form.id
            if pay_mth == 'Paystack':
                return redirect('payment', id =order)  

            messages.success(request, 'Order have been placed successfully')
            return redirect('home')
        else:
            messages.error(request, 'No Order have been placed')
            return redirect('home')

    context = {
        'cart':cart_obj,
        'form':form,
    }
    return render(request, 'stores/checkout.html',context)


def payment(request,id):
    orders = Order.objects.get(id=id)
    context= {
        'order':orders,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request, 'stores/payment.html',context)

def verify_payment(request:HttpRequest,ref:str)-> HttpResponse:
    payment = get_object_or_404(Order, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'verification successful')
    else:
        messages.warning(request, 'Verification failed')
    return redirect('dashboard')