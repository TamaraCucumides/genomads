import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly import graph_objects as go
from plotly.graph_objs import Layout
import plotly.express as px
import seaborn as sns

import shap

from genomaviz._utils import *
from genomaviz.colors import *


def correlation_plot(data, des, corrs_number=None, partition_corrs=2, thresh=0, method="spearman", activity_code = True):
    """
    :param data: dataframe con las variables a correlacionar
    :type data: pandas DataFrame
    :param des: nombre de la variable de salida
    :type des: str
    :param corrs_number: cantidad de correlaciones positivas / negativas
    :type corrs_number: int
    :param partition_corrs: cantidad de correlaciones sobresalientes en el grafico
    :type partition_corrs: int
    :param thresh: limite abs para las correlaciones graficadas (ej: considerar sobre 0.1)
    :type thresh: float
    :param method: tipo de correlacion, de acuerdo a .corr(method) ("pearson", "spearman", etc)
    :type method: str
    :param activity_code: False para mostrar traits sin codigo de juegos
    :type activity_code: bool
    """
    
    paleta_corrs = ["#FF80B5", "#FFD6E7", "#D6E4FF", "#80AAFF"][::-1]
    
    if corrs_number == None:
        rasgos_pos = list(
            data.corr(method)[des].nlargest(50).loc[data.corr(method)[des] > thresh].drop([des]).index
            )
        rasgos_neg = list(
            data.corr(method)[des].nsmallest(50).loc[data.corr(method)[des] < -thresh].index
            )
        
        corrs_number_pos = len(rasgos_pos)
        corrs_number_neg = len(rasgos_neg)
        
        num_pos = list(
            data.corr(method)[des].nlargest(50).loc[data.corr(method)[des] > thresh].drop([des])
            )
        num_neg = list(
            data.corr(method)[des].nsmallest(50).loc[data.corr(method)[des] < -thresh]
            )                   
        
    else:
        rasgos_pos = list(
            data.corr(method)[des].nlargest(50).loc[data.corr(method)[des].nlargest(50) > thresh].drop([des]).index
            )[:corrs_number]
        rasgos_neg = list(
            data.corr(method)[des].nsmallest(50).loc[data.corr(method)[des].nsmallest(50) < -thresh].index
            )[:corrs_number]

        corrs_number_pos = min(len(rasgos_pos), corrs_number)
        corrs_number_neg = min(len(rasgos_neg), corrs_number)
        
        num_pos = list(
            data.corr(method)[des].nlargest(50).loc[data.corr(method)[des].nlargest(50) > thresh].drop([des])
            )[:corrs_number_pos]
        num_neg = list(
            data.corr(method)[des].nsmallest(50).loc[data.corr(method)[des].nsmallest(50) < -thresh]
            )[:corrs_number_neg]
        
    veryhot_corrs = num_pos[:partition_corrs] + [0]*(corrs_number_pos + corrs_number_neg - partition_corrs)
    hot_corrs = [0]*partition_corrs + num_pos[partition_corrs:] + [0]*corrs_number_neg
    cold_corrs = [0]*corrs_number_pos + num_neg[partition_corrs:][::-1] + [0]*partition_corrs
    verycold_corrs = [0]*(corrs_number_pos + corrs_number_neg - partition_corrs) + num_neg[:partition_corrs][::-1]

    x = rasgos_pos + rasgos_neg[::-1]

    if not activity_code:
        try:
            for trait in range(len(x)):
                if x[trait] in t2c.keys():
                    x[trait] = x[trait][7:]
        except:
            pass

    sns.axes_style('white')
    sns.set_style('white')

    fig = plt.figure(figsize=(12,10))
    b = sns.barplot(x=veryhot_corrs,y=x,color=paleta_corrs[0])
    sns.barplot(x=hot_corrs,y=x, color=paleta_corrs[1])
    sns.barplot(x=cold_corrs,y=x, color=paleta_corrs[2])
    sns.barplot(x=verycold_corrs,y=x, color=paleta_corrs[3])


