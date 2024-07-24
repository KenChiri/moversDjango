from django.urls import reverse
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from movers import settings
from .tokens import generate_token

# Create your views here.

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        username = request.POST.get("userId")
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        password_repeat = request.POST.get("pwdRepeat")

        if password != password_repeat:
            messages.error(request, "Passwords do not match")
            return render(request, 'authenticator/signUp.html')

        if not username.isalnum():
            messages.error(request, "Username should be alphanumeric")
            return render(request, 'authenticator/signUp.html')

        User = get_user_model()
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'authenticator/signUp.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'authenticator/signUp.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.is_active = False
        user.save()

        messages.success(request, "Your account was created successfully. We will send you an email for activation.")

        subject = "Welcome to MOVERS."
        message = f"Hello {user.first_name},\n\Thank you for visiting our website. We have sent you a confirmation email, please confirm that this is your email address.\n\nThank You\nTeam MOVERS"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)

        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ AccuReport - Login"
        message2 = render_to_string("email_confirmation.html", {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email = EmailMessage(email_subject, message2, settings.EMAIL_HOST_USER, [user.email])
        email.fail_silently = True
        email.send()
        return redirect('login')

    return render(request, "authenticator/signUp.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        messages.success(request, 'Your account has been activated successfully')
        return redirect('index')
    else:
        return render(request, "activation_failed.html")


def user_login(request):
    if request.method == 'POST':
        identification = request.POST.get('credentials')
        password = request.POST.get("pwd")

        User = get_user_model()
        user = authenticate(request, username=identification, password=password)
        if user is None:
            try:
                user = User.objects.get(Q(email=identification))
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                messages.error(request, "No such user.")
                return redirect('login')

        if user is not None:
            auth_login(request, user)
            request.session['fname'] = f"{user.first_name} {user.last_name}"
            messages.success(request, f"Welcome back {user.first_name} {user.last_name}")
            return redirect('index')
        else:
            messages.error(request, "Incorrect password")

    return render(request, "authenticator/signIn.html")


def index(request):
    if 'fname' not in request.session:
        return redirect('login')

    fname = request.session['fname']
    return render(request, "authenticator/index.html", {'fname': fname})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')



def mail_otp(request):
    if request.method == 'POST':
        user_mail = request.POST.get('credentials')
        User = get_user_model()

        try:
            user = User.objects.get(email=user_mail)
        except User.DoesNotExist:
            messages.error(request, "Email does not exist.")
            return render(request, "authenticator/email_verification.html")

        current_site = get_current_site(request)
        subject = "Password Reset Request"
        message = render_to_string("pwd_reset_email.html", {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user.email])
        email.send()

        messages.success(request, "Password reset email sent.")
        return redirect('email_verification')  # Replace 'email_verification' with your desired URL

    return render(request, "authenticator/email_verification.html")


def pwdReset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get("new_pwd")
            confirm_password = request.POST.get("pwdRepeat")

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
        else:
            return render(request, "authenticator/password-reset.html")
    else:
        return render(request, "authenticator/reset_failed.html")
