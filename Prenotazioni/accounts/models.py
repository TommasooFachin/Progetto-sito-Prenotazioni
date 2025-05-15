from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, nome='', cognome='', is_societario=False, **extra_fields):
        if not email:
            raise ValueError('L\'email è obbligatoria')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, cognome=cognome, is_societario=is_societario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, nome='', cognome='', is_societario=False, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, nome, cognome, is_societario, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    id= models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    is_societario = models.BooleanField(default=False)
    polisportiva = models.ForeignKey(
        'Polisportiva',           # nome del modello a cui si riferisce
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cognome']

    objects = AccountManager()

    def __str__(self):
        return self.email


class Polisportiva(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    città = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=200, unique=True)
    telefono = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100, unique=True)

class Campo(models.Model):
    id = models.AutoField(primary_key=True)
    superficie = models.CharField(max_length=20, choices=[('terra', 'terra'), ('sintetico', 'sintetico'), ('erba', 'erba'), ('cemento', 'cemento')])
    tipo = models.CharField(max_length=20, choices=[('calcio a 5', 'calcio a 5'), ('tennis', 'tennis'), ('padel', 'padel')])
    polisportiva = models.ForeignKey(Polisportiva, on_delete=models.CASCADE, related_name='campi')

class Prenotazione(models.Model):
    id=models.AutoField(primary_key=True)
    data = models.DateField()
    ora_inizio = models.TimeField()
    ora_fine = models.TimeField()
    durata = models.IntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    stato= models.CharField(max_length=20, choices=[('in attesa', 'In attesa'), ('accettata', 'accettata'), ('annullata', 'Annullata')])
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='prenotazioni')
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE, related_name='prenotazioni')
    class Meta:
        unique_together = ('campo', 'data', 'ora_inizio', 'ora_fine')
        