# Kazdy numer REGON konczy sie suma testowa. Zeby ograniczyc mozliwosc wychwycenia automatycznego pobierania danych z REGON trzeba tworzyc prawidlowe kody REGON 
# wyliczajac je przy pomocy algorytmu do sprawdzenia sumy testowej. 
# cyfra sumy testowej to wynik modulo 11 sumy zwazonych pierwszych 8 cyfr numeru, wg wag [8,9,2,3,4,5,6,7]

from litex.regon import REGONAPI #modul zewnetrzny ogarniajacy bir
import pickle
import time
import sys
api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc') # adres serwera public uslugi BIR
api.login('a0a397f69f7e46d88afb') # klucz 4cf do logowania sie do bazy regon

def chcksm_counter(regon_str = str):
    lista_wag = [8,9,2,3,4,5,6,7]
    i = 0
    chcksm = 0
    for d in regon_str:
        chcksm = chcksm + int(d)*lista_wag[i]
        i = i + 1
    chcksm_str = str(chcksm%11)
    if len(chcksm_str) == 1: 
        last_digit = chcksm_str
    elif len(chcksm_str) == 2:
        last_digit = 0
    else:
        print "zle sie dzieje w panstwie dunskim"
    return "%s%s" %(regon_str, last_digit) # funkcja zwraca pelen, poprawny numer regon do uzycia juz w wyszukiwaniu
# regon_prep - funkcja formatuje numer z generatora do postaci argumentu dla metody chcksm_counter

def regon_prep(num):
    reg = "000000%s" %(str(num))
    return reg[len(str(num)):]

def pobor_danych_osoby_fizycznej(proper_regon):
    try: 
        res = api.full_report(proper_regon, 'PublDaneRaportFizycznaOsoba')
        full_report_results = {
            'nip' :  res.fiz_nip.text,
            'nazwisko' :  res.fiz_nazwisko.text,
            'imie1' :  res.fiz_imie1.text,
            'imie2' :  res.fiz_imie2.text,
            'dataZaistnieniaZmiany' :  res.fiz_dataZaistnieniaZmiany.text,
            'dataSkresleniazRegon' :  res.fiz_dataSkresleniazRegon.text,
            'podstawowaFormaPrawna_Symbol' :  res.fiz_podstawowaFormaPrawna_Symbol.text,
            'szczegolnaFormaPrawna_Symbol' :  res.fiz_szczegolnaFormaPrawna_Symbol.text,
            'formaFinansowania_Nazwa' :  res.fiz_formaFinansowania_Nazwa.text,
            'formaWlasnosci_Nazwa' :  res.fiz_formaWlasnosci_Nazwa.text,
            'dzialalnosciCeidg' :  res.fiz_dzialalnosciCeidg,
            'dzialalnosciRolniczych' :  res.fiz_dzialalnosciRolniczych,
            'dzialalnosciPozostalych' :  res.fiz_dzialalnosciPozostalych,
            'dzialalnoscizKrupgn' :  res.fiz_dzialalnosciZKrupgn,
            'jednostekLokalnych' :  res.fiz_jednostekLokalnych
        }
        return full_report_results
    except Exception as e:
        print 'blad poboru danych osoby fizycznej - %s' %(e)

