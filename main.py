

"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Contrast passive investment against active investment Carry out rebalancing policies       -- #
#    to maximize performance.                                                                            -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: luismaria8992ramirez                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository:https://github.com/luismaria8992ramirez/lab1_if691761-iteso.mx/blob/master/main.py                                             -- #
"""


# Importar librerías
import time
import numpy as np
import pandas as pd
import yfinance as yf
import os
import plotly.graph_objects as go
import plotly.offline as pyo

# Opciones
pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas

# data.py
# -------------------------------------------------------------------------------------------- PASO 1.1  -- #
# -- Obtener la lista de los archivos a leer
# Ruta absoluta de archivos
abspath = os.path.abspath("NAFTRAC_holdings")
# obtener una lista de todos los archivos en la carpeta (quitandole la extension de archivo)
# no tener archivos abiertos al mismo tiempo que correr la siguiente linea, error por ".~loc.archivo"
archivos = [i[:-4] for i in os.listdir(abspath) if os.path.isfile(os.path.join(abspath,i))]

# data.py
# --------------------------------------------------------------------------------------------- PASO 1.2 -- #
# -- Leer todos los archivos y guardarlos en un diccionario

# crear un diccionario para almacenar todos los datos
data_archivos = {}

for i in archivos:
    # leer archivos despues de los primeros dos renglones
    data = pd.read_csv(os.path.join(abspath, i + ".csv"),skiprows = 2, header = None)
    # Renombrar y quitar columna sin nombre
    columns = data.iloc[0,:][data.iloc[0,:].notnull()].values.tolist() # Elegir solo los que no son nan's
    # Remover nan's
    data = data.loc[:,data.iloc[0,:].notnull()].dropna() 
    # Establecer columnas
    data.columns = columns
    # resetear el indice
    data = data.iloc[1:-1].reset_index(drop = True, inplace = False)
    # quitar las comas en la columna de precios
    data["Precio"] =  data["Precio"].apply(lambda x: x.replace(",",""))
    # quitar el asterisco de columna ticker
    data["Ticker"] =  data["Ticker"].apply(lambda x: x.replace("*",""))
    # hacer conversiones de tipos de columnas a numerico
    convert_dict = {"Ticker":str,"Nombre":str,"Peso (%)":float,"Precio":float}
    data = data.astype(convert_dict)
    # convertir a decimal la columna de peso (%)
    data["Peso (%)"] = data["Peso (%)"]/100 
    # guardar en diccionario
    data_archivos[i] = data
    
# functions.py
# --------------------------------------------------------------------------------------------- PASO 1.3 -- #
# -- Construir el vector de fechas a partir del vector de nombres de archivos

# estas serviran como etiquetas en dataframe y para yfinance  
t_fechas = [i.strftime("%d-%m-%Y") for i in sorted(pd.to_datetime(i[8:]).date() for i in archivos)]

# lista con fechas ordenadas (para usarse como indexadores de archivos)
i_fechas = [j.strftime("%d%m%Y") for j in sorted(pd.to_datetime(i[8:]).date() for i in archivos)]

# functions.py
# --------------------------------------------------------------------------------------------- PASO 1.4 -- #
# -- Construir el vector de tickers utilizables en yahoo finance

ticker = []

for i in archivos:
    # i = archivos[0]
    l_ticker = list(data_archivos[i]["Ticker"])
    [ticker.append(i + ".MX") for i in l_ticker]

global_tickers = np.unique(ticker).tolist()

# ajustes de nombre de tickers
global_tickers = [i.replace("GFREGIOO.MX", "RA.MX") for i in global_tickers]
global_tickers = [i.replace("MEXCHEM.MX", "ORBIA.MX") for i in global_tickers]
global_tickers = [i.replace("LIVEPOLC.1.MX", "LIVEPOLC-1.MX") for i in global_tickers]

# eliminar entradas de efectivo: MXN, USD, y tickers con problemas de precios: KOFL, BSMXB
# Usamos try porque puede que no tenga alguno y marque algún error
lista =  ["MXN.MX","KOFL.MX","KOFUBL.MX","BSMXB.MX","USD.MX"] 
for i in lista:
    try:
        global_tickers.remove(i)
    except:
        pass

# functions.py
# --------------------------------------------------------------------------------------------- PASO 1.5 -- #
# -- Descargar y acomodar todos los precios historicos

# para contar tiempo que se tarda
inicio = time.time()    

# descarga masiva de precios de yahoo finance
data = yf.download(global_tickers, start = "2017-08-21", end = "2020-08-22", actions = False,
                   group_by = "close", interval = "1d", auto_adjust = True, prepost = False, threads = True)
copia = data.copy()

# tiempo que se tarda
print("Se tardó", time.time()- inicio, " Segundos.")

# main.py
# --------------------------------------------------------------------------------------------- PASO 1.6 -- #
# -- Obtener posiciones históricas

# Tomar solo las fechas de interes
# Tomar solo las columnas de interes
# Transponer matriz para tener x: fechas, y: precios
# Multiplicar matriz de precios por matriz de pesos
# Hacer suma de cada columna para obtener valor de mercado


# Convertir columnas de fechas
data_close = pd.DataFrame({i: data[i]["Close"] for i in global_tickers})

# Tomar solo las fechas de interes (utlizando teoría de conjuntos)
prueba_fechas = [j.strftime("%Y-%m-%d") for j in sorted(pd.to_datetime(i[8:]).date() for i in archivos)]
# Se cambia el tipo de fecha para que se ajuste al mismo formato y veamos si se encuentran todas
ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(prueba_fechas)))
# Localizar todos los precios
precios = np.concatenate([np.where(data_close.index == ic_fechas[i]) for i in range(len(ic_fechas))]).reshape(len(ic_fechas),)
# Elegir Posiciones históricas
closes_timeframe = data_close.iloc[precios,:]

# Ordenar columnas en orden lexográfico
precios = closes_timeframe.reindex(sorted(closes_timeframe.columns), axis = 1)

# main.py
# --------------------------------------------------------------------------------------------- PASO 1.7 -- #
# -- Evolución del capital

# Acomodar columnas de ponderaciones para que tengan el mismo orden que los precios

# Leer primer archivo en orden cronológico para obtener las ponderaciones y los activos con los que se va a trabajar
ponderaciones_iniciales = data_archivos["NAFTRAC_"+i_fechas[0][:-4]+i_fechas[0][-2:]][["Ticker","Peso (%)"]]
# Agregar ".MX" a cada ticker
ponderaciones_iniciales["Ticker"] = [l+ ".MX" for  l in ponderaciones_iniciales["Ticker"]]
# Tomar los tickers para cambiar los activos que no son con ".MX", sino tienen un nombre distinto para consultar
tickers = ponderaciones_iniciales["Ticker"]       
# Remplazar 
tickers = [i.replace("GFREGIOO.MX", "RA.MX") for i in tickers]
tickers  = [i.replace("MEXCHEM.MX", "ORBIA.MX") for i in tickers]
tickers = [i.replace("LIVEPOLC.1.MX", "LIVEPOLC-1.MX") for i in tickers]
# Poner como CASH los activos que se quedarán fuera (por falta de información o algún eveno inesperado).
tickers = [i.replace("MXN.MX", "CASH") for i in tickers]
tickers = [i.replace("KOFL.MX", "CASH") for i in tickers]
tickers = [i.replace("KOFUBL.MX", "CASH") for i in tickers]
tickers = [i.replace("BSMXB.MX", "CASH") for i in tickers]
tickers = [i.replace("USD.MX", "CASH") for i in tickers]
# Renombrar tickers con las modificicaciones correspondientes
ponderaciones_iniciales["Ticker"] = tickers
# Establecer como index la lista de tickers con sus nuevos cambios
ponderaciones_iniciales.set_index("Ticker", inplace = True)
# Agrupar para poder sumar las ponderaciones de los tickers de CASH
ponderaciones_iniciales = ponderaciones_iniciales.groupby("Ticker").sum()  
# Guardar el porcentaje que se quedará en CASH para eliminar el ticker del DATAFRAME y poder trabajar mejor
cash_proporcion = ponderaciones_iniciales.loc["CASH",:].values.tolist()[0]
# Eliminar CASH DE los tickers
ponderaciones_iniciales = ponderaciones_iniciales.drop("CASH")
# Conocer los precios en las fechas históricas y transponerlo para después concatenarlo con las ponderaciones
ajustar_precios = precios[ponderaciones_iniciales.index.values.tolist()].T
# Se tiene la ponderación de cada activo con sus precios en las fechas acordadas.
sss = pd.concat([ponderaciones_iniciales,ajustar_precios],axis = 1) 

# Posición Inicial
k = 1000000
# Comisiciones por transacción
c = 0.00125

# Removemos los pesos
Final = sss.iloc[:,1:].T
# Conocer el cambio que se tiene en cada periodo de tiempo
porcentajes = Final.pct_change().dropna()

# Obtener el rendimiento en cada periodo con respecto al otro y ajustarlo con su ponderación correspondiente 
# para saber como fluctua el portafolio
rendimientos = []

for k in range(len(porcentajes)):
    # Ponderaciones
    pond = sss.iloc[:,0].values
    # Precios por fecha
    cambios = porcentajes.iloc[k,:].values
    # Agregar el rendimiento a partir de los cambios de un tiempo con respecto al otro considerando su ponderación
    # En la cartera o portafolio.
    rendimientos.append(np.sum(cambios*pond))

# Construir DataFrame
Tabla = pd.DataFrame(columns = ["Timestamp","Capital","CASH", "Rend_Acum"])
Tabla["Timestamp"] = sss.columns.values[1:]
Tabla.set_index("Timestamp", inplace = True)
k = 1000000
Tabla.Capital = k
# Agregar lo que está en cada periodo en CASH (Se mantiene constante)
Tabla.CASH = k*cash_proporcion
rends = [0]
rends.extend(rendimientos)
Tabla.Rend_Acum = np.cumsum(rends)
print(Tabla)

# visualizations.py and main.py
# --------------------------------------------------------------------------------------------- PASO 1.8 -- #
# -- graficas de evolución del capital
k = 1000000

trace = go.Scatter(x=precios.index[1:],y = (1+np.array(rends[1:]))*(k)+k*cash_proporcion, mode = "markers+lines", name = "Rendimiento en Periodos")
trace1 = go.Scatter(x=precios.index[1:],y = (1+np.cumsum(rends[1:]))*k+k*cash_proporcion, mode = "markers+lines", name = "Rendimiento en Periodos Acumulado")
data = [trace, trace1]
layout = go.Layout(title  = "Plot de rendimientos simples y acumulados",
                   hovermode = "closest", xaxis = {"title":"Rendimiento"}, yaxis = {"title":"Fechas"})
fig = go.Figure(data = data, layout = layout) 
pyo.plot(fig, filename = "Lines.html")
fig.show()


# --------------------------------------------------------------------------------------------- PASO 1.9 -- #
# -- Gestión Activa (Obtención de Volatilidades)

# Las ponderaciones de los activos inicialese se actualizarán en base al Sharpe Ratio. 
# Se le quitará el 20% de manera equitativa a cada activo y ese 20% se repartirá entre los 5 activos que
# Tuviesen un mayor sharpe ratio.

# Recordar que para obtener el sharpe ratio se necesitan las volatilidades, por lo tanto, se calcularán las volatilidades
# De un periodo con respecto a otro para cada activo. 
Precios_activos = data_close[Final.columns.values.tolist()] # Obtener todos los precios de los activos iniciales
volatilidades = pd.DataFrame(index =  Precios_activos.columns.values) # DataFrame vacio para las volatilidades
for s in range(len(prueba_fechas)-1):
    if s == 0:
        # Tomar datos entre cada lapso
        df = Precios_activos.loc[pd.to_datetime(prueba_fechas[s]):pd.to_datetime(prueba_fechas[s+1]),:].pct_change().dropna()
        # Se quita el primer dato del siguiente periodo, pues no se debe de utilizar
        df = df[:-1].std()
        volatilidades.index = df.index.values
        
        volatilidades[str(pd.to_datetime(prueba_fechas[s]))[:10]+"+"+str(pd.to_datetime(prueba_fechas[s+1]))[:10]] = df
    else:
        # Tomar datos entre cada lapso
        r = Precios_activos.loc[pd.to_datetime(prueba_fechas[s]):pd.to_datetime(prueba_fechas[s+1]),:].pct_change().dropna()
        # Se quita el primer dato del siguiente periodo, pues no se debe de utilizar
        r = r[:-1].std()
        # Se pone de título en cada columna el plazo de donde se agarran los datos
        volatilidades[str(pd.to_datetime(prueba_fechas[s]))[:10]+"+"+str(pd.to_datetime(prueba_fechas[s+1]))[:10]] = r
volatilidades.columns = porcentajes.index.values
# --------------------------------------------------------------------------------------------- PASO 2.0 -- #
# -- Gestión Activa (Obtención de Ratios de Sharpe)

# Tasa Libre de Riesgo
rf = .047505
Ratio_Sharpe = (porcentajes.T - rf)/volatilidades
Ratio_Sharpe.columns = [str(l)[:10] for l in Ratio_Sharpe.columns]
# --------------------------------------------------------------------------------------------- PASO 2.1 -- #
# -- Gestión Activa (Realizar rebalanceos)

# Crear DataFrame que tenga las nuevas ponderaciones
cambio_en_ponderaciones = pd.DataFrame(index = Ratio_Sharpe.index.values.tolist(), columns = [str(Ratio_Sharpe.columns.values[0])], 
                                       data = ponderaciones_iniciales.values)
clmns = Ratio_Sharpe.columns.values.tolist()


for ls in range(len(clmns)):
    if ls == 0:
        pass # Lo pasa porque las primeras ponderaciones no se modifican, pues no existe algún registro existente
    else:
        # Reducir en un 20%
        data_nuevo = pd.DataFrame(cambio_en_ponderaciones.loc[:,clmns[ls-1]])*.80
        # Ver cuanto fue la diferencia del 20%
        agregar  = (cambio_en_ponderaciones.loc[:,clmns[ls-1]].sum()- data_nuevo.sum()).values[0]
        # Agrupar y ordenar para saber cuales fueron los que tuvieron mayor ratio de sharpe
        nuevos_datos = pd.DataFrame(Ratio_Sharpe.iloc[:,ls]).groupby("Ticker").sum()
        nuevos_datos = nuevos_datos.sort_values(clmns[ls], ascending=False)
        for i in range(5):
            # Contador de uno a 5 porque se va a agregar en los mejores 5 
            # Agregar en los mejores 5
            data_nuevo.loc[nuevos_datos.index.values[i],data_nuevo.columns.values[0]] = data_nuevo.loc[nuevos_datos.index.values[i],data_nuevo.columns.values[0]] + agregar/5
        
        # Agregar todo en un dataset
        cambio_en_ponderaciones[clmns[ls]] = data_nuevo
    
# --------------------------------------------------------------------------------------------- PASO 2.2 -- #
# -- Evolución del capital

# Ajustar índices
porcentajes.index = cambio_en_ponderaciones.T.index
# Ver cambio ponderado de la cartera
ajustes = cambio_en_ponderaciones.T*porcentajes
# Conocer lo que se tiene en cash
cash_p = 1-cambio_en_ponderaciones.iloc[:,0].sum()
ss = ajustes.sum(axis = 1).values.tolist()
rr = [0]
rr.extend(ss)
cumsum = np.cumsum(ss)
# Construir DataFrame
Tabla = pd.DataFrame(columns = ["Timestamp","Capital","CASH", "Rend_Acum"])
Tabla["Timestamp"] = ajustes.index.values
Tabla.set_index("Timestamp", inplace = True)
k = 1000000
Tabla.Capital = k
# Agregar lo que está en cada periodo en CASH (Se mantiene constante)
Tabla.CASH = k*cash_p
Tabla.Rend_Acum = cumsum
print(Tabla)
# --------------------------------------------------------------------------------------------- PASO 2.4 -- #
# -- graficas de evolución del capital en inversión activa
k = 1000000

trace = go.Scatter(x=ajustes.index,y = (1+np.array(rr[1:]))*(k)+k*cash_p, mode = "markers+lines", name = "Rendimiento en Periodos")
trace1 = go.Scatter(x=ajustes.index,y = (1+np.cumsum(rr[1:]))*k+k*cash_p, mode = "markers+lines", name = "Rendimiento en Periodos Acumulado")
data = [trace, trace1]
layout = go.Layout(title  = "Plot de rendimientos simples y acumulados (Gestión Activa)",
                   hovermode = "closest", xaxis = {"title":"Rendimiento"}, yaxis = {"title":"Fechas"})
fig = go.Figure(data = data, layout = layout) 
pyo.plot(fig, filename = "Lines.html")
fig.show()

