from django.urls import path

from . import views

urlpatterns = [
    path(
        "username-exists/",
        views.UsernameExistsView.as_view(),
        name="auth-username-exists",
    ),
    path(
        "user-whitelist/",
        views.UserWhitelistView.as_view(),
        name="auth-user-whitelist",
    ),
    path("login/", views.LoginView.as_view(), name="auth-login"),
    path(
        "token-refresh/",
        views.TokenRefreshView.as_view(),
        name="auth-token-refresh",
    ),
]
