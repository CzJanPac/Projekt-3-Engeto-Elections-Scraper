<h1>Election Scraper</h1>
<p>3. projekt - Engeto Python Akademie</p>

<h2>Popis projektu</h2>
<p>Tento projekt slouží ke stažení výsledků parlamentních voleb z webu volby.cz pro vybraný okres.<br>
Program stáhne seznam všech obcí v daném okrese, pro každou obec načte podrobné volební výsledky a uloží je do CSV souboru.</p>

<h2>Instalace knihoven</h2>
<p>Knihovny potřebné pro běh programu jsou uvedeny v souboru <code>requirements.txt</code>.<br>
Před spuštěním programu je nainstalujte pomocí příkazu:</p>
<pre><code>pip install -r requirements.txt</code></pre>

<h2>Spuštění programu</h2>
<p>Program se spouští příkazem:</p>
<pre><code>python main.py &lt;URL&gt; &lt;výstupní_soubor.csv&gt;</code></pre>

<h3>Argumenty</h3>
<ul>
  <li><strong>URL</strong> – odkaz na stránku s výsledky voleb pro vybraný okres (např. seznam obcí a odkazů na jejich detailní výsledky).</li>
  <li><strong>výstupní_soubor.csv</strong> – název CSV souboru, do kterého se výsledky uloží (musí končit <code>.csv</code>).</li>
</ul>

<h2>Ukázka projektu</h2>

<h3>Příklad spuštění programu s argumenty</h3>
<pre><code>python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&amp;xkraj=14&amp;xnumnuts=8102" vysledky_frydek_mistek.csv</code></pre>

<h3>Průběh stahování</h3>
<pre>
Stahuji data z vybraného URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&amp;xkraj=14&amp;xnumnuts=8102
Stahování může chvíli trvat...
Ukládán do souboru: vysledky_frydek_mistek.csv
Data byla uložena (XX obcí).
Hotovo, ukončuji ELECTION SCRAPER.
</pre>
<p><em>Poznámka: Počet zpracovaných obcí závisí na zadané URL.</em></p>

<h3>Částečný výstup (část CSV souboru)</h3>
<pre>
Kód obce,Název obce,Voličů v seznamu,Vydané obálky,Platné hlasy,Občanská demokratická strana,...
598011,Baška,3093,2065,2053,175,1,1,124,1,49,192,21,12,21,1,0,216,0,0,44,665,2,9,194,1,16,7,3,293,5
598020,Bílá,285,178,178,19,0,0,14,0,10,21,3,1,0,1,0,12,1,0,3,52,0,0,15,0,3,0,0,23,0
511633,Bocanovice,358,197,197,20,0,0,32,0,3,13,3,1,0,0,0,18,0,1,1,45,0,0,43,0,0,0,0,17,0
</pre>
