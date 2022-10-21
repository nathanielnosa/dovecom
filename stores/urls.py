from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('home', views.home, name = 'home'),
    path('details/<str:id>/', views.details, name = 'details'),
    path('search', views.search, name = 'search'),
    path('addToCart/<str:id>/', views.addToCart, name = 'addToCart'),
    path('myCart', views.myCart, name = 'myCart'),
    path('manageCart/<str:id>/', views.manageCart, name = 'manageCart'),
    path('emptyCart', views.emptyCart, name = 'emptyCart'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/<str:id>/', views.payment, name = 'payment'),
    path('<str:ref>/', views.verify_payment, name='verify-payment')
]