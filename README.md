# Zeittabelle für Arbeitszeitdaten erstellen

Python-Skript zur Erstellung formatierter Excel-Zeittabellen aus Arbeitszeitdaten mit automatischer deutscher Feiertagsintegration.

## 🚀 Schnellstart (Empfohlen: Web-App nutzen)

### Web-App starten

1. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

2. Web-App starten:
```bash
streamlit run web_app.py
```

3. Browser öffnen und die Anweisungen in der App folgen, um deine Zeitdaten zu exportieren.

### Fallback: Command Line (nur wenn Web-App nicht funktioniert)

Wenn die Web-App nicht funktioniert, kannst du das Skript über die Kommandozeile ausführen. Siehe Abschnitt "🔧 Command Line Fallback" am Ende dieser README.

## 📋 Vorbereitung

Bevor das Skript ausgeführt wird, müssen die folgenden Schritte durchgeführt werden:

### 1. Zeitdaten anfordern
Sende eine E-Mail mit dem Betreff **"STATUS"** um Arbeitszeitdaten anzufordern.

### 2. Daten in JSON-Format übertragen
Übertrage die erhaltenen Zeitdaten in das JSON-Format. Die Daten müssen wie folgt aussehen:

**Dies ist ein Tag, deine Daten haben wahrscheinlich mehrere Tage.**
```json
[
  {
    "date": "2026-01-06",
    "weekday": "Dienstag",
    "status": "A",
    "status_label": "Anwesend",
    "start_time": "08:00",
    "end_time": "16:30",
    "duration_minutes": 480,
    "duration": "08:00",
    "punch_count": 2,
    "break_minutes": 30,
    "fallback_end_applied": false
  }
]
```

## 📋 Anforderungen

### Benötigte Pakete
```bash
pip install openpyxl requests streamlit
```
### alternativ

```bash
python pip install -r requirements.txt
```
__________
### Erforderliche Verzeichnisse / Dateien
```
Zeitnachweis/
            ├── templates/
            │           └── template.xlsx
            └── scripts/
                        ├── create_basic_headers.py
                        ├── create_work_day_from_dict.py
                        ├── export_with_holidays.py
                        ├── fetch_holidays.py
                        ├── fill_holidays.py
                        ├── find_template_sheet.py
                        ├── get_file_extension.py
                        ├── get_german_holidays.py
                        ├── get_status_label.py
                        ├── handle_validation_error.py
                        ├── load_json_data.py
                        ├── load_work_data.py
                        ├── process_work_day_data.py
                        ├── start_time_export.py
                        ├── update_sheet_dates.py
                        ├── validate_file_path.py
                        ├── validate_paths.py
                        ├── write_work_data.py
                        └── WorkDay.py

```

## 🎯 Statuscodes

| Code | 
|------|
| ANWESEND |
| URLAUB |
| KRANK |
| KIND_KRANK | 
| SCHULE | 
| FREI_FEIERTAG | 
| FEIERTAG_AUTO | 
| ENTSCHULDIGT | 
| PRAKTIKUM_NICHT_BEGONNEN | 
| FERTIG | 
| UNBEKANNT | 
| KEIN_EINTRAG | 

## 🇩🇪 Bundeslandcodes

| Code | Bundesland |
|------|------------|
| BY | Bayern |
| BW | Baden-Württemberg |
| BE | Berlin |
| BB | Brandenburg |
| HB | Bremen |
| HH | Hamburg |
| HE | Hessen |
| MV | Mecklenburg-Vorpommern |
| NI | Niedersachsen |
| NW | Nordrhein-Westfalen |
| RP | Rheinland-Pfalz |
| SL | Saarland |
| SN | Sachsen |
| ST | Sachsen-Anhalt |
| SH | Schleswig-Holstein |
| TH | Thüringen |

## 📁 Ausgabe

Erstellt separate Excel-Dateien für jeden Monat:
```
ZEITNACHWEIS_2026_1.xlsx  (Januar 2026)
ZEITNACHWEIS_2026_2.xlsx  (Februar 2026)
...
```

## 🔧 Command Line Fallback

### Nach Excel exportieren
```bash
# Standard (Niedersachsen), prompts for pasted JSON
python start_time_export.py

# Bestimmtes Bundesland, prompts for pasted JSON
python start_time_export.py BY

# Mit benutzerdefinierter Datei (optional)
python start_time_export.py NI /path/to/my_data.json
```

1. **Zum Ordner navigieren:**
```bash
cd ./Zeitnachweis/scripts
```

2. **Skript ausführen:**
```bash
python start_time_export.py [state_code] [data_file] [--output-dir DIR]
```

Wenn keine Datendatei angegeben wird, fordert das Skript zur Eingabe der JSON-Daten auf.

- `state_code`: Bundesland für Feiertage (optional, Standard: NI)
- `data_file`: Pfad zur JSON-Datendatei (optional, wenn nicht angegeben, Eingabeaufforderung)
- `--output-dir`: Output-Verzeichnis (optional, Standard: ../output)
