from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import elimina_corso

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),   
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),  #primo parametro è il nome della vista, secondo il nome dell'url
    path('gestione_polisportiva_home/', views.gestione_polisportiva_home, name='gestione_polisportiva_home'),
    path('gestione_campi/', views.gestione_campi, name='gestione_campi'),
    path('gestione_prenotazioni/', views.gestione_prenotazioni, name='gestione_prenotazioni'),
    path('polisportive/', views.lista_polisportive, name='lista_polisportive'),
    path('polisportiva/<int:polisportiva_id>/campi/', views.campi_polisportiva, name='campi_polisportiva'),
    path('prenota_ajax/', views.prenota_ajax, name='prenota_ajax'),
    path('mie-prenotazioni/', views.mie_prenotazioni, name='mie_prenotazioni'),
    path('polisportiva/<int:pk>/', views.dettaglio_polisportiva, name='dettaglio_polisportiva'),
    path('gestione_corsi/', views.gestione_corsi, name='gestione_corsi'),
    path('gestione_corsi/elimina/<int:corso_id>/', elimina_corso, name='elimina_corso'),

]
