#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import datetime
import json
import csv
import contextlib

import requests
import pandas as pd

def url_get(url):
    """ Realitza una petició GET amb un user-agent pre-definit """

    headers = {'user-agent': 'cryto-scraper/0.0.1'}
    return requests.get(url, headers=headers)

@contextlib.contextmanager
def open_or_stdout(filename='stdout', mode='w'):
    """ Obre el fitxer especificat o la sortida estándard """

    if filename and filename != 'stdout':
        ensure_path_exists(filename)
        fh = open(filename, mode)
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def ensure_path_exists(path):
    """ S'assegura que el path proporcionat existeixi """

    directory = os.path.dirname(os.path.realpath(os.path.expanduser(path)))
    return os.makedirs(directory, exist_ok=True)

def available_coin_names():
    """ Retorna les criptomonedes (codi) disponibles a coinmarketcap.com """

    response = url_get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
    response_json = json.loads(response.text)

    coin_names = []
    for i in response_json:
        coin_names.append(i['id'])

    return sorted(coin_names)

def fetch_history(coins, output, start_at, end_at):
    """
    Captura les dades disponibles a coinmarketcap.com pels parametres
    especificats i les mostra per pantalla o les escriu en un fitxer CSV.
    """

    result_df = get_history_data(coins, start_at, end_at)

    if (len(result_df.index) > 0):
        write_history_csv(output, result_df)
        return True

    return False

def get_history_data(coins, start_at, end_at):
    """
    Captura les dades disponibles a coinmarketcap.com en un dataframe per les
    criptomonedes especificades en l'interval de temps donat.
    """

    result_df = pd.DataFrame(columns=['Name', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap'])

    for coin in coins:
        try:
            df = get_coin_history_data(coin, start_at, end_at)

            result_df = result_df.append(df, ignore_index=True)
        except Exception as ex:
            print('Error al obtenir dades per a la criptomoneda "{}": {}'.format(coin, str(ex)))

    result_df = result_df.sort_values(by=['Date', 'Name'])

    return result_df

def get_coin_history_data(coin, start_at, end_at):
    """
    Obté les dades històriques de valuacions monetaries per la criptomoneda especificada
    en l'interval donat. Retorna un dataframe.
    """

    response = url_get('https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}'.format(coin, start_at, end_at))

    dfs = pd.read_html(response.text)

    return parse_history_data(pd.DataFrame(dfs[0]), coin)

def parse_history_data(df, name):
    """ Realitza normalitzacions en les dades. """

    df['Name']       = name
    df['Date']       = pd.to_datetime(df['Date'])
    df['Open']       = pd.to_numeric(df['Open'], errors='coerce')
    df['High']       = pd.to_numeric(df['High'], errors='coerce')
    df['Low']        = pd.to_numeric(df['Low'], errors='coerce')
    df['Close']      = pd.to_numeric(df['Close'], errors='coerce')
    df['Volume']     = pd.to_numeric(df['Volume'], errors='coerce')
    df['Market Cap'] = pd.to_numeric(df['Market Cap'], errors='coerce')

    df = df[['Name', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']]

    return df

def write_history_csv(fh, df):
    """
    Escriu el dataframe proporcionat en format CSV en el fitxer donat. El fitxer
    pot ser un recurs existent (com stdout).
    """

    with open_or_stdout(fh) as f:
        df.to_csv(f, index=False, sep=',')

def arg_parser():
    """ Retorna l'objecte ArgumentParser per gestionar els paràmetres """

    parser = argparse.ArgumentParser(description="Scraper de valuació de criptomonedes")

    subparsers = parser.add_subparsers()

    coins_parser = subparsers.add_parser('coins')
    coins_parser.set_defaults(func=main_coins)
    coins_parser.add_argument('--output', default="stdout", help=('Sortida del programa: "stdout" o fitxer. Per defecte: stdout'))

    history_parser = subparsers.add_parser('history')
    history_parser.set_defaults(func=main_history)
    history_parser.add_argument('--output', default="stdout", help=('Sortida del programa: "stdout" o fitxer. Per defecte: stdout'))
    history_parser.add_argument('coin', nargs='+', help='Llista de monedes a extreure (una o més, separades per espai). Consultar la comanda \'coins\'.')
    history_parser.add_argument('--start_at', default="2013-04-28", help='Data d\'inici en format YYYY-MM-DD, per defecte: 2013-04-28')

    default_end_at = datetime.date.today().strftime("%Y-%m-%d")
    history_parser.add_argument('--end_at', default=default_end_at, help='Data de final en format YYYY-MM-DD, per defecte: {}'.format(default_end_at))

    return parser

def main_coins(args):
    """ Controlador de la subcomanda 'coins' """

    coin_names = available_coin_names()

    with open_or_stdout(args.output, 'w') as f:
        print("Criptomonedes disponibles:\n", file=f)
        for coin in coin_names:
            print('- {}'.format(coin), file=f)

def main_history(args):
    """ Controlador de la subcomanda 'history' """

    start_at = datetime.datetime.strptime(args.start_at, '%Y-%m-%d').strftime('%Y%m%d')
    end_at = datetime.datetime.strptime(args.end_at, '%Y-%m-%d').strftime('%Y%m%d')

    result = fetch_history(args.coin, args.output, start_at, end_at)

    if not result:
        print('No hi ha dades disponibles.')

def main():
    parser = arg_parser()
    args = parser.parse_args()

    if not vars(args):
        parser.print_help()
        parser.exit()

    return args.func(args)

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print('[ERROR] {}:{}'.format(type(err).__name__, str(err)))
