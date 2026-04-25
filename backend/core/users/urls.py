from django.urls import path
from . import views

urlpatterns = [
    path("", views.AdminUserListView.as_view(), name="admin-user-list"),
    path("<uuid:pk>/", views.AdminUserDetailView.as_view(), name="admin-user-detail"),
    path("me/", views.CurrentUserView.as_view(), name="user-me"),
    path("me/change-password/", views.ChangePasswordView.as_view(), name="user-change-password"),
    path("invite/", views.AdminInviteUserView.as_view(), name="user-invite"),
    path("invite/resend/", views.AdminResendInviteView.as_view(), name="user-invite-resend"),
    path("set-password/", views.SetPasswordView.as_view(), name="user-set-password"),
    path("login/", views.LoginView.as_view(), name="user-login"),
    path("forgot-password/", views.ForgotPasswordView.as_view(), name="user-forgot-password"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="user-reset-password"),
]