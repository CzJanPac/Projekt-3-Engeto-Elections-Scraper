"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Jan Páč
email: czjanpac@gmail.com
"""

from bs4 import BeautifulSoup as bs
from requests import get
import sys

# Stránka odesílá 200 i při prázdné nebo neplatné stránce
def stahni_stranku(odkaz):
    odpoved = get(odkaz)
    if odpoved.status_code != 200:
        sys.exit("Chyba při načítání stránky")
    return odpoved.text

def parsuj_html(html_text):
    return bs(html_text, "html.parser")

# Zvážit způsob kontoroly zda stránka obsahuje správně data
def over_data(soup): 
    if not soup.find("table"):
        sys.exit("Pravděpodobně chybný odkaz, stránka neobsahuje volební data")

def ziskej_parsovany_odkaz(odkaz=None):
    if odkaz is None:
        odkaz = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    html_text = stahni_stranku(odkaz)
    soup = parsuj_html(html_text)
    over_data(soup)
    return soup

def najdi_volebni_data(odkaz):
    pass

def zapis_data_do_csv(soubor):
    pass

def main():
    pass

# tady budem pokracovat

print(ziskej_parsovany_odkaz())