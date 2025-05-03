from django.shortcuts import render

def accounts(request):
    return render(request, 'accounts/accounts.html')  # Specifica il percorso del template
    
