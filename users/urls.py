from django.urls import path
from knox import views as knox_views
from .views import RegisterStaffView, LoginStaffView, GetLoggedUserFromToken

urlpatterns = [
    path('register/', RegisterStaffView.as_view(), name='staff-register'),
    path('login/', LoginStaffView.as_view(), name='staff-login'),
    path('logged-in-user/', GetLoggedUserFromToken.as_view(), name='staff-logged-user'),
    path('logout/', knox_views.LogoutView.as_view(), name='staff-logout'),
]
