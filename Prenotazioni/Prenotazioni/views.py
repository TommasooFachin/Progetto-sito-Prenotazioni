from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Specifica il template della home