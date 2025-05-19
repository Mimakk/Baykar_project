from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import AircraftViewSet

router = DefaultRouter()
router.register(r'aircrafts', AircraftViewSet, basename='aircraft')

urlpatterns = [
    path('', views.aircraft_list, name='aircrafts-list'),
    path('assemble/', views.aircraft_assemble, name='aircrafts-assemble'),
    path('api/', include(router.urls)),
]