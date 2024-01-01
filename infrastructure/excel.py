import xlsxwriter
from .postgres import fetch_names, fetch_users_from_database
import itertools


def make_report():
    names_mappings = fetch_names()
    # Create dictionaries
    telegram_id_real_name_dict = {
        record.telegram_id: record.real_name for record in names_mappings}

    def get_real_name(tg_id):
        # Attempt to get real name from the nickname_real_name_dict
        if tg_id in telegram_id_real_name_dict:
            return telegram_id_real_name_dict[tg_id]

        return f"Unknown {tg_id}"

    # Sample data for UserRecord instances
    user_records = fetch_users_from_database()

    # Extract unique dates and sort them
    unique_dates = sorted(set(record.date.date() for record in user_records))
    # Sort user records by name
    user_records = sorted(
        user_records, key=lambda x: get_real_name(x.telegramId))

    table = {}
    for record in user_records:
        if record.telegramId not in table:
            table[record.telegramId] = {"telegramId": record.telegramId,
                                        "dates": zip(unique_dates, itertools.repeat('Не ответил'))}
        date = record.date.date()
        table[record.telegramId][date] = record.status

    # pprint.pprint(table)
    # pprint.pprint(unique_dates)
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
        worksheet.write(i+1, 0, get_real_name(key), None)

        for j in range(len(unique_dates)):
            status = table[key].get(unique_dates[j], "Не ответил")

            # Apply conditional formatting to cells with 'NoData'
            if status == 'Не ответил':
                worksheet.write(i+1, j+1, status, blue_format)
            elif status == 'Болен':
                worksheet.write(i+1, j+1, status, red_format)
            elif status == 'Почти выздоровел':
                worksheet.write(i+1, j+1, status, orange_format)
            elif status == 'Здоров':
                worksheet.write(i+1, j+1, status, green_format)
            else:
                worksheet.write(i+1, j+1, status)
                
    # Autofit the worksheet.
    worksheet.autofit()
    # Save the workbook and close it.
    workbook.close()
