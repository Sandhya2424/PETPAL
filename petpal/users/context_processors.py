from .models import UserProfile

def user_role(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {'user_role': profile.role}
        except:
            return {'user_role': None}
    return {'user_role': None}