def pobor_danych_osoby_prawnej(proper_regon):
    try:
        res = api.full_report(proper_regon, 'PublDaneRaportPrawna')
        full_report_results = {
            'regon14' : res.praw_regon14.text,
            'nip' : res.praw_nip.text,
            'numerWrejestrzeEwidencji' : res.praw_numerWrejestrzeEwidencji.text,
            'nazwa' : res.praw_nazwa.text,
            'nazwaSkrocona' : res.praw_nazwaSkrocona.text,
            'adSiedzKraj_symbol': res.praw_adSiedzKraj_Symbol.text,
            'adSiedzWojewodztwo_Symbol' : res.praw_adSiedzWojewodztwo_Symbol.text,
            'adSiedzPowiat_Symbol' : res.praw_adSiedzPowiat_Symbol.text, 
            'adSiedzGmina_Symbol' : res.praw_adSiedzGmina_Symbol.text, 
            'adSiedzKodPocztowy' : res.praw_adSiedzKodPocztowy.text, 
            'adSiedzMiejscowoscPoczty_Symbol' : res.praw_adSiedzMiejscowoscPoczty_Symbol.text,
            'adSiedzMiejscowosc_Symbol' : res.praw_adSiedzMiejscowosc_Symbol.text,
            'adSiedzUlica_Symbol' : res.praw_adSiedzUlica_Symbol.text, 
            'adSiedzNumerNieruchomosci' : res.praw_adSiedzNumerNieruchomosci.text, 
            'adSiedzNumerLokalu' : res.praw_adSiedzNumerLokalu.text, 
            'adSiedzNietypoweMiejsceLokalizacji' : res.praw_adSiedzNietypoweMiejsceLokalizacji.text,
            'adSiedzKraj_Nazwa' : res.praw_adSiedzKraj_Nazwa.text,
            'adSiedzWojewodztwo_Nazwa' : res.praw_adSiedzWojewodztwo_Nazwa.text,
            'adSiedzPowiat_Nazwa' : res.praw_adSiedzPowiat_Nazwa.text,
            'adSiedzGmina_Nazwa' : res.praw_adSiedzGmina_Nazwa.text, 
            'adSiedzMiejscowoscPoczty_Nazwa' : res.praw_adSiedzMiejscowoscPoczty_Nazwa.text, 
            'adSiedzMiescjowosc_Nazwa' : res.praw_adSiedzMiejscowosc_Nazwa.text, 
            'adSiedzUlica_Nazwa' : res.praw_adSiedzUlica_Nazwa.text, 
            'numerTelefonu' : res.praw_numerTelefonu.text, 
            'numerWewnetrznyTelefonu' : res.praw_numerWewnetrznyTelefonu.text, 
            'numerFaksu' : res.praw_numerFaksu.text,
            'numerEmail' : res.praw_adresEmail.text,
            'adresStronyInternetowej' : res.praw_adresStronyinternetowej.text, 
            'adresEmail2': res.praw_adresEmail2.text, 
            'dataPowstania' : res.praw_dataPowstania.text,
            'dataRozpoczeciaDzialanosci' : res.praw_dataRozpoczeciaDzialalnosci.text, 
            'dataWpisuDoREGON' : res.praw_dataWpisuDoREGON.text, 
            'dataZawieszeniaDzialalnosci' : res.praw_dataZawieszeniaDzialalnosci.text, 
            'dataWznowieniaDzialalnosci' : res.praw_dataWznowieniaDzialalnosci.text, 
            'dataZaistnieniaZmiany' : res.praw_dataZaistnieniaZmiany.text, 
            'dataZakonczeniaDzialalnosci' : res.praw_dataZakonczeniaDzialalnosci.text, 
            'dataSkresleniazRegon' : res.praw_dataSkresleniazRegon.text, 
            'podstawowaFormaPrawna_Symbol' : res.praw_podstawowaFormaPrawna_Symbol.text, 
            'szczegolnaFormaPrawna_Symbol' : res.praw_szczegolnaFormaPrawna_Symbol.text, 
            'formaFinansowania_Symbol' : res.praw_formaFinansowania_Symbol.text, 
            'formaWlasnosci_Symbol' : res.praw_formaWlasnosci_Symbol.text, 
            'organZalozycielski_Symbol' : res.praw_organZalozycielski_Symbol.text, 
            'organRejestrowy_Symbol' : res.praw_organRejestrowy_Symbol.text, 
            'rodzajRejestruEwidencji_Symbol' : res.praw_rodzajRejestruEwidencji_Symbol.text, 
            'podstawowaFormaPrawna_Nazwa' : res.praw_podstawowaFormaPrawna_Nazwa.text, 
            'szczegolnaFormaPrawna_Nazwa' : res.praw_szczegolnaFormaPrawna_Nazwa.text,
            'formaFinansowania_Nazwa' : res.praw_formaFinansowania_Nazwa.text, 
            'organZalozycielski_Nazwa' : res.praw_organZalozycielski_Nazwa.text, 
            'organRejestrowy_Nazwa' : res.praw_organRejestrowy_Nazwa.text, 
            'rodzajRejestruEwidencji_Nazwa' : res.praw_rodzajRejestruEwidencji_Nazwa.text, 
            'jednostekLokalnych' : res.praw_jednostekLokalnych
        }
        return full_report_results
    except IndexError:

        print 'blad poboru danych osoby prawnej - %s' %(e)

