from django import forms
from .models import Account
from django.contrib.auth.hashers import make_password
from .models import Campo, Corso

class RegisterForm(forms.ModelForm):
    # ridefiniti qui perche di tipo diverso
    password = forms.CharField(widget=forms.PasswordInput)
    is_societario = forms.BooleanField(required=False, label="Societario")

    class Meta:
        model = Account
        fields = ['nome', 'cognome', 'email', 'password']


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
    



class CampoForm(forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['nome', 'superficie', 'tipo']  # campi da inserire dall'admin


class CorsoForm(forms.ModelForm):
    class Meta:
        model = Corso
        fields = ['nome', 'campo', 'data_inizio', 'data_fine', 'ora_inizio', 'ora_fine']
        widgets = {
            'data_inizio': forms.DateInput(attrs={'type': 'date'}),
            'data_fine': forms.DateInput(attrs={'type': 'date'}),
            'ora_inizio': forms.TimeInput(attrs={'type': 'time'}),
            'ora_fine': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        campo = cleaned_data.get('campo')
        data_inizio = cleaned_data.get('data_inizio')
        data_fine = cleaned_data.get('data_fine')
        ora_inizio = cleaned_data.get('ora_inizio')
        ora_fine = cleaned_data.get('ora_fine')

        if campo and data_inizio and data_fine and ora_inizio and ora_fine:
            # Cerca corsi che si sovrappongono nello stesso campo e intervallo di date/ore
            overlapping = Corso.objects.filter(
                campo=campo,
                data_inizio__lte=data_fine,
                data_fine__gte=data_inizio,
            ).exclude(pk=self.instance.pk)

            for corso in overlapping:
                # Controlla se c'è sovrapposizione di orari
                if not (ora_fine <= corso.ora_inizio or ora_inizio >= corso.ora_fine):
                    raise forms.ValidationError(
                        "Esiste già un corso nello stesso campo e orario in queste date."
                    )
        return cleaned_data