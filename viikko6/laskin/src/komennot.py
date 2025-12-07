class Komento:
    def __init__(self, logiikka, lue_arvo, aseta_arvo):
        self._logiikka = logiikka
        self._lue_arvo = lue_arvo
        self._aseta_arvo = aseta_arvo

    def suorita(self):
        pass


class Summa(Komento):
    def suorita(self):
        arvo = self._lue_arvo()
        self._logiikka.plus(arvo)
        self._aseta_arvo(self._logiikka.arvo())


class Erotus(Komento):
    def suorita(self):
        arvo = self._lue_arvo()
        self._logiikka.miinus(arvo)
        self._aseta_arvo(self._logiikka.arvo())


class Nollaus(Komento):
    def suorita(self):
        self._logiikka.nollaa()
        self._aseta_arvo(self._logiikka.arvo())


class Kumoa(Komento):
    def suorita(self):
        self._logiikka.kumoa()  # Kutsu sovelluslogiikan kumoa-metodia
        self._aseta_arvo(self._logiikka.arvo())