def pobor_danych_raport_podstawowy(proper_regon):
    res = api.search(regon = proper_regon)[0]
    basic_report_results = {
        'regon' :  res.Regon.text, 
        'nazwa' :  res.Nazwa.text, 
        'wojewodztwo' :  res.Wojewodztwo.text,  
        'powiat' :  res.Powiat.text,  
        'gmina' :  res.Gmina.text,  
        'miejscowosc' :  res.Miejscowosc.text,  
        'kod_pocztowy' :  res.KodPocztowy.text,  
        'ulica' :  res.Ulica.text,  
        'typ' :  res.Typ.text,  
        'silosID' :  res.SilosID
    }
    return basic_report_results

def pobor_danych_pkd(proper_regon):
    try:    
        res = api.raport_pkd(proper_regon)
        pkd_results = {
            'przewazajacePKDKod' : '',
            'przewazajacePKDNazwa' : '',
            'pozostalePKD' : []
        }
        if len(res) != 0: 
            for each in res:
                if each[2] == 0:
                    pkd_results['pozostalePKD'].append(each)
                elif each[2] == 1:
                    pkd_results['przewazajacePKDKod'] = each[0]
                    pkd_results['przewazajacePKDNazwa'] = each[1]
            return pkd_results
        else: 
            print ("rekord nie posiada PKD w bazie REGON")     
    except Exception as e: 
        print "blad pobor danych pkd %s" %(e)

def pobor_danych_lokalna_fizyczna(proper_regon): 
    try: 
        res = api.full_report(proper_regon, 'PublDaneRaportLokalnaFizycznej')
        full_report_results = {
            'regon9' : res.lokfiz_regon9.text,
            'regon14' : res.lokfiz_regon14.text,
            'nazwa' : res.lokfiz_nazwa.text,
            'silos_Symbol' : res.lokfiz_silos_Symbol.text, 
            'silos_Nazwa' : res.lokfiz_silos_Nazwa.text, 
            'adSiedzKraj_Symbol' : res.lokfiz_adSiedzKraj_Symbol.text, 
            'adSiedzWojewodztwo_Symbol' : res.lokfiz_adSiedzWojewodztwo_Symbol.text, 
            'adSiedzPowiat_Symbol' : res.lokfiz_adSiedzPowiat_Symbol.text, 
            'adSiedzGmina_Symbol' : res.lokfiz_adSiedzGmina_Symbol.text, 
            'adSiedzKodPocztowy' : res.lokfiz_adSiedzKodPocztowy.text, 
            'adSiedzMiejscowoscPoczty_Symbol' : res.lokfiz_adSiedzMiejscowoscPoczty_Symbol.text, 
            'adSiedzMiejscowosc_Symbol' : res.lokfiz_adSiedzMiejscowosc_Symbol.text, 
            'adSiedzUlica_Symbol' : res.lokfiz_adSiedzUlica_Symbol.text, 
            'adSiedzNumerNieruchomosci' : res.lokfiz_adSiedzNumerNieruchomosci.text,            
            'adSiedzNumerLokalu' : res.lokfiz_adSiedzNumerLokalu.text, 
            'adSiedzNietypoweMiejsceLokalu' : res.lokfiz_adSiedzNietypoweMiejsceLokalu.text, 
            'adSiedzKraj_Nazwa' : res.lokfiz_adSiedzKraj_Nazwa.text, 
            'adSiedzWojewodztwo_Nazwa' : res.lokfiz_adSiedzWojewodztwo_Nazwa.text, 
            'adSiedzPowiat_Nazwa' : res.lokfiz_adSiedzPowiat_Nazwa.text, 
            'adSiedzGmina_Nazwa' : res.lokfiz_adSiedzGmina_Nazwa.text, 
            'adSiedzMiejscowoscPoczty_Nazwa' : res.lokfiz_adSiedzMiejscowoscPoczty_Nazwa.text, 
            'adSiedzMiejscowosc_Nazwa' : res.lokfiz_adSiedzMiejscowosc_Nazwa.text, 
            'adSiedzUlica_Nazwa' : res.lokfiz_adSiedzUlica_Nazwa.text, 
            'dataPowstania' : res.lokfiz_dataPowstania.text,
            'dataWpisuDoREGON' : res.lokfiz_dataWpisuDoREGON.text, 
            'dataRozpoczeciaDzialalnosci' : res.lokfiz_dataRozpoczeciaDzialalnosci.text, 
            'dataZawieszeniaDzialalnosci' : res.lokfiz_dataZawieszeniaDzialalnosci.text, 
            'dataWznowieniaDzialalnosci' : res.lokfiz_dataWznowieniaDzialalnosci.text,
            'dataZaistnieniaZmiany' : res.lokfiz_dataZaistnieniaZmiany.text, 
            'dataZakonczeniaDzialalnosci' : res.lokfiz_dataZakonczeniaDzialalnosci.text, 
            'dataSkresleniazRegon' : res.lokfiz_dataSkresleniazRegon.text, 
            'formaFinansowania_Symbol' : res.lokfiz_formaFinansowania_Symbol.text, 
            'formaFinansowania_Nazwa' : res.lokfiz_formaFinansowania_Nazwa.text, 
            'dataWpisuDoRejestruEwidencji' : res.lokfiz_dataWpisuDoRejestruEwidencji.text, 
            'numerwRejestrzeEwidencji' : res.lokfiz_numerwRejestrzeEwidencji.text, 
            'organRejestrowy_Symbol' : res.lokfiz_organRejestrowy_Symbol.text, 
            'organRejestrowy_Nazwa' : res.lokfiz_organRejestrowy_Nazwa.text, 
            'rodzajRejestru_Symbol' : res.lokfiz_rodzajRejestru_Symbol.text, 
            'rodzajRejestru_Nazwa' : res.lokfiz_rodzajRejestru_Nazwa.text, 
            'dzialalnosci' : res.lokfiz_dzialalnosci 
        }
        return full_report_results
    except Exception as e:
        print 'blad poboru danych lokalnej osoby fizycznej - %s' %(e)

