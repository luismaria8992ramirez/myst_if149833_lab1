"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Contrast passive investment against active investment Carry out rebalancing policies       -- #
#    to maximize performance.                                                                            -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: luismaria8992ramirez                                                                     -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository:https://github.com/luismaria8992ramirez/lab1_if691761-iteso.mx/blob/master/visualizations.py                                                                   -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
def plot_rends_pasiva(precios,rends,k,cash_proporcion, Plot = True):
    
    """ Esta función realizará el plot de los rendimientos simples y acumulados en la inversión activa.
        
        Parameters    
        ----------------------------------------------------------------------------------------------    
        :param precioss: DataFrame con cambios en los precios.
        :param rends: Lista de rendimientos.
        :param k: Inversión.
        :param cash_proporcion: Dinero que se mantuvo en cash.
        :param Plot: Realizar el plot en una ventana externa.
        
        Returns
        ----------------------------------------------------------------------------------------------
        :return  
    """

    trace = go.Scatter(x=precios.index[1:],y = (1+np.array(rends[1:]))*(k)+k*cash_proporcion, mode = "markers+lines", name = "Rendimiento en Periodos")
    trace1 = go.Scatter(x=precios.index[1:],y = (1+np.cumsum(rends[1:]))*k+k*cash_proporcion, mode = "markers+lines", name = "Rendimiento en Periodos Acumulado")
    data = [trace, trace1]
    layout = go.Layout(title  = "Plot de rendimientos simples y acumulados",
                       hovermode = "closest", xaxis = {"title":"Rendimiento"}, yaxis = {"title":"Fechas"})
    fig = go.Figure(data = data, layout = layout) 
    if Plot:
        pyo.plot(fig, filename = "Lines.html")
    fig.show()

def plot_rends_activa(ajustes,rr,k,cash_p, Plot = True):
    
    """ Esta función realizará el plot de los rendimientos simples y acumulados en la inversión activa.
        
        Parameters    
        ----------------------------------------------------------------------------------------------    
        :param ajustes: DataFrame con cambios en los precios.
        :param rr: Lista de rendimientos.
        :param k: Inversión.
        :param cash_p: Dinero que se mantuvo en cash.
        :param Plot: Realizar el plot en una ventana externa.
        
        Returns
        ----------------------------------------------------------------------------------------------
        :return  
    """
    trace = go.Scatter(x=ajustes.index,y = (1+np.array(rr[1:]))*(k)+k*cash_p, mode = "markers+lines", name = "Rendimiento en Periodos")
    trace1 = go.Scatter(x=ajustes.index,y = (1+np.cumsum(rr[1:]))*k+k*cash_p, mode = "markers+lines", name = "Rendimiento en Periodos Acumulado")
    data = [trace, trace1]
    layout = go.Layout(title  = "Plot de rendimientos simples y acumulados (Gestión Activa)",
                       hovermode = "closest", xaxis = {"title":"Rendimiento"}, yaxis = {"title":"Fechas"})
    fig = go.Figure(data = data, layout = layout) 
    if Plot:
        pyo.plot(fig, filename = "Lines.html")
    fig.show()
