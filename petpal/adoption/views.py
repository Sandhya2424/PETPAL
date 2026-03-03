from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

from pets.models import Pet
from adoption.models import AdoptionRequest, Wishlist
from adoption.forms import AdoptionRequestForm

# Browse Pets (All Available Pets)
@method_decorator(login_required, name='dispatch')
class BrowsePetsView(View):
    def get(self, request):
        pets = Pet.objects.filter(status='Available')
        favorite_pets = Wishlist.objects.filter(user=request.user).values_list('pet_id', flat=True)
        return render(request, 'browse_pets.html', {'pets': pets, 'favorite_pets': favorite_pets})

# Search Pets (Separate View)
@method_decorator(login_required, name='dispatch')
class SearchPetsView(View):
    def get(self, request):
        query = request.GET.get('q')
        pets = Pet.objects.filter(status='Available')
        if query:
            pets = pets.filter(Q(name__icontains=query) | Q(breed__icontains=query))
        favorite_pets = Wishlist.objects.filter(user=request.user).values_list('pet_id', flat=True)
        return render(request, 'browse_pets.html', {'pets': pets, 'favorite_pets': favorite_pets, 'query': query})

# Pet Details
@method_decorator(login_required, name='dispatch')
class PetDetailView(View):
    def get(self, request, pet_id):
        pet = Pet.objects.filter(id=pet_id, status='Available').first()
        if not pet:
            return redirect('adoption:browse_pets')
        in_wishlist = Wishlist.objects.filter(user=request.user, pet=pet).exists()
        return render(request, 'pet_detail.html', {'pet': pet, 'in_wishlist': in_wishlist})

# Adoption Request
@method_decorator(login_required, name='dispatch')
class AdoptionRequestView(View):
    def get(self, request, pet_id):
        pet = Pet.objects.filter(id=pet_id, status='Available').first()
        if not pet:
            return redirect('adoption:browse_pets')
        form = AdoptionRequestForm()
        return render(request, 'adoption_form.html', {'form': form, 'pet': pet})

    def post(self, request, pet_id):
        pet = Pet.objects.filter(id=pet_id, status='Available').first()
        if not pet:
            return redirect('adoption:browse_pets')
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.pet = pet
            adoption_request.adopter = request.user
            adoption_request.save()
            return redirect('adoption:adoption_success')
        return render(request, 'adoption_form.html', {'form': form, 'pet': pet})

# Adoption Success
class AdoptionSuccessView(View):
    def get(self, request):
        return render(request, 'adoption_success.html')

# Toggle Wishlist
@login_required
def toggle_wishlist(request, pet_id):
    pet = Pet.objects.filter(id=pet_id).first()
    if not pet:
        return redirect('adoption:browse_pets')

    wishlist_item = Wishlist.objects.filter(user=request.user, pet=pet).first()
    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(user=request.user, pet=pet)
    return redirect('adoption:browse_pets')

# Wishlist Page
@method_decorator(login_required, name='dispatch')
class WishlistView(View):
    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


# ✅ NEW — My Applications Page (ONLY FOR LOGGED-IN USER)
@method_decorator(login_required, name='dispatch')
class MyApplicationsView(View):
    def get(self, request):
        applications = AdoptionRequest.objects.filter(adopter=request.user).order_by('-requested_at')
        return render(request, 'my_applications.html', {'applications': applications})





# SHELTER ADMIN - VIEW ALL ADOPTION REQUESTS


@method_decorator(login_required, name='dispatch')
class AdminAdoptionRequestsView(View):
    def get(self, request):
        # Only shelter admin allowed
        if request.user.userprofile.role != 'shelter_admin':
            return redirect('home')

        requests_list = AdoptionRequest.objects.all().order_by('-requested_at')
        return render(request, 'admin_adoption_requests.html', {'requests_list': requests_list})


# APPROVE REQUEST


@method_decorator(login_required, name='dispatch')
class ApproveRequestView(View):
    def get(self, request, req_id):
        if request.user.userprofile.role != 'shelter_admin':
            return redirect('home')

        adoption_request = AdoptionRequest.objects.get(id=req_id)

        adoption_request.status = 'Approved'
        adoption_request.save()

        # Update pet status also
        adoption_request.pet.status = 'Adopted'
        adoption_request.pet.save()

        return redirect('adoption:admin_requests')



# REJECT REQUEST


@method_decorator(login_required, name='dispatch')
class RejectRequestView(View):
    def get(self, request, req_id):
        if request.user.userprofile.role != 'shelter_admin':
            return redirect('home')

        adoption_request = AdoptionRequest.objects.get(id=req_id)
        adoption_request.status = 'Rejected'
        adoption_request.save()

        return redirect('adoption:admin_requests')
