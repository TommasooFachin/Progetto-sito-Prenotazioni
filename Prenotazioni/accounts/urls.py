from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts'),  # Associa la vista accounts alla root di /accounts/
]


