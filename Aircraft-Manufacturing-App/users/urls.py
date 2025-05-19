from django.urls import path
from .views import UserDetailView, UserProfileEditView
from . import views

urlpatterns = [
    path('profile/<int:pk>/', UserDetailView.as_view(), name='users-profile'),
    path('profile/<int:pk>/edit/', UserProfileEditView.as_view(), name='users-profile-edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
