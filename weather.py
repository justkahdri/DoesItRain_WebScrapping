import requests
import lxml.html as html
import os
import datetime
from xpaths import *


def return_days(string):
    today = datetime.date.today()
    splitted = string.split('/')
    splitted = [int(i) for i in splitted]
    if len(splitted) != 3:
        future_day = datetime.date(today.year, splitted[1], splitted[0])
    else:
        future_day = datetime.date(splitted[2], splitted[1], splitted[0])

    delta = future_day - today
    return delta.days


def does_it_rain(future_date, hour, percentage=False):
    n = return_days(future_date) + 1
    ws = to_website(BSAS_HOURLY_URL + str(n))

    web_hours = ws.xpath(XPATH_HOURS)

    precip = []
    full = ws.xpath(XPATH_PERCENTAGES)
    count = 1
    for i in full:
        if count % 2 == 0:
            for ch in ('\t', '\n', '\xa0'):
                i = i.replace(ch, '')
            precip.append(i)
        count += 1

    try:
        for item in web_hours:
            if item == hour:
                idx = web_hours.index(item)
                if percentage:
                    print(f'Hay una probabilidad de {precip[idx]} de que llueva a esa hora')
                if int(precip[idx].replace('%', '')) >= 50:
                    return True
                else:
                    return False
        raise ValueError
    except ValueError:
        print('Ingrese una hora válida')


def report_now():
    today = datetime.datetime.now().strftime("%d-%m-%Y %Hhs")
    report_path = f'./reports/{today}.txt'

    if not os.path.isfile(report_path):
        ws = to_website(BSAS_NOW_URL)

        try:
            temps = ws.xpath(XPATH_TEMPS)
            state = ws.xpath(XPATH_STATE)[0]
            extra_stats = ws.xpath(XPATH_STATS)
        except IndexError:
            raise

        with open(report_path, 'w', encoding='utf-8') as f:
            invalid = True
            f.write(f'La temperatura actual es de {temps[0][:-1]}C{temps[0][-1]} y está {state.lower()}\n')
            while invalid:
                option = input('Desea imprimir la información extra? (Si/No): ')
                if option.lower() == 'no':
                    f.write('\n')
                    invalid = False
                elif option.lower() == 'si':
                    f.write(f'La calidad del aire es: {extra_stats[0]}\n')
                    f.write(f'La velocidad del viento es: {extra_stats[1]}\n')
                    f.write(f'La ráfagas de viento son de: {extra_stats[2]}\n\n')
                    invalid = False
                else:
                    print('Ingrese una opción válida')
            f.write(f'La temperatura de esta noche será de {temps[1][:-1]}C{temps[1][-1]} \n')
            f.write(f'La temperatura de mañana será de {temps[2][:-1]}C{temps[2][-1]} \n')
    else:
        print('Ya se realizó un reporte en la última hora')


def to_website(url):
    try:
        response = requests.get(url, headers={"User-Agent": "J5"})
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            return parsed
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


if __name__ == '__main__':
    report_now()
    print(does_it_rain('18/11', '4', True))
