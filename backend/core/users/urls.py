from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserListCreateView.as_view(), name="user-list-create"),
    path("<uuid:pk>/", views.UserRetrieveUpdateDestroyView.as_view(), name="user-detail"),
    path("me/", views.CurrentUserView.as_view(), name="user-me"),
    path("me/change-password/", views.ChangePasswordView.as_view(), name="user-change-password"),
]