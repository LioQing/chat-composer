from django.urls import path

from . import views

urlpatterns = [
    path(
        "username-exists/",
        views.UsernameExistsView.as_view(),
        name="auth-username-exists",
    ),
    path(
        "is-whitelisted/",
        views.IsWhitelistedView.as_view(),
        name="auth-is-whitelisted",
    ),
    path(
        "user-whitelist/",
        views.UserWhitelistView.as_view(),
        name="auth-user-whitelist",
    ),
    path("is-admin/", views.IsAdminView.as_view(), name="auth-is-admin"),
    path("login/", views.LoginView.as_view(), name="auth-login"),
    path(
        "token-refresh/",
        views.TokenRefreshView.as_view(),
        name="auth-token-refresh",
    ),
]
