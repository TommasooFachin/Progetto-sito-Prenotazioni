from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm 
from .models import Account
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CampoForm
from .models import Campo


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

class CustomLoginView(LoginView):
    template_name = 'accounts/accounts.html'

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'is_societario') and user.is_societario:
            return reverse('gestione_polisportiva')
        return reverse('home')
    
@login_required
def gestione_polisportiva(request):
    user = request.user
    polisportiva = user.polisportiva  # Assumendo che l'utente abbia il campo polisportiva

    if request.method == 'POST':
        form = CampoForm(request.POST)
        if form.is_valid():
            campo = form.save(commit=False)
            campo.polisportiva = polisportiva
            campo.save()
            # Puoi aggiungere un messaggio di successo o reindirizzare
    else:
        form = CampoForm()

    return render(request, 'accounts/gestione_polisportiva.html', {
        'form': form,
        'polisportiva': polisportiva,
    })


def gestione_polisportiva_home(request):
    polisportiva = request.user.polisportiva
    return render(request, 'accounts/gestione_polisportiva_home.html', {'polisportiva': polisportiva})

def gestione_campi(request):
    polisportiva = request.user.polisportiva
    campi = Campo.objects.filter(polisportiva=polisportiva)
    if request.method == 'POST':
        if 'elimina' in request.POST:
            Campo.objects.filter(id=request.POST['elimina']).delete()
        else:
            form = CampoForm(request.POST)
            if form.is_valid():
                campo = form.save(commit=False)
                campo.polisportiva = polisportiva
                campo.save()
    form = CampoForm()
    return render(request, 'accounts/gestione_campi.html', {'form': form, 'campi': campi, 'polisportiva': polisportiva})

def gestione_prenotazioni(request):
    # Per ora solo una pagina vuota
    return render(request, 'accounts/gestione_prenotazioni.html')