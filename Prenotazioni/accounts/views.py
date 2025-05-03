from django.shortcuts import render

def accounts(request):
    return render(request, 'accounts/accounts.html')  # Specificaaa il percorso del template
    
