from django.urls import reverse
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from movers import settings
from .tokens import generate_token
from django.contrib.messages import success
from authenticate.models import CustomUser
from booking.models import *
# Create your views here.

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        username = request.POST.get("userId")
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        password_repeat = request.POST.get("pwdRepeat")


        # Validation logic BEFORE user creation
        if password != password_repeat:
            messages.error(request, "Passwords do not match")
            return render(request, 'authenticator/signUp.html')

        if not username.isalnum():
            messages.error(request, "Username should be alphanumeric")
            return render(request, 'authenticator/signUp.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'authenticator/signUp.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'authenticator/signUp.html')

        try:
            # Create the user after validation
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.first_name = firstname
            user.last_name = lastname
            #hashed password
            user.set_password(password)
            user.is_active = False  # Set user as inactive until activation
            user.save()

        except Exception as e:
            messages.error(request, "An error occurred during registration. Please try again.")
            return render(request, 'authenticator/signUp.html')

        success(request, "Your Account created Successully.  We will send you an Email for Activation")

        #take him to the login page is the signup is successfull
        subject = "Welcome to MOVERS."
        message = "Hello" + user.first_name + "\n" + "Thank you for visiting our website. We have sent you a confirmation email, please confirm that this is your email address.\n\nThank You\nTeam MOVERS"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        # Generate email confirmation message
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Movers - Login"
        message2 = render_to_string("email_confirmation.html", {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email = EmailMessage(email_subject, message2, settings.EMAIL_HOST_USER, [user.email])
        email.fail_silently = True
        email.send()


        return redirect('signup')

    return render(request, "authenticator/signUp.html")


def activate(request, uidb64, token):
    try:
        # decode the user ID from the base64 string
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request,user)
        messages.success(request, 'Your account has been activated successfully')
        return redirect('login')
    else:
        return render(request, "activation_failed.html")


def user_login(request):
    # Initialize messages before the conditional block
    msg = get_messages(request)
    
    if request.method == 'POST':
        identification = request.POST.get('credentials')
        password = request.POST.get("pwd")
        
        # Authentication with various fields
        user = get_user_model()
        try:
            # Fetch the user who matches username or email
            user = CustomUser.objects.get(Q(username=identification) | Q(email=identification))
            
            # Check password validity
            if user.check_password(password):
                auth_login(request, user)
                fname = f"{user.first_name} {user.last_name}"
                request.session['fname'] = fname
                messages.success(request, "Welcome back " + fname)
                return redirect('index')
            else:
                messages.error(request, "Incorrect password")
        except CustomUser.DoesNotExist:
            messages.error(request, "No such user.")
            return redirect('login')

    return render(request, "authenticator/signIn.html", {'messages': msg})


def index(request):
    if 'fname' not in request.session:
        return redirect('login')

    fname = request.session['fname']
    bookings=ServiceBooking.objects.all()
    drivers=Driver.objects.all()
    vehicles=Vehicle.objects.all()
    return render(request, "authenticator/index.html", {'fname': fname,'bookings':bookings,'vehicles':vehicles,'drivers':drivers})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')



def mail_otp(request):
    if request.method == 'POST':
        user_mail = request.POST.get('credentials')
        user = get_user_model()

        try:
            user = CustomUser.objects.get(email=user_mail)
        except CustomUser.DoesNotExist:
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
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
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
