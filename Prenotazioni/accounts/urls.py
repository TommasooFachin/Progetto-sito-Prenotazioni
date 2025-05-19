from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('gestione_polisportiva/', views.gestione_polisportiva_home, name='gestione_polisportiva'),
    path('gestione_campi/', views.gestione_campi, name='gestione_campi'),
    path('gestione_prenotazioni/', views.gestione_prenotazioni, name='gestione_prenotazioni'),
]


