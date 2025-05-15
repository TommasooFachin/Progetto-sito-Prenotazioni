from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm 
from .models import Account


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            Account.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                nome=form.cleaned_data['nome'],
                cognome=form.cleaned_data['cognome'],
                is_societario=False  # forza sempre a False
            )
            # Passa una variabile per mostrare la spunta
            return render(request, 'accounts/register.html', {'form': RegisterForm(), 'success': True})
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})