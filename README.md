# M2.951 · Tipología i cicle de vida de les dades
# PRAC 1: Web Scraping

## Descripció

Aquesta pràctica s'ha realitzat per a l'assignatura de *Tipologia i cicle de vida de les dades*, cursada dins el *Màster en Ciència de Dades* de la *Univesitat Oberta de Catalunya (UOC)*.

En ella, s'apliquen tècniques de *web scraping* per extreure les dades de valuacions diàries de les 25 *crypto-monedes* més importants de la web [Cryptocurrency Market Capitalizations](https://coinmarketcap.com/), utilitzant el llenguatge de programació [Python](https://www.python.org).

## Membres de l'equip

Aquesta pràctica s'ha realitzat de forma individual per **Estanislau Trepat i López**.

## Arxius en aquest repositori

* `dataset/cryptocurrencies.txt`: Llistat de criptomonedes disponibles a [coinmarketcap.com](https://coinmarketcap.com). Obtingut amb l'*scraper* implementat en aquesta PRAC.
* `dataset/crypto-dataset-top25.csv`: Dataset generat amb l'*scraper* realitzat en aquesta PRAC.
* `src/requirements.txt`: Fitxer de requeriments de llibreries/programari per a la eina *[Pip](https://pypi.org/project/pip/)* de [Python](https://www.python.org).
* `src/scraper.py`: *Scraper* implementat per a la resolució d'aquesta PRAC.
* `etrepat-PRAC1.(odt|pdf)`: Document amb les respostes requerides en aquesta PRAC.

## Dataset

El dataset generat amb l'*Scraper* implementat per aquesta PRAC conté les *valuacions* de *trading* (o bursàtil) per a les 25 criptomonedes més importants (a nivell de capitalització monetario) desde el 28 d'abril de 2013 fins el 15 d'abril de 2018. Es a dir, gairebé 5 anys complerts.

El dataset està comprés de 23219 registres i 8 atributs en cada registre, ocupant en disc aproximadament ~1,7Mb.

Els atributs presents en el dataset són (tots els valors monetaris s'expressen en dòlars americans):

* `Name`: Nom de la criptomoneda.
* `Date`: Data a la que el registre fà referència (dia, en format YYYY-MM-DD).
* `Open`: Valoració monetaria en l'apertura del dia.
* `High`: Valoració monetaria màxima del dia.
* `Low`: Valoració monetaria mínima del dia.
* `Close`: Valoració monetaria al tancament del dia.
* `Volume`: Volum monetari tractat (24h).
* `Market Cap`: Valor de la capitalització de mercat (preu * circulant).

## Scraper

L'*Scraper* implementat en aquesta PRAC està pensat per utilitzar com una eina en la línia de comandes.

### Instal·lació

Per utilitzar-lo, es pot clonar aquest repositori (amb git):

```
$ git clone https://github.com/etrepat/tcvd-prac1.git
```

### Requeriments

L'script implementat necessita d'algunes llibreries que necessitarem instal·lar per a poder executar-lo correctament. Ho podem fer fàcilment, per mitjà del fitxer `requirements.txt` proporcionat i l'eina *[Pip](https://pypi.org/project/pip/)*. Per exemple, la comanda següent instal·larà les dependències necessàries (executant-la des de l'arrel del projecte):

```
$ pip install -r src/requirements.txt
```

### Ús/Sintaxi

Podem veure les instruccions d'us fàcilment:

```
$ python src/scraper.py -h
```

L'script d'*scraping* implementat per aquesta PRAC disposa de dues subcomandes principals `coins` i `history`. La primera extreu un llistat de criptomonedes disponibles en la web [coinmarketcap.com](https://coinmarketcap.com), els noms de les quals es poden fer servir en la subcomanda `history`. La segona, extreu les dades històriques mercantils per a les criptomonedes especificades.

En la subcomanda `coins`, només es pot especificar el fitxer de sortida per mitjà de l'opció `--output`. Si no s'especifica, els resultats es treuràn per pantalla.

En la subcomanda `history`, es pot especificar les criptomonedes de les que volem extreure dades, un interval de dates de treball per mitjà de les opcions `--start_at` i `--end_at` i un fitxer de sortida amb l'opció `--output`. Si aquest últim no s'especifica les dades es mostraràn per pantalla.

Es pot veure informació detallada de com funciona cada subcomanda, així com dels diferents paràmetres i els seus valors per defecte, demanant ajuda a la eina:

```
$ python src/scraper.py history -h
```

Quan s'utilitza la subcomanda `history`, tant si s'especifica un fitxer de sortida com si no (es mostren per pantalla), les dades retornades es trobarán en format CSV, utilitzant la coma com a separador.

#### Exemples d'ús

Per llistar les criptomonedes disponibles per pantalla:

```
$ python src/scraper.py coins
```

Per llistar les criptomonedes disponibles en un fitxer:

```
$ python src/scraper.py coins --output=noms.txt
```

Per extreure les dades mercantils de la criptomoneda *bitcoin* des de l'1 de gener de 2018 per pantalla:

```
$ python src/scraper.py history bitcoin --start_at=2018-01-01
```

Per extreure les dades mercantils de les criptomonedes *bitcoin* i *litecoin* des de l'inici (28/04/2013) fins a dia d'avui en un fitxer:

```
$ python src/scraper.py history bitcoin litecoin --output=cryptos.csv
```

La comanda utilitzada per a generar el dataset que es troba en aquest repositori es la següent:

```
$ python3 src/scraper.py history bitcoin ethereum ripple bitcoin-cash litecoin cardano stellar iota neo monero nem dash ethereum-classic qtum verge lisk bitcoin-gold zcash nano bytecoin-bcn steem wanchain siacoin bitshares dogecoin --output=dataset/crypto-dataset-top25.csv
```
