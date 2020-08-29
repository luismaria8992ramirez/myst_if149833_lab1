
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""


import time as time
import numpy as np
import pandas as pd
import yfinance as yf
from os import listdir, path
from os.path import isfile, join

pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas

# -------------------------------------------------------------------------------------------- PASO 1.1  -- #
# -- Obtener la lista de los archivos a leer

# obtener la ruta absoluta de la carpeta donde estan los archivos
abspath = path.abspath('files/NAFTRAC_holdings')
# obtener una lista de todos los archivos en la carpeta (quitandole la extension de archivo)
# no tener archivos abiertos al mismo tiempo que correr la siguiente linea, error por ".~loc.archivo"
archivos = [f[:-4] for f in listdir(abspath) if isfile(join(abspath, f))]

# --------------------------------------------------------------------------------------------- PASO 1.2 -- #
# -- Leer todos los archivos y guardarlos en un diccionario

# crear un diccionario para almacenar todos los datos
data_archivos = {}

for i in archivos:
    # leer archivos despues de los primeros dos renglones
    data = pd.read_csv('files/NAFTRAC_holdings/' + i + '.csv', skiprows=2, header=None)
    # renombrar las columnas con lo que tiene el 1er renglon
    data.columns = list(data.iloc[0, :])
    # quitar columnas que no sean nan
    data = data.loc[:, pd.notnull(data.columns)]
    # resetear el indice
    data = data.iloc[1:-1].reset_index(drop=True, inplace=False)
    # quitar las comas en la columna de precios
    data['Precio'] = [i.replace(',', '') for i in data['Precio']]
    # quitar el asterisco de columna ticker
    data['Ticker'] = [i.replace('*', '') for i in data['Ticker']]
    # hacer conversiones de tipos de columnas a numerico
    convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
    data = data.astype(convert_dict)
    # convertir a decimal la columna de peso (%)
    data['Peso (%)'] = data['Peso (%)']/100
    # guardar en diccionario
    data_archivos[i] = data

# --------------------------------------------------------------------------------------------- PASO 1.3 -- #
# -- Construir el vector de fechas a partir del vector de nombres de archivos

# estas serviran como etiquetas en dataframe y para yfinance
t_fechas = [i.strftime('%d-%m-%Y') for i in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

# lista con fechas ordenadas (para usarse como indexadores de archivos)
i_fechas = [j.strftime('%d%m%y') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

# --------------------------------------------------------------------------------------------- PASO 1.4 -- #
# -- Construir el vector de tickers utilizables en yahoo finance

tickers = []
for i in archivos:
    # i = archivos[0]
    l_tickers = list(data_archivos[i]['Ticker'])
    [tickers.append(i + '.MX') for i in l_tickers]
global_tickers = np.unique(tickers).tolist()

# ajustes de nombre de tickers
global_tickers = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_tickers]
global_tickers = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_tickers]
global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]

# eliminar entradas de efectivo: MXN, USD, y tickers con problemas de precios: KOFL, BSMXB
[global_tickers.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'BSMXB.MX']]

# --------------------------------------------------------------------------------------------- PASO 1.5 -- #
# -- Descargar y acomodar todos los precios historicos

# para contar tiempo que se tarda
inicio = time.time()

# descarga masiva de precios de yahoo finance
data = yf.download(global_tickers, start="2017-08-21", end="2020-08-21", actions=False,
                   group_by="close", interval='1d', auto_adjust=True, prepost=False, threads=True)

# tiempo que se tarda
print('se tardo', round(time.time() - inicio, 2), 'segundos')

# --------------------------------------------------------------------------------------------- PASO 1.6 -- #
# -- Obtener posiciones historicas

# nota, pasar en todos los meses las posiciones en KOFL.MXN y BSMXB.MX a CASH en MXN

# tomar solo las fechas de interes
# tomar solo las columnas de interes
# transponer matriz para tener x: fechas, y: precios
# multiplicar matriz de precios por matriz de pesos
# hacer suma de cada columna para obtener valor de mercado de la posicion

# capital inicial
k = 1000000
# comisiones por transaccion
c = 0.00125
