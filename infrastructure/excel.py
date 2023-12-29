import operator
import xlsxwriter
import pprint
from postgres import fetch_users_from_database
import itertools


# Sample data for UserRecord instances
user_records = fetch_users_from_database()

# Extract unique dates and sort them
unique_dates = sorted(set(record.date.date() for record in user_records))
# Sort user records by name
user_records = sorted(user_records, key=operator.attrgetter("name", "date"))


table = {}
for record in user_records:
    if record.telegramId not in table:
        table[record.telegramId] = {"telegramId": record.telegramId,
                                    "dates": zip(unique_dates, itertools.repeat('Не ответил'))}
    date = record.date.date()
    table[record.telegramId][date] = record.status

pprint.pprint(table)
pprint.pprint(unique_dates)
# pprint.pprint(user_records)

workbook = xlsxwriter.Workbook("Records.xlsx")
worksheet = workbook.add_worksheet()

# Define a format for the blue cells
blue_format = workbook.add_format(
    {'bg_color': '#62C6FF'})
red_format = workbook.add_format(
    {'bg_color': '#FF6262'})
orange_format = workbook.add_format(
    {'bg_color': '#FFB762'})
green_format = workbook.add_format(
    {'bg_color': '#62FF97'})


for i in range(len(unique_dates)):
    worksheet.write(0, i + 1, unique_dates[i].strftime('%d-%m-%Y'))

# Write user data to the worksheet
for i, key in enumerate(table):
    # key - имя
    worksheet.write(i+1, 0, key)

    for j in range(len(unique_dates)):
        status = table[key].get(unique_dates[j], "NoData")
        
        # Apply conditional formatting to cells with 'NoData'
        if status == 'Не ответил':
            worksheet.write(i+1, j+1, status, blue_format)
        elif status == 'Болен':
            worksheet.write(i+1, j+1, status, red_format)
        elif status == 'Выздоравливает':
            worksheet.write(i+1, j+1, status, orange_format)
        elif status == 'Здоров':
            worksheet.write(i+1, j+1, status, green_format)
        else:
            worksheet.write(i+1, j+1, status)

# Save the workbook and close it.
workbook.close()
