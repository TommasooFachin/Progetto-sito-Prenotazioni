from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm 
from .models import Account
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CampoForm
from .models import Campo, Polisportiva, Prenotazione
from django.db.models import Q
from datetime import date, datetime, timedelta
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

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
            return reverse('gestione_polisportiva_home')
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


def lista_polisportive(request):
    citta = request.GET.get('citta', '')
    sport = request.GET.get('sport', '')
    data = request.GET.get('data', '')
    ora = request.GET.get('ora', '')

    polisportive = Polisportiva.objects.all()

    # Filtro città/società
    if citta:
        polisportive = polisportive.filter(
            Q(nome__icontains=citta) | Q(città__icontains=citta)
        )

    # Filtro sport
    if sport:
        polisportive = polisportive.filter(campi__tipo__icontains=sport)

    # Filtro per disponibilità di almeno un campo in data/ora
    if data and ora:
        disponibili = []
        for p in polisportive.distinct():
            campi_disp = p.campi.all()
            if sport:
                campi_disp = campi_disp.filter(tipo__icontains=sport)
            # Escludi i campi prenotati in quella data/ora
            campi_disp = campi_disp.exclude(
                prenotazioni__data=data,
                prenotazioni__ora_inizio__lte=ora,
                prenotazioni__ora_fine__gt=ora,
                prenotazioni__stato='accettata'
            )
            if campi_disp.exists():
                disponibili.append(p.id)
        polisportive = polisportive.filter(id__in=disponibili)

    context = {
        'polisportive': polisportive.distinct(),
        'citta': citta,
        'sport': sport,
        'data': data,
        'ora': ora,
    }
    return render(request, 'accounts/lista_polisportive.html', context)


def campi_polisportiva(request, polisportiva_id):
    data = request.GET.get('data', '')
    if not data:
        data = date.today().isoformat()  # Imposta la data di oggi se non fornita
    ora = request.GET.get('ora', '')
    sport = request.GET.get('sport', '')

    polisportiva = Polisportiva.objects.get(id=polisportiva_id)
    campi = polisportiva.campi.all()
    if sport:
        campi = campi.filter(tipo__icontains=sport)

    orari = [
        "08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30",
        "12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30",
        "16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30",
        "20:00","20:30","21:00","21:30","22:00","22:30","23:00"
    ]

    # Costruisci una mappa: campo_id -> {ora: prenotato}
    prenotazioni_map = {}
    for campo in campi:
        prenotazioni_map[campo.id] = {o: False for o in orari}
        prenotazioni = campo.prenotazioni.filter(data=data, stato='accettata')
        for pren in prenotazioni:
            ora_corrente = pren.ora_inizio.strftime("%H:%M")
            ora_fine = pren.ora_fine.strftime("%H:%M")
            while ora_corrente != ora_fine:
                if ora_corrente in prenotazioni_map[campo.id]:
                    prenotazioni_map[campo.id][ora_corrente] = True
                # aggiungi 30 minuti
                t = datetime.strptime(ora_corrente, "%H:%M") + timedelta(minutes=30)
                ora_corrente = t.strftime("%H:%M")

    today = date.today().isoformat()  # <-- aggiungi questa riga

    return render(request, 'accounts/campi_polisportiva.html', {
        'polisportiva': polisportiva,
        'campi': campi,
        'data': data,
        'ora': ora,
        'sport': sport,
        'orari': orari,
        'prenotazioni_map': prenotazioni_map,
        'today': today, 
    })

@csrf_exempt
@login_required
def prenota_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        campo_id = data.get('campo_id')
        data_pren = data.get('data')
        orari = data.get('orari', [])
        modalita_pagamento = data.get('modalita_pagamento', 'struttura')
        campo = Campo.objects.get(id=campo_id)
        if not orari:
            return JsonResponse({'success': False, 'error': 'Nessun orario selezionato'})
        orari.sort()
        ora_inizio = datetime.strptime(orari[0], "%H:%M")
        ora_fine = (datetime.strptime(orari[-1], "%H:%M") + timedelta(minutes=30)).time()
        durata = len(orari) * 30
        pren = Prenotazione.objects.create(
            campo=campo,
            account=request.user,
            data=data_pren,
            ora_inizio=ora_inizio.time(),
            ora_fine=ora_fine,
            durata=durata,
            costo=5.00 * len(orari),
            stato='accettata',
            pagato=False  # di default
        )
        if modalita_pagamento == 'online':
            # Redirect a pagina di pagamento virtuale
            return JsonResponse({'success': True, 'redirect': f'/accounts/pagamento_online/{pren.id}/'})
        return JsonResponse({'success': True})
@login_required
def pagamento_online(request, pren_id):
    pren = get_object_or_404(Prenotazione, id=pren_id, account=request.user)
    if request.method == "POST":
        pren.pagato = True
        pren.save()
        return render(request, 'accounts/pagamento_successo.html')
    return render(request, 'accounts/pagamento_online.html', {'pren': pren})
    
@login_required
def mie_prenotazioni(request):
    prenotazioni = Prenotazione.objects.filter(account=request.user).order_by('-data', 'ora_inizio')
    if request.method == "POST":
        elimina_id = request.POST.get("elimina")
        if elimina_id:
            Prenotazione.objects.filter(id=elimina_id, account=request.user).delete()
            return redirect('mie_prenotazioni')
    return render(request, 'accounts/mie_prenotazioni.html', {'prenotazioni': prenotazioni})


def is_societario(user):
        return user.is_authenticated and user.is_societario  # Adatta secondo il tuo modello utente

@login_required
@user_passes_test(is_societario)
def gestione_prenotazioni(request):
    polisportiva = request.user.polisportiva  # Prendi la polisportiva dell'utente societario
    prenotazioni = Prenotazione.objects.filter(campo__polisportiva=polisportiva)
    if request.method == "POST":
        pren_id = request.POST.get("elimina")
        pren = get_object_or_404(Prenotazione, id=pren_id, campo__polisportiva=polisportiva)
        pren.delete()
        return redirect('gestione_prenotazioni')
    return render(request, 'accounts/gestione_prenotazioni.html', {'prenotazioni': prenotazioni})

def dettaglio_polisportiva(request, pk):
    polisportiva = get_object_or_404(Polisportiva, pk=pk)
    return render(request, 'accounts/dettaglio_polisportiva.html', {'polisportiva': polisportiva})
