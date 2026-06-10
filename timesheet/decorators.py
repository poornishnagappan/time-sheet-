from django.http import HttpResponse
from functools import wraps
from .models import Profile

def manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponse("Login required")

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return HttpResponse("Profile not found")

        if profile.role != "manager":
            return HttpResponse("Access denied: Manager only")

        return view_func(request, *args, **kwargs)

    return wrapper
