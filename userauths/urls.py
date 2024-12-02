# urls.py
from django.urls import path
from . import views

app_name = "userauths"

urlpatterns = [
    path('splash/', views.splash, name='splash'),
    path('register/', views.signup_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('set-pin/', views.set_pin, name='set_pin'),
    path('enter-pin/', views.enter_pin, name='enter_pin'),
    path('finish/', views.finish, name='finish'),
    path('btc_payment/', views.btc_payment, name='btc_payment'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('login/', views.login_view, name="login"),
    path('credit-card/', views.credit_card_view, name='credit_card'),    
    path('credit-card-uploaded/', views.success, name='success'),
    path('plans-payments/', views.payment_plans, name='payment_plans'),
    path('plans-detail/<int:plan_id>/', views.payment_plan_detail, name='payment_plan_detail'),
    path('email-lookup/', views.email_lookup_view, name='email_lookup'),

    

    # Add similar URLs for signup, logout, etc.
]
