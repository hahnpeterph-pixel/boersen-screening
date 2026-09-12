# Lange Kurshistorie - laeuft NUR auf Zuruf.
#
# Bewusst kein Zeitplan. Das Skript zieht sieben Jahre Tagesdaten fuer rund
# 218 Werte und braucht dafuer 10 bis 20 Minuten. Taeglich waere das
# verschwendet: die Auswertung, fuer die es gedacht ist - was folgt auf
# Tage mit hohem Anteil gefallener Werte - aendert sich durch einen
# einzelnen neuen Handelstag nicht messbar.
#
# Sinnvoll ist ein Lauf alle paar Monate oder wenn eine konkrete Frage zu
# Marktphasen aufkommt. Ergebnis sind zwei Dateien in docs/:
#   markthistorie.csv.gz - Tagesschluesse, Zeilen Ticker, Spalten Datum
#   marktbreite.md       - fertige Auswertung zum Lesen
name: Markthistorie

on:
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: markthistorie
  cancel-in-progress: false

jobs:
  historie:
    runs-on: ubuntu-latest
    # Grosszuegig, aber nicht unbegrenzt: haengt Yahoo, soll der Lauf
    # abbrechen statt eine Stunde Laufzeit zu verbrennen.
    timeout-minutes: 45

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Abhaengigkeiten installieren
        run: |
          python -m pip install --upgrade pip
          pip install yfinance pandas numpy requests

      - name: Markthistorie ausfuehren
        env:
          TWELVEDATA_API_KEY: ${{ secrets.TWELVEDATA_API_KEY }}
        run: python markthistorie.py

      - name: Ergebnis pruefen
        run: |
          python - <<'PY'
          import gzip, os, sys
          import pandas as pd

          pfad = "docs/markthistorie.csv.gz"
          if not os.path.exists(pfad):
              sys.exit("markthistorie.csv.gz wurde nicht geschrieben.")

          with gzip.open(pfad, "rt", encoding="utf-8") as f:
              d = pd.read_csv(f).set_index("ticker")

          tage = list(d.columns)
          print(f"{len(d)} Ticker, {len(tage)} Handelstage "
                f"({tage[0]} bis {tage[-1]})")

          # Eine lange Historie ist nur brauchbar, wenn sie auch lang IST.
          # Sieben Jahre sind rund 1.760 Handelstage; unter 1.200 stimmt
          # etwas nicht - dann hat Yahoo gekuerzt geliefert.
          if len(tage) < 1200:
              sys.exit(f"Nur {len(tage)} Handelstage - erwartet werden ueber "
                       "1.200 fuer sieben Jahre. Quelle hat gekuerzt.")

          # Werte, die im JUENGSTEN Jahr fast leer sind, waeren fuer jede
          # Marktbreite-Rechnung wertlos. Aeltere Luecken sind dagegen
          # normal: Neuemissionen notierten frueher schlicht noch nicht.
          jung = tage[-250:]
          duenn = [t for t in d.index if d.loc[t, jung].notna().sum() < 200]
          print(f"Werte mit weniger als 200 Kursen im letzten Jahr: {len(duenn)}")
          if duenn:
              for t in duenn[:20]:
                  print(f"  {t}: {int(d.loc[t, jung].notna().sum())} von 250")
          if len(duenn) > 10:
              sys.exit(f"{len(duenn)} Werte sind im letzten Jahr zu duenn "
                       "besetzt - die Marktbreite waere verzerrt.")
          PY

      - name: Ergebnis speichern
        run: |
          git config user.name "screening-bot"
          git config user.email "actions@github.com"
          git add docs/markthistorie.csv.gz docs/marktbreite.md
          if git diff --staged --quiet; then
            echo "Nichts geaendert."
            exit 0
          fi
          git commit -m "Markthistorie $(date -u +%Y-%m-%d)"
          # Der Push scheitert, sobald main sich seit dem Checkout bewegt
          # hat. Bei diesem Workflow ist das besonders wahrscheinlich: er
          # laeuft 10 bis 20 Minuten, und in dieser Zeit kann das
          # Screening dazwischenkommen. Genau so ist es am 12.09.2026
          # passiert - der Lauf war fertig gerechnet, der Commit lag
          # lokal vor, und der Push wurde mit "fetch first" abgewiesen.
          # Deshalb vor jedem Versuch neu aufsetzen und bis zu drei
          # Anlaeufe nehmen, statt 20 Minuten Rechenzeit zu verwerfen.
          # Identisch zu screening.yml, historie.yml und den uebrigen.
          for versuch in 1 2 3; do
            if git pull --rebase --autostash origin main && git push origin main; then
              echo "Gespeichert im Versuch $versuch."
              exit 0
            fi
            echo "Versuch $versuch fehlgeschlagen, neuer Anlauf in 10 Sekunden ..."
            sleep 10
          done
          echo "Push nach drei Versuchen fehlgeschlagen."
          exit 1
