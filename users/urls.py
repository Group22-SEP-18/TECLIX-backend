from django.urls import path
from knox import views as knox_views
from .views import RegisterStaffView

urlpatterns = [
    path('register/', RegisterStaffView.as_view(), name='staff-register'),
    path('logout/', knox_views.LogoutView.as_view(), name='staff-logout'),
]
