from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required
def index(request):
    return render(request, "finance/bank.html")



@login_required
def bank(request):
    return render(request, "finance/home.html")


def connect_bank(request):
    return render(request, "finance/connect_bank.html")


def resolve(request):
    messages.error(request, "Please fix your account!")
    return render(request, "finance/resolve.html")


def send_money(request):
    return render(request, "finance/send_money.html")

