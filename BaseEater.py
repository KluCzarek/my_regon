# -*- coding: utf-8 -*-

import os

pytanie_o_filtry = 'Jakie chcesz ustawic filtry?\n1) Wojewodztwo\n2) Powiat\n3) Miasto\n4) Kod pocztowy\n5) Forma prawna\n6) PKD przewazajace\n'

pytanie_o_wojewodztwo = 'Ktore wojewodztwo chcesz wybrac?\n1) Dolnoslaskie\n2) Kujawsko-pomorskie\n3) Lubelskie\n\
4) Lubuskie\n5) Lodzkie\n6) Malopolskie\n7) Mazowieckie\n8) Opolskie\n9) Podkarpackie\n\
10) Podlaskie\n11) Pomorskie\n12) Slaskie\n13) Swietokrzyskie\n14) Warminsko-mazurskie\n\
15) Wielkopolskie\n16) Zachodniopomorskie\n'

pytanie_o_kod_pocztowy = 'Podaj poszukiwany kod pocztowy'
pytanie_o_forme_prawna = 'Podaj rodzaj formy prawnej\n1) Osoba prawna\n2) Osoba fizyczna\n3) Lokalna osoba prawna\n4) Lokalna osoba fizyczna'
pytanie_o_PKD_przewazajace = 'Podaj kod PKD przewazajacego'

 
lista_wojewodztw = {
    1: u'DOLNOŚLĄSKIE',
    2: u'KUJAWSKO-POMORSKIE',
    3: u'LUBELSKIE',
    4: u'LUBUSKIE',
    5: u'ŁÓDZKIE',
    6: u'MAŁOPOLSKIE',
    7: u'MAZOWIECKIE',
    8: u'OPOLSKIE',
    9: u'PODKARPACKIE',
    10: u'PODLASKIE',
    11: u'POMORSKIE'
    12: u'ŚLĄSKIE',
    13: u'ŚWIĘTOKRZYSKIE',
    14: u'WARMIŃSKO-MAZURSKIE',
    15: u'WIELKOPOLSKIE',
    16: u'ZACHODNIOPOMORSKIE',
}

directory = 'D:\\REGON'

# przewijarka przez pliki:


for filename in os.listdir(directory):
    #tutaj co ma robic z kazdym plikiem - generalnie tu bedzie metoda juz do szukania po zadanych filtrach
    pass
    

def poprawnosc_odpowiedzi(zadane_pytanie,mozliwe_odpowiedzi):
    correct_answer = False
    while correct_answer != True:
        answer = int(raw_input(zadane_pytanie))
        if answer in mozliwe_odpowiedzi:
            return answer

def czy_rekord_pasuje_do_zapytania(rekord, filters):
    for key in filters.keys():
        if rekord[key] not in filters[key]:
            return False
        elif rekord[key] in filters[key]:
            pass

    




