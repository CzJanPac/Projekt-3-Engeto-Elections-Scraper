from bs4 import BeautifulSoup as bs
from requests import get
import sys
import csv

def stahni_stranku(odkaz):
    odpoved = get(odkaz)
    if odpoved.status_code != 200:
        sys.exit("Chyba: nepodařilo se načíst stránku, zkontrolujte správnost URL")
    return odpoved.text

def parsuj_html(html_text):
    return bs(html_text, "html.parser")

def ziskej_parsovany_odkaz(odkaz):
    print(f"Stahuji data z vybraného URL: {odkaz}")
    print(f"Stahování může chvíli trvat...")
    html_text = stahni_stranku(odkaz)
    soup = parsuj_html(html_text)
    return soup

def ziskej_kody_a_nazvy_obci(soup):
    """
    Najde v HTML všechny obce a ke každé zjistí její kód, název a odkaz na podstránku.
    Vrací seznam trojic: (kód obce, název obce, URL podstránky).
    """
    vysledky = []
    zaklad_url = "https://www.volby.cz/pls/ps2017nss/"
    cisla = soup.find_all("td", class_="cislo")
    nazvy = soup.find_all("td", class_="overflow_name")

    for cislo, nazev in zip(cisla, nazvy):
        odkaz = cislo.find("a")
        if odkaz:
            kod = odkaz.text.strip()
            nazev_obce = nazev.text.strip()
            href = zaklad_url + odkaz["href"]
            vysledky.append((kod, nazev_obce, href))
    return vysledky

def ziskej_data_z_podstranky(soup):
    """
    Načte z podstránky údaje o počtu voličů, obálek a platných hlasů.
    Také získá (ve dvou tabulkách) všechny strany a kolik hlasů dostaly.
    """
    data = soup.find_all("td", class_="cislo", headers=["sa2", "sa3", "sa6"])

    if len(data) < 3:
        sys.exit("Chyba: Nepodařilo se najít všechny údaje (voliči, obálky, platné hlasy) na stránce s výsledky. Zkontrolujte, zda je URL správná.")

    volici = data[0].text.strip().replace("\xa0", "")
    obalky = data[1].text.strip().replace("\xa0", "")
    platne = data[2].text.strip().replace("\xa0", "")

    strany_data = []
    strany_nazvy = []

    strany_radky = soup.find_all("tr")

    # První tabulka stran (t1sa)
    for radek in strany_radky:
        nazev_td = radek.find("td", class_="overflow_name", headers="t1sa1 t1sb2")
        hlasy_td = radek.find("td", class_="cislo", headers="t1sa2 t1sb3")
        if nazev_td and hlasy_td:
            nazev = nazev_td.text.strip()
            hlasu = hlasy_td.text.strip().replace("\xa0", "")
            strany_nazvy.append(nazev)
            strany_data.append(hlasu)

    # Druhá tabulka stran (t2sa)
    for radek in strany_radky:
        nazev_td = radek.find("td", class_="overflow_name", headers="t2sa1 t2sb2")
        hlasy_td = radek.find("td", class_="cislo", headers="t2sa2 t2sb3")
        if nazev_td and hlasy_td:
            nazev = nazev_td.text.strip()
            hlasu = hlasy_td.text.strip().replace("\xa0", "")
            strany_nazvy.append(nazev)
            strany_data.append(hlasu)

    return volici, obalky, platne, strany_data, strany_nazvy

def zpracuj_vsechny_obce(soup):
    """
    Projde všechny obce ze vstupní stránky a jejich podstránky,
    ke každé obci stáhne volební data.

    Vrací dvě věci:
    - seznam názvů všech stran z první obce (do hlavičky v CSV)
    - seznam řádků s výsledky pro každou obec
    """
    obce = ziskej_kody_a_nazvy_obci(soup)
    vysledky = []
    hlavicky_stran = []

    for i, (kod, nazev, odkaz) in enumerate(obce):
        html = stahni_stranku(odkaz)
        podstranka_soup = parsuj_html(html)
        volici, obalky, platne, hlasy, nazvy_stran = ziskej_data_z_podstranky(podstranka_soup)

        if i == 0:
            hlavicky_stran = nazvy_stran

        zaznam = [kod, nazev, volici, obalky, platne] + hlasy
        vysledky.append(zaznam)

    return vysledky, hlavicky_stran

def zapis_do_csv(data, soubor, hlavicky_stran):
    with open(soubor, 'w', newline='', encoding="utf-8") as csvfile:
        print(f"Ukládán do souboru: {soubor}")
        writer = csv.writer(csvfile)
        hlavicka = ["Kód obce", "Název obce", "Voličů v seznamu", "Vydané obálky", "Platné hlasy"] + hlavicky_stran
        writer.writerow(hlavicka)
        writer.writerows(data)

def over_argumenty(args):
    """
    Zkontroluje, jestli uživatel zadal správné argumenty při spuštění programu.
    Pokud argumenty chybí nebo jsou ve špatném formátu, program se ukončí s chybou.
    Program očekává 2 argumenty:
    1. URL adresa se stránkou s výsledky voleb.
    2. Název výstupního CSV souboru.
    """
    if len(args) != 3:
        print(f"Použití: python {args[0]} <URL> <vystupni_soubor.csv>")
        sys.exit(1)

    url = args[1]
    soubor = args[2]

    if not url.startswith("http"):
        print("Chyba: první argument musí být platná URL začínající 'http' nebo 'https'")
        sys.exit(1)

    if not soubor.endswith(".csv"):
        print("Chyba: druhý argument musí být název výstupního souboru končící '.csv'")
        sys.exit(1)

    return url, soubor

def main():
    """
    Hlavní funkce programu:
    1. Získá a ověří vstupní argumenty (URL a název výstupního souboru).
    2. Načte stránku se seznamem obcí.
    3. Načte a zpracuje podstránky všech obcí s volebními výsledky.
    4. Uloží výsledky do CSV souboru.
    5. Informuje o ukončení programu.
    """
    url, csvfile = over_argumenty(sys.argv)
    soup = ziskej_parsovany_odkaz(url)
    vysledky, hlavicky_stran = zpracuj_vsechny_obce(soup)
    zapis_do_csv(vysledky, csvfile, hlavicky_stran)
    print(f"Data byla uložena ({len(vysledky)} obcí).")
    print("Hotovo, ukončuji ELECTION SCRAPER.")

# python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102" vysledky_frydek_mistek.csv
# Kód obce,Název obce,Voličů v seznamu,Vydané obálky,Platné hlasy,Občanská demokratická strana, ...
# 598011,Baška,3093,2065,2053,175,1,1,124,1,49,192,21,12,21,1,0,216,0,0,44,665,2,9,194,1,16,7,3,293,5
# 598020,Bílá,285,178,178,19,0,0,14,0,10,21,3,1,0,1,0,12,1,0,3,52,0,0,15,0,3,0,0,23,0
# 511633,Bocanovice,358,197,197,20,0,0,32,0,3,13,3,1,0,0,0,18,0,1,1,45,0,0,43,0,0,0,0,17,0

if __name__ == "__main__":
    main()