def pobor_danych_lokalna_prawna(proper_regon):
    try: 
        res = api.full_report(proper_regon, "DaneRaportLokalnaPrawnej")
        full_report_results = {
            'regon14' : res.lokpraw_regon14.text,
            'nazwa' : res.lokpraw_nazwa.text,
            'nip' : res.lokpraw_nip.text,
            'numerwRejestrzeEwidencji' : res.lokpraw_numerwRejestrzeEwidencji.text, 
            'adSiedzKraj_Symbol' : res.lokpraw_adSiedzKraj_Symbol.text, 
            'adSiedzWojewodztwo_Symbol' : res.lokpraw_adSiedzWojewodztwo_Symbol.text, 
            'adSiedzPowiat_Symbol' : res.lokpraw_adSiedzPowiat_Symbol.text, 
            'adSiedzGmina_Symbol' : res.lokpraw_adSiedzGmina_Symbol.text, 
            'adSiedzKodPocztowy' : res.lokpraw_adSiedzKodPocztowy.text, 
            'adSiedzMiejscowoscPoczty_Symbol' : res.lokpraw_adSiedzMiejscowoscPoczty_Symbol.text, 
            'adSiedzMiejscowosc_Symbol' : res.lokpraw_adSiedzMiejscowosc_Symbol.text, 
            'adSiedzUlica_Symbol' : res.lokpraw_adSiedzUlica_Symbol.text, 
            'adSiedzNumerNieruchomosci' : res.lokpraw_adSiedzNumerNieruchomosci.text,
            'adSiedzNumerLokalu' : res.lokpraw_adSiedzNumerLokalu.text, 
            'adSiedzNietypoweMiejsceLokalu' : res.lokpraw_adSiedzNietypoweMiejsceLokalu.text, 
            'adSiedzKraj_Nazwa' : res.lokpraw_adSiedzKraj_Nazwa.text, 
            'adSiedzWojewodztwo_Nazwa' : res.lokpraw_adSiedzWojewodztwo_Nazwa.text, 
            'adSiedzPowiat_Nazwa' : res.lokpraw_adSiedzPowiat_Nazwa.text, 
            'adSiedzGmina_Nazwa' : res.lokpraw_adSiedzGmina_Nazwa.text, 
            'adSiedzMiejscowoscPoczty_Nazwa' : res.lokpraw_adSiedzMiejscowoscPoczty_Nazwa.text, 
            'adSiedzMiejscowosc_Nazwa' : res.lokpraw_adSiedzMiejscowosc_Nazwa.text, 
            'adSiedzUlica_Nazwa' : res.lokpraw_adSiedzUlica_Nazwa.text, 
            'dataWpisuDoRejestruEwidencji' : res.lokpraw_dataWpisuDoRejestruEwidencji.text,            
            'dataPowstania' : res.lokpraw_dataPowstania.text,
            'dataRozpoczeciaDzialalnosci' : res.lokpraw_dataRozpoczeciaDzialalnosci.text, 
            'dataWpisuDoREGON' : res.lokpraw_dataWpisuDoREGON.text,  
            'dataZawieszeniaDzialalnosci' : res.lokpraw_dataZawieszeniaDzialalnosci.text, 
            'dataWznowieniaDzialalnosci' : res.lokpraw_dataWznowieniaDzialalnosci.text,
            'dataZaistnieniaZmiany' : res.lokpraw_dataZaistnieniaZmiany.text, 
            'dataZakonczeniaDzialalnosci' : res.lokpraw_dataZakonczeniaDzialalnosci.text, 
            'dataSkresleniazRegon' : res.lokpraw_dataSkresleniazRegon.text, 
            'podstawowaFormaPrawna_Symbol' : res.lokpraw_podstawowaFormaPrawna_Symbol.text, 
            'szczegolnaFormaPrawna_Symbol' : res.lokpraw_szczegolnaFormaPrawna_Symbol.text, 
            'formaFinansowania_Symbol' : res.lokpraw_formaFinansowania_Symbol.text, 
            'formaWlasnosci_Symbol' : res.lokpraw_formaWlasnosci_Symbol.text,
            'organZalozycielski_Symbol' : res.lokpraw_organZalozycielski_Symbol.text, 
            'organRejestrowy_Symbol' : res.lokpraw_organRejestrowy_Symbol.text, 
            'rodzajRejestruEwidencji_Symbol' : res.lokpraw_rodzajRejestruEwidencji_Symbol.text,
            'podstawowaFormaPrawna_Nazwa' : res.lokpraw_podstawowaFormaPrawna_Nazwa.text,
            'szczegolnaFormaPrawna_Nazwa' : res.lokpraw_szczegolnaFormaPrawna_Nazwa.text, 
            'formaFinansowania_Nazwa' : res.lokpraw_formaFinansowania_Nazwa.text, 
            'formaWlasnosci_Nazwa' : res.lokpraw_formaWlasnoci_Nazwa.text, 
            'organZalozycielski_Nazwa' : res.lokpraw_organZalozycielski_Nazwa.text,           
            'organRejestrowy_Nazwa' : res.lokpraw_organRejestrowy_Nazwa.text, 
            'rodzajRejestruEwidencji_Nazwa' : res.lokpraw_rodzajRejestruEwidencji_Nazwa.text,           
            'dzialalnosci' : res.lokpraw_dzialalnosci                      
        }
        return full_report_results
    except Exception as e:
        print (e)

