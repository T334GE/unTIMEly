from datetime import datetime
from pathlib import Path
import os
from typing import List
import openpyxl

from validate_paths import validate_paths
from find_template_sheet import find_template_sheet
from update_sheet_dates import update_sheet_dates
from fetch_holidays import fetch_holidays
from fill_holidays import fill_holidays
from fill_name import fill_name
from fill_month_name import fill_month_name
from fill_sponsor import fill_sponsor
from fill_business import fill_business
from write_work_data import write_work_data

DEFAULT_STATE_CODE = "NI"
DEFAULT_TEMPLATE_PATH = "../templates/template.xlsx"
DEFAULT_OUTPUT_DIR = "../output"
DATE_FORMAT = "%Y-%m-%d"


def export_with_holidays(
    work_data: List,
    state_code: str = "DE",
    template_path: str = DEFAULT_TEMPLATE_PATH,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    name: str = "",
    sponsor: str = "",
    business: str = "",
) -> List[str]:
    try:
        if not os.path.exists(template_path):
            print(f"Error: Template file {template_path} not found")
            return []

        validate_paths(template_path, output_dir)

        parsed_dates = {}
        months_data = {}
        output_files = []

        for day in work_data:
            if day.date not in parsed_dates:
                parsed_dates[day.date] = datetime.strptime(day.date, DATE_FORMAT)
            date_obj = parsed_dates[day.date]
            month_key = (date_obj.year, date_obj.month)
            if month_key not in months_data:
                months_data[month_key] = []
            months_data[month_key].append((day, date_obj))

        for year, month in sorted(months_data.keys()):
            month_work_days = months_data[(year, month)]
            output_filename = f"ZEITNACHWEIS_{year}_{month}.xlsx"
            output_path = Path(output_dir) / output_filename
            sheet_name = f"{month:02d}-{year}"

            print(f"Creating file from template: {output_filename}")
            template_wb = openpyxl.load_workbook(template_path)
            fill_name(template_wb, name)
            fill_sponsor(template_wb, sponsor)
            fill_business(template_wb, business)
            template_sheet = find_template_sheet(template_wb)

            new_sheet = template_wb.copy_worksheet(template_sheet)
            new_sheet.title = sheet_name
            fill_month_name(new_sheet, month, year)
            update_sheet_dates(new_sheet, year, month)
            template_wb.remove(template_sheet)

            months_in_data = {(year, month)}
            all_holidays = fetch_holidays(months_in_data, state_code)
            fill_holidays(template_wb, months_in_data, all_holidays)

            write_work_data(template_wb, month_work_days)
            template_wb.save(output_path)

            print(f"Exported {output_filename} with {len(month_work_days)} work days")
            output_files.append(str(output_path))

        print(f"Created {len(months_data)} separate files in output folder")
        return output_files

    except (
        openpyxl.utils.exceptions.InvalidFileException,
        FileNotFoundError,
        PermissionError,
    ) as e:
        print(f"Error: Template file {template_path} not found or inaccessible: {e}")
        return False
    except (ValueError, KeyError, IndexError) as e:
        print(f"Error: Invalid data format while processing work data: {e}")
        return False
    except OSError as e:
        print(f"Error: File system error during export: {e}")
        return False
    except (TypeError, AttributeError) as e:
        print(f"Warning: Error processing holiday data during export: {e}")
        return False
