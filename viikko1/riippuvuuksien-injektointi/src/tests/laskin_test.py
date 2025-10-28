import unittest
from laskin import Laskin


class StubIO:
    def __init__(self, inputs):
        self.inputs = inputs
        self.outputs = []

    def lue(self, teksti):
        return self.inputs.pop(0)

    def kirjoita(self, teksti):
        self.outputs.append(teksti)


class TestLaskin(unittest.TestCase):
    def test_yksi_summa_oikein(self):
        io = StubIO(["1", "3", "-9999"])
        laskin = Laskin(io)
        laskin.suorita()

        self.assertEqual(io.outputs[0], "Summa: 4")

    def test_kaksi_perakkaista_laskua(self):
        # Ensimmäinen lasku: 1 + 2 = 3
        # Toinen lasku: 5 + 6 = 11
        # Lopetus -9999
        io = StubIO(["1", "2", "5", "6", "-9999"])
        laskin = Laskin(io)
        laskin.suorita()

        # Tarkistetaan, että molemmat summat tulostuivat oikein
        self.assertEqual(io.outputs[0], "Summa: 3")
        self.assertEqual(io.outputs[1], "Summa: 11")
