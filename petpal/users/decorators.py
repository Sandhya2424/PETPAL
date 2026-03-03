from django.http import HttpResponse
from .models import UserProfile

def role_required(required_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponse("Not allowed")

            profile = UserProfile.objects.get(user=request.user)
            if profile.role != required_role:
                return HttpResponse("Not allowed")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
