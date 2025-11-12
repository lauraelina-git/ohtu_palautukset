HINTA = 5


class Kassapaate:
    def __init__(self):
        self.__myytyja_lounaita = 0

    def lataa(self, kortti, summa):
        if summa > 0:
            kortti.lataa(summa)

    def osta_lounas(self, maksukortti):
        if maksukortti.saldo() >= HINTA:
            maksukortti.osta(HINTA)
            self.__myytyja_lounaita = self.__myytyja_lounaita + 1
            return True  # Voimme palauttaa True, jos osto onnistui
        else:
            return False  # Voimme palauttaa False, jos saldo ei riitä
