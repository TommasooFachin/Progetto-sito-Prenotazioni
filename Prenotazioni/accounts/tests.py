from django.test import TestCase
from .models import Polisportiva, Campo, Account, Prenotazione
from datetime import date, time
from django.urls import reverse

#test la creazione di una prenotazione
class PrenotazioneModelTest(TestCase):
    def setUp(self):
        self.polisportiva = Polisportiva.objects.create(  #crea una polisportiva di test
            nome="Test ASD", città="Modena", indirizzo="Via Test", telefono="1234567890", email="test@asd.it"
        )
        self.account = Account.objects.create(   # crea un account di test
            nome="Mario", cognome="Rossi", email="mario@rossi.it", password="test", is_societario=False, is_active=True
        )
        self.campo = Campo.objects.create(  #campo di test
            nome="Campo 1", superficie="erba", tipo="calcio", polisportiva=self.polisportiva
        )

    def test_creazione_prenotazione(self):   #definizione del vero e proprio test
        pren = Prenotazione.objects.create(
            campo=self.campo,
            account=self.account,
            data=date.today(),
            ora_inizio=time(10, 0),
            ora_fine=time(11, 0),
            durata=60,
            costo=20.0,
            stato='accettata',
            pagato=True
        )
        self.assertEqual(pren.campo.nome, "Campo 1")
        self.assertEqual(pren.account.email, "mario@rossi.it")
        self.assertTrue(pren.pagato)



#test la vista: campi_polsportiva
class CampiPolisportivaViewTest(TestCase):
    def setUp(self):
        self.polisportiva = Polisportiva.objects.create(
            nome="Test ASD", città="Modena", indirizzo="Via Test", telefono="1234567890", email="test@asd.it"
        )

    def test_campi_polisportiva_view(self):
        url = reverse('campi_polisportiva', args=[self.polisportiva.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test ASD")