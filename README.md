# Zeittabelle für Arbeitszeitdaten erstellen

Eine Streamlit Python-App zur Erstellung formatierter Excel-Zeittabellen aus Arbeitszeitdaten mit automatischer deutscher Feiertagsintegration.

Check it out: https://untimely.streamlit.app/

## 🚀 Schnellstart (Empfohlen: Web-App nutzen)

### Web-App starten

Du kannst die App entweder online nutzen oder lokal installieren.

**Option 1: Online-Version**

Gehe zu: https://zeitnachweis-export.streamlit.app/

**Option 2: Lokale Version**

1. Dieses Repository klonen:
```bash
git clone https://github.com/T334GE/Zeitnachweis-Web-App.git
cd Zeitnachweis-Web-App
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Web-App starten:
```bash
streamlit run web_app.py
```

4. Browser öffnen und die Anweisungen in der App folgen, um deine Zeitdaten zu exportieren.

### Fallback: Command Line (nur wenn Web-App nicht funktioniert)

Wenn die Web-App nicht funktioniert, kannst du das Skript über die Kommandozeile ausführen. Siehe Abschnitt "🔧 Command Line Fallback" am Ende dieser README.

## 📋 Vorbereitung

Bevor das Skript ausgeführt wird, müssen die folgenden Schritte durchgeführt werden:

### 1. Zeitdaten anfordern
Sende eine E-Mail mit dem Betreff **"STATUS"** um Arbeitszeitdaten anzufordern.

### 2. JSON-Daten aus der E-Mail kopieren
Unten auf der erhaltenen E-Mail befinden sich die JSON-Daten. Kopiere diese vollständig.

### 3. Daten verwenden
Es gibt zwei Möglichkeiten, die JSON-Daten zu verwenden:

- **Empfohlen:** Übertrage die kopierten JSON-Daten in eine `data.json` Datei (z.B. mit einem Texteditor speichern). Diese Datei kann dann in der Web-App hochgeladen werden.
- **Alternativ:** Füge die JSON-Daten direkt in die Web-App ein (über die "JSON einfügen" Option).

Für die Kommandozeile: Wenn keine Datendatei angegeben wird, fordert das Skript zur direkten Eingabe der JSON-Daten auf.

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
# Standard, prompts for pasted JSON
python start_time_export.py

# Mit benutzerdefinierter Datei (optional)
python start_time_export.py /path/to/my_data.json
```

1. **Zum Ordner navigieren:**
```bash
cd ./Zeitnachweis/scripts
```

2. **Skript ausführen:**
```bash
python start_time_export.py [data_file] [--output-dir DIR]
```

Wenn keine Datendatei angegeben wird, fordert das Skript zur Eingabe der JSON-Daten auf.

- `data_file`: Pfad zur JSON-Datendatei (optional, wenn nicht angegeben, Eingabeaufforderung)
- `--output-dir`: Output-Verzeichnis (optional, Standard: ../output)

