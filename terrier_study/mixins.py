from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import UserProfile


class CheckLogin(LoginRequiredMixin):
    """
    A mixin to ensure the user is logged in before accessing certain views.
    """

    # Redirect unauthenticated users to the login page
    def get_login_url(self):
        return reverse("login")

    # Get the UserProfile associated with the logged-in user
    def get_my_profile(self):
        """
        Return the UserProfile instance for the current authenticated user.
        """
        return UserProfile.objects.get(user=self.request.user)