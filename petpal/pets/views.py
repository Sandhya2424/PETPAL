from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pets.decorators import admin_required
from pets.forms import PetForm
from pets.models import Pet



@method_decorator(login_required, name="dispatch")
@method_decorator(admin_required, name="dispatch")
class AddPetView(View):
    def get(self, request):
        form_instance = PetForm()
        return render(request, 'add_pet.html', {'form': form_instance})

    def post(self, request):
        form_instance = PetForm(request.POST, request.FILES)
        if form_instance.is_valid():
            pet = form_instance.save(commit=False)
            pet.added_by = request.user
            pet.save()
            return redirect('pets:manage_pets')
        else:
            print("error")
            return render(request, 'add_pet.html', {'form': form_instance})



@method_decorator(login_required, name="dispatch")
@method_decorator(admin_required, name="dispatch")
class ManagePetsView(View):
    def get(self, request):
        pets = Pet.objects.filter(added_by=request.user)
        return render(request, 'manage_pets.html', {'pets': pets})



@method_decorator(login_required, name="dispatch")
@method_decorator(admin_required, name="dispatch")
class EditPetView(View):
    def get(self, request, pk):
        pet = Pet.objects.get(id=pk)
        form_instance = PetForm(instance=pet)
        return render(request, 'edit_pet.html', {'form': form_instance})

    def post(self, request, pk):
        pet = Pet.objects.get(id=pk)
        form_instance = PetForm(request.POST, request.FILES, instance=pet)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('pets:manage_pets')
        else:
            return render(request, 'edit_pet.html', {'form': form_instance})



@method_decorator(login_required, name="dispatch")
@method_decorator(admin_required, name="dispatch")
class DeletePetView(View):
    def get(self, request, pk):
        pet = Pet.objects.get(id=pk)
        pet.delete()
        return redirect('pets:manage_pets')
