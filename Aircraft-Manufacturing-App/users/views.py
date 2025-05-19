from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from parts.models import Part
from aircrafts.models import Aircraft
from .models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic import UpdateView

@login_required
def profile_view(request):
    profile = None
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    return render(request, "profile.html", {"user": request.user, "profile": profile})

@login_required
def dashboard(request):
    parts_count = Part.objects.filter(team=request.user.profile.team).count()
    aircraft_count = Aircraft.objects.count()
    return render(request, 'users/dashboard.html', {
        'parts_count': parts_count,
        'aircraft_count': aircraft_count,
    })

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)
    
class UserProfileEditView(UpdateView):
    model = User
    fields = ['username', 'email']  # add fields you want to allow editing
    template_name = 'users/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('users-profile', kwargs={'pk': self.object.pk})
