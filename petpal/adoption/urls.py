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
from adoption import views

app_name = 'adoption'

urlpatterns = [
    path('browse/', views.BrowsePetsView.as_view(), name='browse_pets'),
    path('search/', views.SearchPetsView.as_view(), name='search_pets'),
    path('pet/<int:pet_id>/', views.PetDetailView.as_view(), name='pet_detail'),
    path('request/<int:pet_id>/', views.AdoptionRequestView.as_view(), name='adoption_request'),
    path('success/', views.AdoptionSuccessView.as_view(), name='adoption_success'),
    path('toggle-wishlist/<int:pet_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),

    path('my-applications/', views.MyApplicationsView.as_view(), name='my_applications'),
    path('admin/requests/', views.AdminAdoptionRequestsView.as_view(), name='admin_requests'),
    path('admin/approve/<int:req_id>/', views.ApproveRequestView.as_view(), name='approve_request'),
    path('admin/reject/<int:req_id>/', views.RejectRequestView.as_view(), name='reject_request'),

]






