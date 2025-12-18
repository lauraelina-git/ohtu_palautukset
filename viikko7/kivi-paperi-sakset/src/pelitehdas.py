from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


def luo_peli(valinta):
    if valinta == "a":
        return KPSPelaajaVsPelaaja()
    if valinta == "b":
        return KPSTekoaly()
    if valinta == "c":
        return KPSParempiTekoaly()

    return None