def funnel_plot(values=[], labels=[], **kwargs):
    fig = go.Figure(go.Funnel(
        y = labels,
        x = values, marker = {"color": palette,
        "line": {"width": [1,1,1,1,1], "color": palette}},
        textinfo = "value+percent initial"),
        layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'))
    return fig


def correlation_matrix(data, triangle=False):
    """
    :param data: dataframe con las variables a correlacionar
    :type data: pandas DataFrame
    :param triangle: booleano que indica si la quieres triangular o completa
    :type data: boolean
    """
    f, ax = plt.subplots(figsize=(10, 8))
    corr = data.corr()
    sns.heatmap(corr, cmap=sns.diverging_palette(0, 255, as_cmap=True), square=True, ax=ax, annot=True)
    plt.show()
    #TODO: add triangle mode


def binned_boxplot(data, x, y, num_bins=4):
    q1,q2,q3 = data[x].quantile([0.25,0.5,0.75])
    quartile = data.apply(lambda row: _quartilize_col(row, q1, q2, q3), axis=1)
    #TODO: plot and annotate bins, add custom amount of bins
    pass
    

def freq_matrix(x, y, data):
    """ TODO: Agregar fila de totales
    Matriz de frecuencia para dos variables
    :param x: nombre columna 1
    :type x: str
    :param y: nombre columna 2
    :type y: str
    :param data: dataframe con columnas a cruzar
    :type data: pandas DataFrame
    """
    matrix = pd.DataFrame()
    for xi in data[x].unique():
        count = pd.DataFrame(pd.Series(data.loc[data[x]==xi][y].value_counts(), name=xi))
        matrix = pd.concat([matrix, count], axis=1)
    matrix = matrix.fillna(0)
    return matrix

# """ [DEPRECATED]
# def stacked_barplot(data, stack_by, x = None, y = None, order = [], palette=saturated_palette):
#     """
#     data : la data como df
#     x : variable opcional (para apilar solo vertical)
#     y : variable opcional (para apilar solo horizontal)
#     stack_by : la variable con la que se agrupan las barras (como un groupby)
#     order : por si quieres que vayan con orden especifico las barras,
#         es una lista de strings con los valores unicos de la variable
#         stack_by (algo como ["nivel1", "nivel2", ...])

#     returns : plot
#     """
#     df_dict = {}
#     concat_list = []
    
#     if not x:
#         x = y

#     if order:
#         for unique in order:
#             df_dict[unique] = data.loc[data[x] == unique]
#             df_dict[unique][str(unique)] = data[x].map(lambda x: 100/df_dict[unique].shape[0])
#             df_dict[unique] = df_dict[unique].groupby(stack_by).sum().reset_index()
#             concat_list.append(df_dict[unique][str(unique)])
            
#     else:   
#         for unique in data[x].unique():
#             df_dict[unique] = data.loc[data[x] == unique]
#             df_dict[unique][str(unique)] = data[x].map(lambda x: 100/df_dict[unique].shape[0])
#             df_dict[unique] = df_dict[unique].groupby(stack_by).sum().reset_index()
#             concat_list.append(df_dict[unique][str(unique)])
        
#     pls = pd.concat(concat_list, axis = 1)

#     for i in range(1, pls.shape[0]):
#         pls.iloc[i] = pls.iloc[i]+pls.iloc[i-1]

#     if y:
#         for i in range(pls.shape[0], 0, -1):
#             pls2 = pls.iloc[i-1]
#             ax4 = sns.barplot(y=pls2.index, x=pls2.values, color = palette[i-1])

#         plt.xticks(ticks=[0,20,40,60,80,100], labels=["0%","20%","40%","60%","80%","100%"])
#     elif x:
#         for i in range(pls.shape[0], 0, -1):
#             pls2 = pls.iloc[i-1]
#             ax4 = sns.barplot(x=pls2.index, y=pls2.values, color = palette[i-1])

#         plt.yticks(ticks=[0,20,40,60,80,100], labels=["0%","20%","40%","60%","80%","100%"])      
        
#     #plt.show()
# """


def stacked_barplot(data, stack_by, x = None, y = None, stack_order = [], bar_order=[], palette=saturated_palette):
    """
    data : la data como df
    x : variable opcional (para apilar solo vertical)
    y : variable opcional (para apilar solo horizontal)
    stack_by : la variable con la que se agrupan las barras (como un groupby)
    stack_order : por si quieres que vayan con orden especifico las barras,
        es una lista de strings con los valores unicos de la variable
        stack_by (algo como ["nivel1", "nivel2", ...])

    returns : plot
    """
    if not bar_order:
        bar_order = x.unique()
        
    if not stack_order:
        stack_order = stack_by.unique()
        
    plot_data = pd.DataFrame()

    for bar in bar_order:
        bar_data = data.copy()
        bar_data = bar_data.loc[bar_data[x]==bar]
        bar_data = bar_data[[x, stack_by]]
        percentage = {st:bar_data.loc[bar_data[stack_by]==st].shape[0]/bar_data.shape[0]*100 for st in stack_order}
        percentage_data=pd.DataFrame(percentage.values(), columns=["%"])
        percentage_data[stack_by]=stack_order
        percentage_data[x]=bar
        for row in range(1, percentage_data.shape[0]):
            percentage_data["%"].iloc[row] += percentage_data["%"].iloc[row-1]
        plot_data = pd.concat([plot_data, percentage_data], ignore_index=True)
    
    for n, v in reversed(list(enumerate(stack_order))):
        if n > len(palette):
            color = n - len(palette)
        else:
            color = n
        sns.barplot(data=plot_data.loc[plot_data[stack_by]==stack_order[n]],
                    x = x, y="%", color=palette[color])


def stacked_kdeplot(x, group_by, data, palette=saturated_palette, order=None, legend=True, **kwargs):
    """ Graficos de densidad para múltiples clases
    
    :param x: Variable para comparar
    :type x: str
    :param group_by: Variable para separar clases
    :type group_by: str
    :param data: dataframe con los datos
    :type data: pandas DataFrame
    :param palette: paleta de colores, en hexa
    :type palette: list
    :param order: orden de las clases, por defecto: df[group_by].unique()
    :type order: list
    :param legend: True para mostrar leyendas de acuerdo a parametro order
    :type legend: bool
    :param kwargs: Argumentos opcionales para sns.kdeplot()
    :type kwargs: **kwargs
    """
    color = 0
    if not order:
        order = list(data[group_by].unique())
    for cls in order:
        sns.kdeplot(x=x, data=data.loc[data[group_by]==cls], color=palette[color], **kwargs)
        color += 1
        if color > 5:
            color = 0
    if legend:
        plt.legend(order)


def ABS_SHAP(df_shap, df):
    #import matplotlib as plt
    # Make a copy of the input data
    
    for col in df.columns:
        try:
            df = df.rename({col: c2t[col][7:]}, axis=1)

        except:
            try:
                if col == "Exp laboral banca":
                    df = df.rename({col: "Antes de trabajar en Fundación Génesis Empresarial,\n¿tenías experiencia laboral en banca o microfinanzas?"}, axis=1)
                elif col == "Exp laboral":
                    df = df.rename({col: "Antes de trabajar en Fundación Génesis Empresarial,\n¿tenías experiencia laboral?"}, axis=1)
            except:
                pass

    
    shap_v = pd.DataFrame(df_shap)
    feature_list = df.columns
    shap_v.columns = feature_list
    df_v = df.copy().reset_index().drop('index',axis=1)
    
    # Determine the correlation in order to plot with different colors
    corr_list = list()
    for i in feature_list:
        b = np.corrcoef(shap_v[i].astype(float), df_v[i].astype(float))[1][0]
        corr_list.append(b)
    corr_df = pd.concat([pd.Series(feature_list),pd.Series(corr_list)],
                        axis=1).fillna(0)

    # Make a data frame. Column 1 is the feature, and Column 2 is the 
    # correlation coefficient
    corr_df.columns  = ['Variable','Corr']
    corr_df['Sign'] = np.where(corr_df['Corr']>0,'#8080ff', '#ff66b3')
    
    # Plot it
    shap_abs = np.abs(shap_v)
    k=pd.DataFrame(shap_abs.mean()).reset_index()
    k.columns = ['Variable','SHAP_abs']
    k2 = k.merge(corr_df, left_on = 'Variable',
                 right_on='Variable', how='inner')
    k2 = k2.sort_values(by='SHAP_abs', ascending = True)
    colorlist = k2['Sign']
    ax = k2.plot.barh(x='Variable', y='SHAP_abs', color = colorlist, 
                      figsize=(5,6), legend=False)
    ax.set_xlabel("SHAP Value (Impacto positivo en azul)")
    
    return k2


def gender_plot(data, x, palette=palette):
    data.dropna(subset=[x]).loc[data[x] != "Genero no válido"][x].value_counts().plot.pie(autopct='%1.1f%%', colors = palette)
    plt.ylabel("")