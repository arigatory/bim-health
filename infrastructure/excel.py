import uuid
import xlsxwriter
from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserRecord:
    id: uuid.UUID
    telegramId: int
    name: str
    status: str
    date: datetime


# Sample data for UserRecord instances
user_records = [
    UserRecord(uuid.uuid4(), 123, 'John Doe', 'Active', datetime(2023, 1, 1)),
    UserRecord(uuid.uuid4(), 456, 'Alice Smith',
               'Inactive', datetime(2023, 1, 2)),
    UserRecord(uuid.uuid4(), 789, 'Bob Johnson',
               'Active', datetime(2023, 1, 1)),
    UserRecord(uuid.uuid4(), 101, 'Eve Williams', '', datetime(2023, 1, 3)),
    # Add more sample data as needed
]

# Extract unique dates and sort them
unique_dates = sorted(set(record.date.date() for record in user_records))
# Sort user records by name
user_records.sort(key=lambda record: record.name)

workbook = xlsxwriter.Workbook("Records.xlsx")
worksheet = workbook.add_worksheet()

# Define a format for the blue cells
blue_format = workbook.add_format(
    {'bg_color': '#0000FF', 'font_color': '#FFFFFF'})


# Write the header row with dates
worksheet.write('A1', 'Name')
for col_num, date in enumerate(unique_dates, start=1):
    col_letter = chr(ord('A') + col_num)
    worksheet.write(0, col_num, date.strftime('%Y-%m-%d'))

# Write user data to the worksheet
for row_num, user_record in enumerate(user_records, start=1):
    worksheet.write(row_num, 0, user_record.name)

    for col_num, date in enumerate(unique_dates, start=1):
        col_letter = chr(ord('A') + col_num)
        status = next((record.status for record in user_records if record.date.date(
        ) == date and record.name == user_record.name), 'NoData')

        # Apply conditional formatting to cells with 'NoData'
        if status == 'NoData':
            worksheet.write(row_num, col_num, status, blue_format)
        else:
            worksheet.write(row_num, col_num, status)

# Save the workbook and close it.
workbook.close()
