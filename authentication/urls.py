from django.urls import path
from authentication import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .forms import (
    LoginForm,
    MyPasswordChangeForm,
    MyPasswordResetForm,
    MySetPasswordForm,
)


urlpatterns = [
    path(
        "activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        views.ActivateView.as_view(),
        name="activate",
    ),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "passwordchange/",
        auth_views.PasswordChangeView.as_view(
            template_name="password_change.html",
            form_class=MyPasswordChangeForm,
            success_url="/passwordchangedone/",
        ),
        name="passwordchange",
    ),
    path(
        "passwordchangedone/",
        auth_views.PasswordChangeView.as_view(
            template_name="password_change_done.html"
        ),
        name="passwordchangedone",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html", form_class=MyPasswordResetForm
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            form_class=MySetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("registration/", views.SignupView.as_view(), name="signup"),
    path("signup/", views.SignUpView.as_view()),
    path("email-verification/", views.VerifyEmailView.as_view(), name="email-verification"),
    path("sign-in/", views.LoginView.as_view(), name="sign-in"),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('password-reset-confirm/<slug:uidb64>/<slug:token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    # path('accounts/facebook/login/', views.FacebookLogin.as_view(), name='facebook_login'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
