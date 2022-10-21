import secrets
from django.db import models
from users.models import Profile

from . paystack import PayStack
# Create your models here.
class Carousel(models.Model):
    slider = models.ImageField(upload_to='sliders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=300)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    view_count = models.PositiveIntegerField(default=0,null=True,blank=True)
    warranty = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.price}'
        
    @property
    def get_percent(self):
        percentage = (self.discount_price * 100) / self.price
        return percentage


class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null =True, blank=True)
    total = models.PositiveIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'cart :::: {str(self.id)}'

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null =True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null =True, blank=True)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    create_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'cart :::: {str(self.cart.id)} - cart product {self.id}'

ORDER_STATUS = (
    ('Order Received', 'Order Received'),
    ('Order Processing', 'Order Processing'),
    ('Order Canceled', 'Order Canceled'),
    ('Order Completed', 'Order Completed'),
)

METHOD = (
    ('Cash on delivery','Cash on delivery'),
    ('Paystack','Paystack'),
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null =True, blank=True)
    order_by = models.CharField(max_length=200)
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=14)
    email = models. EmailField()
    discount = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices= ORDER_STATUS)
    create_at = models.DateTimeField(auto_now_add=True)


    payment_method = models.CharField(max_length=20, choices=METHOD,default='Cash on delivery')
    payment_completed = models.BooleanField(default=False,null=True,blank=True)
    ref = models.CharField(max_length=20,null=True, blank=True)

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref= ref
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.order_status} :::: {str(self.id)}'

    def amount_value(self)->int:
        return self.amount * 100
        
    def verify_payment(self):
        paystack = PayStack()
        status, result =  paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] /100 == self.amount:
                self.payment_completed = True
            self.save()
        
        if self.order_status == 'Order Completed':
            self.save()
            self.cart.delete()
        if self.payment_completed:
            return True
        return False