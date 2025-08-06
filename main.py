from bs4 import BeautifulSoup as bs
from requests import get
import sys
import csv

def stahni_stranku(odkaz):
    odpoved = get(odkaz)
    if odpoved.status_code != 200:
        sys.exit("Chyba při načítání stránky.")
    return odpoved.text

def parsuj_html(html_text):
    return bs(html_text, "html.parser")

def ziskej_parsovany_odkaz(odkaz):
    print(f"STAHUJI DATA Z VYBRANÉHO URL: {odkaz}")
    html_text = stahni_stranku(odkaz)
    soup = parsuj_html(html_text)
    return soup

def ziskej_kody_a_nazvy_obci(soup):
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
    data = soup.find_all("td", class_="cislo", headers=["sa2", "sa3", "sa6"])
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
        print(f"UKLÁDÁM DO SOUBORU: {soubor}")
        writer = csv.writer(csvfile)
        hlavicka = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"] + hlavicky_stran
        writer.writerow(hlavicka)
        writer.writerows(data)

def main():
    if len(sys.argv) != 3:
        print(f"Použití: python {sys.argv[0]} <URL> <vystupni_soubor.csv>")
        sys.exit(1)

    url = sys.argv[1]
    csvfile = sys.argv[2]

    # Kontrola, že první argument je URL a druhý CSV soubor
    if not url.startswith("http") or not csvfile.endswith(".csv"):
        print("Chyba: argumenty nejsou ve správném pořadí nebo formátu.")
        print(f"Správné použití: python {sys.argv[0]} <URL> <vystupni_soubor.csv>")
        sys.exit(1)

    soup = ziskej_parsovany_odkaz(url)
    vysledky, hlavicky_stran = zpracuj_vsechny_obce(soup)
    zapis_do_csv(vysledky, csvfile, hlavicky_stran)
    print("UKONČUJI ELECTION SCRAPER")

if __name__ == "__main__":
    main()