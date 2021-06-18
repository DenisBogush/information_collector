# -*- coding: utf-8 -*-

import io
import os
from argparse import ArgumentParser

import pandas as pd
from num2words import num2words

from information_collector.excel import set_autosize, set_format_to_column, share_exchange_rates
from information_collector.send_email import send
from information_collector.web_crawler import download_webdriver, get_currency_pair


# функция для формирования строки в отчетном документе
def get_final_row(prefix, number):
    number_in_str = num2words(number, lang='ru')
    last_digit = number % 10

    # 0
    if not number:
        return '{} нет строк'.format(prefix)

    if 4 < number < 21:
        return '{} {} строк'.format(prefix, number_in_str)

    if 0 < last_digit < 5:
        if last_digit == 1:
            return '{} {}на строка'.format(prefix, number_in_str[:-2])
        elif last_digit == 2:
            return '{} {}е строки'.format(prefix, number_in_str[:-1])
        else:
            # 3, 4
            return '{} {} строки'.format(prefix, number_in_str)
    # 5,6,7,8,9,0
    else:
        return '{} {} строк'.format(prefix, number_in_str)


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--email-to', required=False, help='Email to send to')
    parser.add_argument('--subject', default='Report', help='An email subject')
    parser.add_argument('--attachment-filename', default='report.xlsx', help='An attached file name')
    return parser


def main():
    args_parser = get_parser()
    args = args_parser.parse_args()

    with download_webdriver('win' if os.name == 'nt' else 'linux') as driver:
        currency = get_currency_pair('USD_RUB', 'EUR_RUB', driver_path=driver)
    df_usd = pd.DataFrame(currency['USD_RUB'], columns=['Дата USD', 'Курс USD/RUB']).sort_values('Дата USD',
                                                                                                 ascending=False).reindex()
    df_usd['Курс USD/RUB'] = df_usd['Курс USD/RUB'].str.replace('-', '0')
    df_usd['Курс USD/RUB'] = df_usd['Курс USD/RUB'].str.replace(',', '.').astype(float)
    df_usd['Изменение USD'] = (df_usd['Курс USD/RUB'] - df_usd['Курс USD/RUB'].shift(-1)).fillna(0)

    df_eur = pd.DataFrame(currency['EUR_RUB'], columns=['Дата EUR', 'Курс EUR/RUB']).sort_values('Дата EUR',
                                                                                                 ascending=False).reindex()
    df_eur['Курс EUR/RUB'] = df_eur['Курс EUR/RUB'].str.replace('-', '0')
    df_eur['Курс EUR/RUB'] = df_eur['Курс EUR/RUB'].str.replace(',', '.').astype(float)
    df_eur['Изменение EUR'] = (df_eur['Курс EUR/RUB'] - df_eur['Курс EUR/RUB'].shift(-1)).fillna(0)

    res = df_usd.merge(df_eur, left_index=True, right_index=True, how='outer')

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    res.to_excel(writer, index=False)
    worksheet = writer.book.active

    # устанавливаем форматы ячеек
    set_format_to_column(worksheet, 'Курс USD/RUB', 'Изменение USD', 'Курс EUR/RUB', 'Изменение EUR')

    # заменяем названия колонок на указанные в задании
    for col in worksheet.columns:
        if col[0].value.startswith('Дата'):
            col[0].value = 'Дата'
        if col[0].value.startswith('Изменение'):
            col[0].value = 'Изменение'

    # по тексту задания отношение курсов считается работая с файлом, а не с данными со тсраницы
    share_exchange_rates(worksheet['E'], worksheet['B'], worksheet['G'])

    set_autosize(worksheet)
    writer.save()

    # из за различных настроек терминалов (как они передают конец строки)
    # в винд пароль через аргументы командной строки передать не получилось и времени но нормальное решение не осталось
    email_from = os.environ.get('MY_MAIL', 'mailForRobotR2D2@gmail.com')
    password = os.environ.get('MY_MAIL_PASSWORD', 'der_parol')
    text = get_final_row('В прикрепленном файле excel ', len(res) + 1)
    send(args.subject, text, (args.attachment_filename, output), email_from, password, args.email_to or email_from)
    print('Собранные данные с сайта:')
    print(res)
    print('Письмо отправлено!')
