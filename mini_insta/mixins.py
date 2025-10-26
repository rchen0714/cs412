from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Profile

class CheckLogin(LoginRequiredMixin):
    
    def get_login_url(self):
        return reverse('login')

    def get_my_profile(self):
        return Profile.objects.get(user=self.request.user)