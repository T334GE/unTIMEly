#!/usr/bin/env python3

import streamlit as st
import sys
from pathlib import Path
import json

# Import your existing functions
sys.path.append("scripts")
from export_with_holidays import export_with_holidays
from process_work_day_data import process_work_day_data

# Constants
SCROLL_HEIGHT_JSON = 600
SCROLL_HEIGHT_TABLE = 500
ITEMS_PER_PAGE_OPTIONS = [10, 20, 50, 100]
TEMPLATE_PATH = "templates/template.xlsx"

# Page configuration
st.set_page_config(page_title="unTIMEly Zeitnachweis", page_icon="📊", layout="centered")

# Title and description
st.title("📊 unTIMEly Zeitnachweis")
st.markdown("Arbeitsdaten in Excel-Dateien mit Feiertagsintegration exportieren")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Konfiguration")

    # Name input
    name = st.text_input(
        "Name",
        value="",
        help="Namen für das Exportdokument eingeben",
        placeholder="Max Mustermann",
    )

    # Träger input
    sponsor = st.text_input(
        "Träger/Kundennummer",
        value="",
        help="Träger/Kundennummer für das Exportdokument eingeben",
        placeholder="IBB 12345",
    )

    # Business input
    business = st.text_input(
        "Betrieb",
        value="",
        help="Betrieb für das Exportdokument eingeben",
        placeholder="Firmenname",
    )

    # State code hardcoded to DE since API now only accepts DE
    state_code = "DE"

# Main content area
st.header("📁 Dateneingabe")

# Get script directory for paths
script_dir = Path(__file__).parent

# Data input method selection using tabs
tab1, tab2 = st.tabs(["📁 Datei hochladen", "📝 JSON einfügen"])

with tab1:
    st.subheader("JSON-Datei hochladen")
    uploaded_file = st.file_uploader(
        "JSON-Datei auswählen", type=["json"], help="Arbeitsdaten-JSON-Datei hochladen"
    )

    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            st.success(f"✅ {len(data)} Arbeitstage aus hochgeladener Datei geladen")
            # Store in session state
            st.session_state.work_data = data
            st.session_state.data_source = "uploaded"
        except json.JSONDecodeError as e:
            st.error(f"❌ Ungültiges JSON-Format: {e}")
            st.code(str(e))

with tab2:
    st.subheader("Rohes JSON einfügen")
    raw_json = st.text_area(
        "JSON-Daten hier einfügen",
        height=300,
        placeholder='[{"date": "2026-01-19", "weekday": "Montag", "status": "ANWESEND", "status_label": "Anwesend", "start_time": "08:00", "end_time": "16:30", "duration_minutes": 480, "duration": "08:00", "punch_count": 2, "break_minutes": 30, "fallback_end_applied": false}, ...]',
        help="Arbeitsdaten im JSON-Format einfügen",
    )

    if st.button("🔄 JSON parsen", type="primary"):
        if raw_json.strip():
            try:
                data = json.loads(raw_json)
                # Ensure data is a list
                if isinstance(data, dict):
                    data = [data]
                st.success(f"✅ {len(data)} Arbeitstage aus JSON-Text geparst")
                # Store in session state
                st.session_state.work_data = data
                st.session_state.data_source = "uploaded"
            except json.JSONDecodeError as e:
                st.error(f"❌ Ungültiges JSON-Format: {e}")
                st.code(str(e))
        else:
            st.warning("⚠️ JSON-Daten zuerst einfügen")

