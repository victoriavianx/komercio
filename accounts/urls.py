from django.urls import path
from . import views

urlpatterns = (
    path("accounts/", views.AccountView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("accounts/newest/<int:num>/", views.AccountDetailView.as_view())
)