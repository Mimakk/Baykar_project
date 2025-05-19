from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', lambda request: redirect('login'), name='home'),
    
    path('api/users/', include('users.urls')),
    path('api/parts/', include('parts.urls')),
    path('api/aircrafts/', include('aircrafts.urls'), name="aircraft_list"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
