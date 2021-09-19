from django.urls import path
from knox import views as knox_views
from .views import RegisterStaffView, LoginStaffView, GetLoggedUserFromToken, UpdateSalespersonAccStateView, \
    UpdateDistOfficerAccStateView

urlpatterns = [
    path('register/', RegisterStaffView.as_view(), name='staff-register'),
    path('login/', LoginStaffView.as_view(), name='staff-login'),
    path('logged-in-user/', GetLoggedUserFromToken.as_view(), name='staff-logged-user'),
    path('logout/', knox_views.LogoutView.as_view(), name='staff-logout'),
    path('approve/salesperson/<int:id>', UpdateSalespersonAccStateView.as_view(), name='approve-sp'),
    path('approve/distribution-officer/<int:id>', UpdateDistOfficerAccStateView.as_view(), name='approve-do'),

]
