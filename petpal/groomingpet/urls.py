"""
URL configuration for petpal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from groomingpet import views

app_name = 'groomingpet'

urlpatterns = [
    path('services/', views.ServicesView.as_view(), name='services'),
    path('book/<str:service_name>/', views.BookAppointmentView.as_view(), name='book_appointment'),
    path('checkout/<int:appointment_id>/', views.CheckoutView.as_view(), name='checkout'),
    path('payment-success/<str:username>/', views.PaymentSuccessView.as_view(), name='payment_success'),
    # Adopter - My Bookings
    path('my-bookings/', views.MyBookingsView, name='my_bookings'),

    # Groomer - All Bookings
    path('bookings/', views.AllBookingsView, name='bookings'),

]










