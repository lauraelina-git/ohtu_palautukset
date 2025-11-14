import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id in [1, 2]:
                return 10
            return 0

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)
            return None

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    # Alkuperäinen testi
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42
        varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        pankki_mock.tilisiirto.assert_called()
    
    # Ensimmäinen laajennettu testi

    def test_ostos_yhdella_tuotteella_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", ANY, 5
        )
    
    # Toinen testi
    
    def test_ostos_kahdella_eri_tuotteella_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito (5 €)
        self.kauppa.lisaa_koriin(2)  # leipä (3 €)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            42,
            "12345",
            ANY,
            8  # 5 + 3
        )

    def test_ostos_kahdella_samalla_tuotteella_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",       # asiakkaan nimi
            42,            # mockattu viite
            "12345",       # asiakkaan tilinumero
            ANY,           # kaupan tili (ei ole testin fokus)
            10             # yhteishinta: 5 + 5
        )

    def test_ostos_tuotteella_jota_on_ja_tuotteella_joka_on_loppu_tilisiirto_oikeilla_parametreilla(self):
        # Päivitetään varaston toiminta: tuote 1 saatavilla, tuote 2 loppu
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10   # saatavilla
            if tuote_id == 2:
                return 0    # loppu
            return 0

        self.varasto_mock.saldo.side_effect = varasto_saldo

        # Aloitetaan asiointi ja lisätään tuotteet
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito (saatavilla)
        self.kauppa.lisaa_koriin(2)  # leipä (loppu)
        self.kauppa.tilimaksu("pekka", "12345")

        # Tarkistetaan, että vain saatavilla olevan tuotteen hinta veloitetaan
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            42,        # mockattu viite
            "12345",   # asiakkaan tilinumero
            ANY,       # kaupan tili (ei ole testin fokus)
            5          # vain maito 5 €, koska leipää ei ollut
        )
    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        # Minea kaupassa
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, 5 €
        self.kauppa.tilimaksu("Minea", "12345")

        #  Andreas kaupassa
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)  # leipä, 3 €
        self.kauppa.tilimaksu("Andreas", "67890")

        # Tarkistetaan ensimmäinen tilisiirto
        self.pankki_mock.tilisiirto.assert_any_call(
            "Minea",
            42,
            "12345",
            ANY,
            5  # vain maito
        )

        # Tarkistetaan toinen tilisiirto
        self.pankki_mock.tilisiirto.assert_any_call(
            "Andreas",
            42,
            "67890",
            ANY,
            3  # vain leipä, edellisen ostoksen hinta ei näy
        )
    
    def test_uusi_viitenumero_jokaiselle_maksutapahtumalle(self):
        # Asetetaan viitegeneraattori palauttamaan eri viitenumero jokaiselle kutsulle
        self.viitegeneraattori_mock.uusi.side_effect = [1001, 1002]

        # Ensimmäinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("Minea", "12345")

        # Toinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("Andreas", "67890")

        # Tarkistetaan, että viitegeneraattorin metodia kutsuttiin kaksi kertaa
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

        self.pankki_mock.tilisiirto.assert_any_call(
            "Minea",
            1001,      # ensimmäinen viite
            "12345",
            ANY,
            5
        )
        self.pankki_mock.tilisiirto.assert_any_call(
            "Andreas",
            1002,      # toinen viite
            "67890",
            ANY,
            3
        )
    def test_tilimaksu_kutsuu_tilisiirto_myos_tyhja_korilla_summalla_0(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.tilimaksu("pekka", "12345")

        # Tarkistetaan, että pankin tilisiirto kutsuttiin, mutta summana 0
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            42,          # mockattu viite
            "12345",
            ANY,
            0            # tyhjä kori → summa 0
        )

    # coveragen nostamiseksi...
    def test_poista_korista_paivittaa_korin_ja_varaston(self):
        # Aloitetaan asiointi ja lisätään tuotteet
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito
        self.kauppa.lisaa_koriin(2)  # leipä

        # Poistetaan tuote 1
        self.kauppa.poista_korista(1)

        # Maksu -> summaksi jää vain jäljelle jäänyt tuote (leipä, 3€)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            42,
            "12345",
            ANY,
            3  # vain leipä
        )