# PETLA DO pobierania danych

# otwarcie pliku z danymi operacyjnymi (op_data.pkl) w formacie pickle. Plik bedzie mial w sobie slownik z nastepujacymi kluczami: 
# last_regon - ostatnio pobrany regon
# ???


def save_results_to_file(prefix, suffix, results_to_save):
    with open('D:\\REGON\\%s_prefix_cz_%s.pkl' %(prefix, suffix), 'wb') as f:
        pickle.dump(results_to_save, f)
    print "Zapisuje do pliku \'%s_prefix_cz_%s.pkl\'" %(prefix,suffix)
    
def update_op_data_to_file(op_data):
    with open('op_data.pkl', 'wb') as f:
        pickle.dump(op_data, f)

def check_if_need_to_save(liczba_petli, n):
    if liczba_petli%n == 0:
        return True
    else:
        return False

def check_if_need_to_change_prefix(licznik_pustych_regonow, n):
    if licznik_pustych_regonow >= n: 
        return True
    else:
        return False 

#przygotowanie startu programu
with open('op_data.pkl', 'rb') as f: # do zmiany op_data
    op_data = pickle.load(f)

try:
    prefix_index = op_data['prefix_index']
    last_regon = op_data['last_regon'] # wyciagniecie ostatnio sprawdzanego regonu
    prefix = op_data['prefix'][prefix_index]
    suffix = op_data['suffix']
except: 
    last_regon = 1
    prefix = '00'
    prefix_index = 0    
    suffix = 0