# Data preview
if "work_data" in st.session_state and st.session_state.work_data:
    st.header("👀 Datenübersicht")

    # Add pagination controls
    items_per_page = st.selectbox("Elemente pro Seite", ITEMS_PER_PAGE_OPTIONS, index=2)
    total_items = len(st.session_state.work_data)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Page navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Zurück", disabled=st.session_state.get("current_page", 1) <= 1):
            st.session_state.current_page = max(
                1, st.session_state.get("current_page", 1) - 1
            )
    with col2:
        current_page = st.number_input(
            "Seite",
            min_value=1,
            max_value=total_pages,
            value=st.session_state.get("current_page", 1),
            key="current_page_input",
        )
        st.session_state.current_page = current_page
    with col3:
        if st.button(
            "Weiter ➡️", disabled=st.session_state.get("current_page", 1) >= total_pages
        ):
            st.session_state.current_page = min(
                total_pages, st.session_state.get("current_page", 1) + 1
            )

    st.write(
        f"Seite {st.session_state.get('current_page', 1)} von {total_pages} ({total_items} Gesamteinträge)"
    )

    # Export button in data preview section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(
            "🚀 Nach Excel exportieren", type="primary", use_container_width=True
        ):
            try:
                with st.spinner("🔄 Exportiere..."):
                    if st.session_state.data_source == "uploaded":
                        st.write("🔍 Hochgeladene Daten verarbeiten...")
                        processed_work_days = process_work_day_data(
                            st.session_state.work_data, "json"
                        )
                        st.write(
                            f"✅ {len(processed_work_days)} Arbeitstage verarbeitet"
                        )

                        output_files = export_with_holidays(
                            processed_work_days,
                            state_code,
                            template_path=str(script_dir / TEMPLATE_PATH),
                            output_dir=str(script_dir / "output"),
                            name=name,
                            sponsor=sponsor,
                            business=business,
                        )

                        if output_files:
                            st.success("✅ Export erfolgreich abgeschlossen!")
                            st.session_state["output_files"] = output_files
                        else:
                            st.error("❌ Export fehlgeschlagen!")

                    else:
                        # For WorkDay objects from pasted JSON
                        st.write("🔍 Eingefügte Daten verarbeiten...")
                        # WorkDay objects are already processed
                        output_files = export_with_holidays(
                            st.session_state.work_data,
                            state_code,
                            template_path=str(script_dir / TEMPLATE_PATH),
                            output_dir=str(script_dir / "output"),
                            name=name,
                            sponsor=sponsor,
                            business=business,
                        )

                        if output_files:
                            st.success("✅ Export erfolgreich abgeschlossen!")
                            st.session_state["output_files"] = output_files
                        else:
                            st.error("❌ Export fehlgeschlagen!")

            except Exception as e:
                st.error(f"❌ Exportfehler: {e}")
                st.error(f"❌ Fehlertyp: {type(e).__name__}")
                st.error(f"❌ Fehlerdetails: {str(e)}")
                import traceback

                st.error(f"❌ Vollständiger Traceback: {traceback.format_exc()}")

    # Display download buttons if output_files exist in session_state
    if "output_files" in st.session_state and st.session_state["output_files"]:
        st.subheader("📁 Generierte Excel-Dateien:")
        for file_path in st.session_state["output_files"]:
            with open(file_path, "rb") as f:
                file_data = f.read()
            file_name = Path(file_path).name
            st.download_button(
                label=f"⬇️ {file_name} herunterladen",
                data=file_data,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"download_{file_name}",
            )

    with st.expander(
        "Klicken Sie hier, um die Datenübersicht anzuzeigen", expanded=True
    ):
        if st.session_state.data_source == "uploaded":
            # For uploaded data, show as JSON preview with pagination
            st.subheader("📋 Hochgeladene Datenstruktur")

            # Calculate page boundaries
            page = st.session_state.get("current_page", 1)
            start_idx = (page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)
            page_data = st.session_state.work_data[start_idx:end_idx]

            # Create scrollable container
            with st.container(height=SCROLL_HEIGHT_JSON):
                for i, day in enumerate(page_data, start=start_idx + 1):
                    # Get the actual date and weekday from the data for the title
                    day_date = day.get("date", f"Eintrag {i}")
                    day_weekday = day.get("weekday", "")

                    if day_date != f"Eintrag {i}" and day_weekday:
                        day_title = f"{day_date} ({day_weekday})"
                    elif day_date != f"Eintrag {i}":
                        day_title = f"{day_date}"
                    else:
                        day_title = f"Eintrag {i}"

                    with st.expander(f"{day_title}"):
                        # Format as key-value pairs
                        cols = st.columns(2)
                        with cols[0]:
                            for key, value in day.items():
                                if isinstance(value, str) and len(value) > 20:
                                    st.text_area(
                                        f"{key}:",
                                        value=value,
                                        height=60,
                                        key=f"col1_{i}_{key}",
                                    )
                                else:
                                    st.write(f"**{key}:** {value}")
                        with cols[1]:
                            st.write("")  # Empty column for balance

            st.info(
                f"📊 Zeige Einträge {start_idx + 1}-{end_idx} von {total_items} Gesamteinträgen"
            )

        else:
            # For WorkDay objects, show as table with pagination
            st.subheader("📊 Arbeitstage-Übersicht")

            # Create summary stats
            total_days = len(st.session_state.work_data)
            work_statuses = ["Anwesend"]
            work_days = len(
                [d for d in st.session_state.work_data if d.status in work_statuses]
            )
            # Handle None values in duration_minutes
            valid_durations = [
                d.duration_minutes
                for d in st.session_state.work_data
                if d.duration_minutes is not None
            ]
            total_minutes = sum(valid_durations) if valid_durations else 0
            total_hours = total_minutes // 60
            remaining_minutes = total_minutes % 60
            total_hours_display = (
                f"{total_hours}h {remaining_minutes}m"
                if total_hours > 0
                else f"{remaining_minutes}m"
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Gesamt Tage", total_days)
            with col2:
                st.metric("Arbeitstage", work_days)
            with col3:
                st.metric("Gesamt Stunden", total_hours_display)

            # Show paginated data as table
            st.subheader("📋 Arbeitstage")

            # Calculate page boundaries
            page = st.session_state.get("current_page", 1)
            start_idx = (page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)
            page_data = st.session_state.work_data[start_idx:end_idx]

            # Prepare data for display
            table_data = []
            for day in page_data:
                table_data.append(
                    {
                        "Datum": day.date,
                        "Wochentag": day.weekday,
                        "Status": day.status_label,
                        "Start": day.start_time,
                        "Ende": day.end_time,
                        "Dauer": day.duration,
                        "Pause": f"{day.break_minutes}min",
                    }
                )

            # Create scrollable container for table
            with st.container(height=SCROLL_HEIGHT_TABLE):
                st.dataframe(table_data, use_container_width=True)

            st.info(
                f"📊 Zeige Einträge {start_idx + 1}-{end_idx} von {total_items} Gesamteinträgen"
            )

# Instructions
st.header("📖 Anleitung")
with st.expander("Verwendung"):
    st.markdown("""
    1. **Einstellungen konfigurieren**: Name, Sponsor und Business in der Seitenleiste eingeben
    2. **Daten bereitstellen**: JSON-Datei hochladen oder JSON einfügen
    3. **Exportieren**: Export-Schaltfläche klicken, um Excel-Dateien zu erstellen
    4. **Ergebnisse**: Generierte Excel-Dateien direkt herunterladen
    
    **JSON-Dateiformat:**
    JSON-Datei sollte Arbeitsdaten mit Feldern wie Datum, Wochentag, Status, Startzeit, Endzeit usw. enthalten.
    
    Beispiel: {"date": "2026-01-19", "weekday": "Montag", "status": "ANWESEND", "status_label": "Anwesend", "start_time": "08:00", "end_time": "16:30", "duration_minutes": 480, "duration": "08:00", "punch_count": 2, "break_minutes": 30, "fallback_end_applied": false}
    """)

# Footer
st.markdown("---")
st.markdown("Erstellt mit ❤️ unter Verwendung von Streamlit")
