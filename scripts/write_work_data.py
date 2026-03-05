from get_status_label import get_status_label

WORK_STATUSES = {"A", "P", "ANWESEND"}
DATE_COLUMN = 1
DEFAULT_HEADER_ROW = 6
DEFAULT_STATUS_COLUMN = 2
DEFAULT_START_TIME_COLUMN = 4
DEFAULT_END_TIME_COLUMN = 5
DEFAULT_BREAK_COLUMN = 6
FIRST_SHEET_INDEX = 0
MINUTES_PER_HOUR = 60
TIME_FORMAT_HOURS = "02d"
TIME_FORMAT_MINUTES = "02d"


def write_work_data(
    wb,
    work_days_with_dates: list,
    header_row: int = DEFAULT_HEADER_ROW,
    status_column: int = DEFAULT_STATUS_COLUMN,
    start_time_column: int = DEFAULT_START_TIME_COLUMN,
    end_time_column: int = DEFAULT_END_TIME_COLUMN,
    break_column: int = DEFAULT_BREAK_COLUMN,
):
    if not wb.sheetnames:
        print("⚠️  Warning: No sheets found in workbook - cannot write work data")
        return

    ws = wb[wb.sheetnames[FIRST_SHEET_INDEX]]

    for day, date_obj in work_days_with_dates:
        target_row = header_row + date_obj.day

        if target_row > ws.max_row:
            sheet_name = (
                wb.sheetnames[FIRST_SHEET_INDEX] if wb.sheetnames else "unknown"
            )
            print(
                f"⚠️  Warning: Cannot write data for {day.date} "
                f"({date_obj.strftime('%Y-%m-%d')}) - "
                f"row {target_row} exceeds sheet '{sheet_name}' max row {ws.max_row}"
            )
            continue

        ws.cell(row=target_row, column=DATE_COLUMN, value=date_obj)
        ws.cell(
            row=target_row,
            column=status_column,
            value=get_status_label(day.status),
        )

        normalized_status = str(day.status).upper()

        if normalized_status in WORK_STATUSES:
            ws.cell(
                row=target_row,
                column=start_time_column,
                value=day.start_time,
            )
            ws.cell(row=target_row, column=end_time_column, value=day.end_time)
            ws.cell(
                row=target_row,
                column=break_column,
                value=f"{day.break_minutes // MINUTES_PER_HOUR:{TIME_FORMAT_HOURS}}:{day.break_minutes % MINUTES_PER_HOUR:{TIME_FORMAT_MINUTES}}",
            )
        else:
            ws.cell(row=target_row, column=start_time_column, value=None)
            ws.cell(row=target_row, column=end_time_column, value=None)
            ws.cell(row=target_row, column=break_column, value=None)
