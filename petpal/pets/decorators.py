from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.role == 'shelter_admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')   # redirect if not admin
    return wrapper
