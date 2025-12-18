from kivi_paperi_sakset import KiviPaperiSakset
from tekoaly_parannettu import TekoalyParannettu

class KPSParempiTekoaly(KiviPaperiSakset):
    def __init__(self):
        self._tekoaly = TekoalyParannettu(10)

    def _toisen_siirto(self, ensimmaisen_siirto):
        # Aseta viimeisin siirto tekoälylle
        self._tekoaly.aseta_siirto(ensimmaisen_siirto)
        # Kysy tekoälyn siirto
        siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {siirto}")
        return siirto
