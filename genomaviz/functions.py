import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from genomaviz._utils import *


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

    b = sns.barplot(x=veryhot_corrs,y=x,color=paleta_corrs[0])
    sns.barplot(x=hot_corrs,y=x, color=paleta_corrs[1])
    sns.barplot(x=cold_corrs,y=x, color=paleta_corrs[2])
    sns.barplot(x=verycold_corrs,y=x, color=paleta_corrs[3])
    plt.show()

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