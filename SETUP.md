# Börsen-Screening – Einrichtung Schritt für Schritt

Ziel: Jeden Werktagmorgen liegt ein Report bereit, der **nur Veränderungen** in drei
Ranglisten zeigt (Turnaround, Momentum, Value/Qualität) – lesbar auf dem Handy im Claude-Chat.

Aufwand einmalig: ca. 30 Minuten am PC. Danach läuft es ohne dich.
Laufende Kosten: 0 €.

---

## Teil A – Der Motor bei GitHub (einmalig, am PC)

### A1. Konto anlegen
[github.com](https://github.com) → **Sign up**. Kostenlos, E-Mail-Bestätigung genügt.

### A2. Repository erstellen
Oben rechts **+** → **New repository**
- Name: `boersen-screening`
- Sichtbarkeit: **Public**
  (Wichtig: Nur bei „Public" kann Claude die Report-Datei später abrufen.
  Im Repo liegen nur Kursauswertungen, nichts Persönliches.)
- Haken bei **Add a README file**
- **Create repository**

### A3. Dateien hochladen
Im Repo: **Add file** → **Upload files** → diese vier Dateien hineinziehen:

```
screener.py
universe.json
requirements.txt
SETUP.md          (optional, als Nachschlagewerk)
```

→ unten **Commit changes**.

### A4. Die Workflow-Datei anlegen
Die muss in einen Unterordner, deshalb anders:

**Add file** → **Create new file** → in das Namensfeld exakt eintragen:

```
.github/workflows/screening.yml
```

(Sobald du den Schrägstrich tippst, legt GitHub die Ordner automatisch an.)
Dann den Inhalt von `screening.yml` hineinkopieren → **Commit changes**.

### A5. Schreibrechte für den Automaten freischalten
**Settings** (im Repo) → links **Actions** → **General** → ganz unten
**Workflow permissions** → **Read and write permissions** auswählen → **Save**.

Ohne diesen Schritt kann der Lauf seine Ergebnisse nicht speichern und der
Vortagsvergleich funktioniert nie.

### A6. Ersten Lauf manuell starten
Tab **Actions** → links **Boersen-Screening** → rechts **Run workflow** → **Run workflow**.

Der erste Lauf dauert **5–10 Minuten** (er holt einmalig alle Fundamentaldaten).
Danach 1–2 Minuten pro Tag.

Grüner Haken? Dann liegt jetzt im Repo:
- `docs/report.md` – der Report (heute noch die komplette Baseline)
- `state/state.json` – der Zustand für den Vergleich morgen

### A7. Die URL für Claude kopieren
Öffne `docs/report.md` im Repo → Knopf **Raw** → die Adresse aus der Browserzeile kopieren.
Sie sieht so aus:

```
https://raw.githubusercontent.com/DEINNAME/boersen-screening/main/docs/report.md
```

**Diese URL brauchst du gleich.**

---

## Teil B – Der Morgen-Report im Claude-Chat

Geplante Aufgaben laufen in **Claude Cowork** und werden in der Cloud ausgeführt –
dein PC darf also aus sein, und du liest das Ergebnis auf dem Handy.
(Verfügbar in den kostenpflichtigen Plänen.)

1. In Cowork links in der Seitenleiste **Scheduled** → **New task**
   (oder in einer laufenden Unterhaltung `/schedule` eintippen).
2. Als Prompt die Vorlage unten einsetzen, `DEINNAME` ersetzen.
3. Zeitplan: **Weekdays, 07:00 Uhr** (der GitHub-Lauf ist um 06:00 fertig).
4. Vorher einmal manuell laufen lassen und prüfen, ob der Abruf klappt.

### Prompt-Vorlage

```
Rufe https://raw.githubusercontent.com/DEINNAME/boersen-screening/main/docs/report.md ab.

Gib mir den Inhalt als kurzen Morgen-Report:
- Wenn dort "Keine Veraenderungen" steht: sage genau das in einem Satz, sonst nichts.
- Sonst: liste die Neuzugänge, Abgänge und Rangsprünge auf und ergänze
  bei jedem Neuzugang zwei Sätze Einordnung – was das Unternehmen macht
  und was zuletzt passiert sein könnte (kurz im Web nachsehen).
- Nenne Quartalstermine, falls im Report Warnungen stehen.
- Keine Kauf- oder Verkaufsempfehlungen, nur Einordnung.
- Maximal 15 Zeilen.
```

---

## Teil C – Was das Skript rechnet

**Drei getrennte Ranglisten, je Top 15, je 0–100 Punkte:**

| | Turnaround | Momentum | Value/Qualität |
|---|---|---|---|
| Kern (25 P.) | Drawdown 30–55 % vom ATH | < 10 % unter ATH | KGV/PEG, Cashflow |
| Struktur (20 P.) | höheres Tief | rel. Stärke vs. Index | Marge, Umsatzwachstum |
| Bestätigung | über 50-Tage-Linie, RSI dreht | über 50 + 200-Tage-Linie | Verschuldung, ROE |
| Volumen (10 P.) | Anstiege auf höherem Umsatz | dito | – |

**Ausschlussfilter** (fliegt aus allen Listen):
- fallender Umsatz bei Verschuldung > 150 % des Eigenkapitals
- 200-Tage-Linie fällt steiler als 2 % im Monat
- mehr als 80 % unter Allzeithoch
- negativer Cashflow bei gleichzeitigem Verlust

**Gemeldet wird nur:** neu in den Top 15, raus aus den Top 15,
Rangsprung ≥ 5 Plätze, Quartalszahlen in ≤ 5 Tagen.

---

## Teil D – Grenzen, ehrlich benannt

- **Fundamentaldaten sind die Schwachstelle.** Yahoo liefert KGV, Margen und
  Verschuldung lückenhaft und teils veraltet. Turnaround und Momentum sind
  belastbar (reine Kursdaten), die Value-Liste ist eine grobe Vorsortierung.
  Wenn dir die wichtig wird: Financial Modeling Prep oder EOD Historical Data
  (je ca. 20 €/Monat) und die Funktion `get_fundamentals` umstellen.
- **Allzeithoch = 10-Jahres-Hoch.** Für ältere Werte wie Siemens oder Coca-Cola
  liegt das echte ATH teils weiter zurück. In `HISTORY_PERIOD` änderbar.
- **yfinance ist inoffiziell.** Fällt gelegentlich für ein, zwei Tage aus;
  dann greift der Stooq-Fallback. Bei Dauerproblemen: `pip install -U yfinance`
  in der `requirements.txt` anstoßen (Versionsnummer erhöhen).
- **Indexzusammensetzung veraltet.** `universe.json` einmal im Quartal prüfen,
  besonders nach den Umstellungen im Dezember (NASDAQ-100) und September (DAX).
- **Kein Backtest.** Die Punktgewichtungen sind plausibel, aber nicht optimiert.
  Nach vier Wochen Mitlesen wirst du sehen, welche Signale bei dir etwas taugen –
  die Gewichte stehen alle oben in den `score_*`-Funktionen und sind leicht änderbar.
- Das Ganze sortiert Kennzahlen. Es ist keine Anlageberatung und ersetzt keine
  eigene Prüfung des Einzelfalls.

---

## Teil E – Wartung

| Wann | Was |
|---|---|
| wöchentlich | Report kurz querlesen, auffällige Werte selbst nachrecherchieren |
| monatlich | Actions-Tab auf rote Läufe prüfen |
| quartalsweise | `universe.json` gegen die aktuellen Indexlisten abgleichen |
| bei Bedarf | Punktgewichte in `screener.py` anpassen |

Falls GitHub die geplanten Läufe nach längerer Repo-Inaktivität pausiert:
Tab **Actions** → Hinweisbanner → **Enable workflow**.
