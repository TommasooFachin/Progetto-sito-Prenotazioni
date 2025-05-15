from django import forms
from .models import Account
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.ModelForm):
    # ridefiniti qui perche di tipo diverso
    password = forms.CharField(widget=forms.PasswordInput)
    is_societario = forms.BooleanField(required=False, label="Societario")

    class Meta:
        model = Account
        fields = ['nome', 'cognome', 'email', 'password', 'is_societario']


    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("La mail inserita è già stata utilizzata.")
        return email
    # per fare il salvataggio della password in modo sicuro.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user