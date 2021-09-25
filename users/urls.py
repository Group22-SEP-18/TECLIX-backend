from django.urls import path
from knox import views as knox_views
from .views import RegisterStaffView, LoginWebStaffView, GetLoggedUserFromToken, UpdateSalespersonAccStateView, \
    UpdateDistOfficerAccStateView, LoginSalespersonStaffView, GetDOAccountsView

urlpatterns = [
    path('register/', RegisterStaffView.as_view(), name='staff-register'),
    path('login/web', LoginWebStaffView.as_view(), name='web-login'),
    path('login/salesperson/', LoginSalespersonStaffView.as_view(), name='mobile-login'),

    path('logged-in-user/', GetLoggedUserFromToken.as_view(), name='staff-logged-user'),
    path('logout/', knox_views.LogoutView.as_view(), name='staff-logout'),
    path('distribution-officer/pending/', GetDOAccountsView.as_view(), name='do-accounts'),
    path('approve/salesperson/<int:id>', UpdateSalespersonAccStateView.as_view(), name='approve-sp'),
    path('approve/distribution-officer/<int:id>', UpdateDistOfficerAccStateView.as_view(), name='approve-do'),

]
