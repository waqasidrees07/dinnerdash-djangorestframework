from django.shortcuts import render, redirect, HttpResponse
from .forms import SignupForm
from django.views.generic import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignupSerializer, VerifyEmailSerializer, LoginSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from.models import MyUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse
from .serializers import PasswordResetSerializer
from django.core.mail import send_mail
from django.utils.encoding import force_str
from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer
import uuid


class ActivateView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("login")
        else:
            return HttpResponse("Activation link is invalid!")


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "customer_registration.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your email id"
            message = render_to_string(
                "acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                "Please confirm your email address to complete the registration>"
            )

        else:
            form = SignupForm()
        return render(request, "customer_registration.html", {"form": form})


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SignUpView(APIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Signup successful. Please check your email for verification.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = serializer.validated_data['verification_code']

            # Find the user profile associated with the email
            try:
                user_profile = MyUser.objects.get(email=email)
            except MyUser.DoesNotExist:
                return Response({'detail': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the verification code matches
            if user_profile.verification_code == verification_code:
                user_profile.email_verify = True
                user_profile.save()
                return Response({'detail': 'Email verification successful.'})
            else:
                return Response({'detail': 'Invalid verification code.', "user": user_profile.verification_code}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Nothing"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Create or retrieve token for the authenticated user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        email = request.data.get('email')
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            return Response({'detail': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate password reset token
        token_generator = default_token_generator
        token = token_generator.make_token(user)

        # Send password reset email with the token
        reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'token': token}))
        send_mail(
            f'Password Reset Mail',
            f'{reset_url}',
            'waqasidrees15@gmail.com',
            [f'{email}'],
            fail_silently=False,
        )
        return Response({'detail': 'Password reset email sent.'})


class PasswordResetConfirm(PasswordResetConfirmView):
    serializer_class = PasswordResetSerializer
    success_url = '/password-reset-complete/'  # Set the URL for password reset complete

    def get(self, request, *args, **kwargs):
        # Verify the password reset token
        token = kwargs['token']
        uid = kwargs['uidb64']
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = MyUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid password reset link.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Reset the user's password
        return super().post(request, *args, **kwargs)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
