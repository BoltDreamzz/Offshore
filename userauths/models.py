from django.contrib.auth.models import AbstractUser
from django.db import models
import pyotp

from django_countries.fields import CountryField as DjangoCountryField


class CountryField(DjangoCountryField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # This method is necessary for Django to recognize this field in forms.
        defaults = {'form_class': CountryField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    is_active = models.BooleanField(default=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)  # Ensure null=False is set
    date_of_birth = models.DateField(blank=True, null=True)
    savings = models.DecimalField(max_digits=40, decimal_places=2, null=True, blank=True)

    country = CountryField()
    ssn = models.IntegerField(null=True, blank=True)
    pin = models.CharField(max_length=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    totp_secret = models.CharField(max_length=32, null=True, blank=True)



# models.py


class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        totp = pyotp.TOTP(pyotp.random_base32())
        return totp.now()

    def __str__(self):
        return f'{self.user.username} - {self.otp_code}'


# models.py
# from django.db import models
from django.db import models

class CreditCard(models.Model):
    card_pin = models.CharField(max_length=255, help_text="Enter the car subscription number.", null=True, blank=False)
    card_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Enter the card amount.")
    card_photo = models.ImageField(upload_to="card_photos/", help_text="Upload a clear photo of the card.", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Card with amount {self.card_amount} uploaded on {self.uploaded_at}"
    
    
class PaymentPlan(models.Model):
    PLAN_DURATIONS = [
        ('biweekly', 'Every 2 Weeks'),
        ('monthly', 'Monthly'),
    ]

    name = models.CharField(max_length=50)  # Plan name (e.g., Basic, Standard, Premium)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price (e.g., 10.00, 20.00)
    duration = models.CharField(max_length=20, choices=PLAN_DURATIONS)  # Duration (biweekly or monthly)
    is_featured = models.BooleanField(default=False)  # Highlighted plan (e.g., Standard)

    def __str__(self):
        return f"{self.name} (${self.price}) - {self.get_duration_display()}"