regon_number = last_regon
results_to_save = dict()
program_runs = True
liczba_petli = 1
licznik_pustych_regonow = 0
raport_pkd = []
full_report = {}
liczba_rekordow_w_pliku = 1000

print "Rozpoczynam program.\nPrefix - %s\nRegon - %s\nSuffix - %s" %(prefix, last_regon, suffix)
time.sleep(5)

while program_runs: 
    
    try:
        time.sleep(3)
  # sprawdzenie czy nie nalezy zmienic prefixu
        
        print "Liczba pustych regonow = %s" %(licznik_pustych_regonow) 
        if check_if_need_to_change_prefix(licznik_pustych_regonow, 100):
            prefix_index += 1
            regon_number = 0
            try:
                prefix = op_data['prefix'][prefix_index]
            except Exception as e:
                print "Blad w zmianie prefixu - prawdopodobny koniec programu - %s" %(e)
                break
            op_data['prefix_index'] = prefix_index
            op_data['last_regon'] = 0
            licznik_pustych_regonow = 0
            suffix = 0
            update_op_data_to_file(op_data)
            save_results_to_file(prefix,'resztowka', results_to_save)
            
            # chwilowo wykomentowalem ponizszy fragment kodu - dzieki temu program bedzie chodzil przez cala noc, a i tak bedzie mozna go zatrzymac.
            
            #continue_prompt = raw_input('Czy chcesz rozpoczac pobieranie regonow z nastepnego prefixu - %s? T/N' %(prefix))
            #if continue_prompt == 'N':
            #    save_results_to_file(prefix,'resztowka', results_to_save)
            #    break
            #elif continue_prompt == 'T': 
            #    pass
        else: 
            pass

    # warunek zapisania nowego pliku na dysk oraz reset slownika z wynikami
    
        if check_if_need_to_save(liczba_petli, liczba_rekordow_w_pliku): 
            save_results_to_file(prefix, suffix, results_to_save) 
            update_op_data_to_file(op_data)
            results_to_save = {}
            suffix += 1
            op_data['suffix'] = suffix
    
    # przerobienie regonu na dobry 9 cyfrowy string

        proper_regon = chcksm_counter(''.join([prefix,regon_prep(regon_number)]))
        print proper_regon # wydruk tylko dla upewnienia sie ze dziala system
    
    # pobranie podstawowego raportu
    
        try: 
            basic_report = pobor_danych_raport_podstawowy(proper_regon) 
            licznik_pustych_regonow = 0 # udane pobranie raportu (wystarczy podstawowego) skutkuje resetem licznika pustych regonow
        except Exception as e: 
            print "Blad api - %s" %(e)
            regon_number += 1
            licznik_pustych_regonow += 1 
            liczba_petli += 1
            continue
            
    # pobor pelnego raportu na podstawie typu dzialalnosci
    
        try:
            if basic_report['typ'] == "F": 
                full_report = pobor_danych_osoby_fizycznej(proper_regon)
            elif basic_report['typ'] == "P":
                full_report = pobor_danych_osoby_prawnej(proper_regon)
                raport_pkd = pobor_danych_pkd(proper_regon)
            elif basic_report['typ'] == "LF":
                full_report = pobor_danych_lokalna_fizyczna(proper_regon)       
            elif basic_report['typ'] == "LP":
                full_report = pobor_danych_lokalna_prawna(proper_regon)
                raport_pkd = pobor_danych_pkd(proper_regon)
            else:
                print "nieprawidlowy typ raportu"
        except Exception as e:
            print (e)

    # zlozenie slownika zawierajacego wszystkie potrzebne dane, dodanie go do slownika glownego results_to_save

        reports = {'basic': basic_report, 'full': full_report, 'pkd': raport_pkd}
        results_to_save.update({proper_regon: reports})
        
    # update numeratorow i nadpisanie zmiennych okresowych
    
        liczba_petli += 1
        regon_number += 1
        op_data['last_regon'] = regon_number
        
    
    # Zmiana polaczenia - na wypadek wszelki

        if (liczba_petli % 5000)==0:
            api = REGONAPI('https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc') # adres serwera public uslugi BIR
            api.login('a0a397f69f7e46d88afb') # klucz 4cf do logowania sie do bazy regon

    except KeyboardInterrupt:
        print 'konczymy na dzis'
        save_results_to_file(prefix,'koncowka', results_to_save)
        update_op_data_to_file(op_data)
        sys.exit()
