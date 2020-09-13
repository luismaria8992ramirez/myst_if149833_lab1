"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Contrast passive investment against active investment Carry out rebalancing policies       -- #
#    to maximize performance.                                                                            -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: luismaria8992ramirez                                                                     -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository:https://github.com/luismaria8992ramirez/lab1_if691761-iteso.mx/blob/master/functions.py                                                                     -- #
"""


def fechas(archivos):
    """ Ajustar fechas para su procesamiento posteriormente.
    Parameters    
    ----------------------------------------------------------------------------------------------    
    :param archivos: Lista de fechas. 
    Returns
    ----------------------------------------------------------------------------------------------  
    :return [t_fechas, i_fechas]: Fechas con formatos distintos.
    """
    import pandas as pd
    # estas serviran como etiquetas en dataframe y para yfinance  
    t_fechas = [i.strftime("%d-%m-%Y") for i in sorted(pd.to_datetime(i[8:]).date() for i in archivos)]
    
    # lista con fechas ordenadas (para usarse como indexadores de archivos)
    i_fechas = [j.strftime("%d%m%Y") for j in sorted(pd.to_datetime(i[8:]).date() for i in archivos)]
    
    return [t_fechas, i_fechas]

def global_tickers(archivos, data_archivos):
    
    """ Ver todos los tickers existentes en el periodo.
    Parameters    
    ----------------------------------------------------------------------------------------------    
    :param archivos: Lista de fechas. 
    :param datos_archivos: Lista de DataFrames con datos del NAFTRAC por periodos.
    Returns
    ----------------------------------------------------------------------------------------------  
    :return global_tickers: Todos los tickers del periodo analizado
    """
    
    import numpy as np
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
        
    return global_tickers

def download(global_tickers, start, end):
    """ Descargar datos de global tickers en un periodo determinado.
    Parameters    
    ----------------------------------------------------------------------------------------------    
    :param global_tickers: Lista de Tickers. 
    :param start: Fecha inicial.
    :param end: Fecha Final.
    Returns
    ----------------------------------------------------------------------------------------------  
    :return data: DataFrame con precios descargados. 
    """
    inicio = time.time()    

    # descarga masiva de precios de yahoo finance
    data = yf.download(global_tickers, start = "2017-08-21", end = "2020-08-22", actions = False,
                       group_by = "close", interval = "1d", auto_adjust = True, prepost = False, threads = True)
    
    # tiempo que se tarda
    print("Se tardó", time.time()- inicio, " Segundos.")
    
    return data
