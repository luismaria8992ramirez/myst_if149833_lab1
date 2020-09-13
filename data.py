"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Contrast passive investment against active investment Carry out rebalancing policies       -- #
#    to maximize performance.                                                                            -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: luismaria8992ramirez                                                                      -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/luismaria8992ramirez/lab1_if691761-iteso.mx/blob/master/data.py                                                                     -- #
"""


# Importar librerías
import pandas as pd
import os

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
   
