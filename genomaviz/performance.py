import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from genomaviz.colors import *

def hiring_stats(df, fit, hired_col, hired_indicator="HIRED"):
    hired = df[df[hired_col]==hired_indicator]
    hired_mean_fit = round(hired[fit].mean(),1)
    hired_recommended = len(hired[hired[fit]>=85])
    hired_maybe = len(hired[hired[fit]>=60]) - hired_recommended
    hired_no = len(hired[hired[fit]<=60])
    print(f"REPORTE DE CONTRATACIONES \nFit promedio contratados: {hired_mean_fit}\n\
        Contratados recomendados: {hired_recommended} ({hired_recommended/len(hired)})\n\
        Contratados quizás: {hired_maybe} ({hired_maybe/len(hired)})\n\
        Contratados no recomendados: {hired_no} ({hired_no/len(hired)})")

def performance_stats(df, fit, performance, type='binary', convert='binary'):
    if type=='binary':
        good_perf = df[df[performance]==1]
        bad_perf = df[df[performance]==0]
        fit_good_perf = round(good_perf[fit].mean(),2)
        fit_bad_perf = round(bad_perf[fit].mean(),2)
        print(f"REPORTE DE EVALUACION DE CONTRATADOS\n\
            Promedio de fit contratados de alto desempeño: {fit_good_perf}\n\
            Promedio de fit contratados de bajo desempeño: {fit_bad_perf}\n\
            Contratados de alto desempeño recomendados: {good_perf[good_perf[fit]>=85]}\n\
            Contratados de alto desempeño quizas: {good_perf[good_perf[fit]<85 & good_perf[fit]>=60]}\n\
            Contratados de alto desempeño no recomendados: {good_perf[good_perf[fit]<60]}\n\
            Contratados de bajo desempeño recomendados: {bad_perf[bad_perf[fit]>=85]}\n\
            Contratados de bajo desempeño quizas: {bad_perf[bad_perf[fit]<85 & bad_perf[fit]>=60]}\n\
            Contratados de bajo desempeño no recomendados: {bad_perf[bad_perf[fit]<60]}\n")
    elif type=='quartile':
        q1 = df[df[performance]==1]
        q2 = df[df[performance]==2]
        q3 = df[df[performance]==3]
        q4 = df[df[performance]==4]
        mean_q1 = q1[fit].mean()
        mean_q2 = q2[fit].mean()
        mean_q3 = q3[fit].mean()
        mean_q4 = q4[fit].mean()
        print(f"REPORTE DE EVALUACION DE CONTRATADOS\n\
            Promedio de fits\n\
            Q1: {mean_q1}  Q2: {mean_q2}  Q3: {mean_q3}  Q4:{mean_q4} \n\
            Contratados Q1\n \
            Recomendados:{q1[q1[fit]>=85]}    Quizas:{q1[q1[fit]>=60 & q1[fit]<85]}  No recomendados:{q1[q1[fit]<60]} \n\
            Contratados Q2 \n\
            Recomendados:{q2[q2[fit]>=85]}    Quizas:{q2[q2[fit]>=60 & q2[fit]<85]}  No recomendados:{q2[q2[fit]<60]} \n\
            Contratados Q3\n\
            Recomendados:{q3[q3[fit]>=85]}    Quizas:{q3[q3[fit]>=60 & q3[fit]<85]}  No recomendados:{q3[q3[fit]<60]} \n\
            Contratados Q4 \n\
            Recomendados:{q4[q4[fit]>=85]}    Quizas:{q4[q4[fit]>=60 & q4[fit]<85]}  No recomendados:{q4[q4[fit]<60]} \n")
    elif type=='numeric':
        if convert == 'binary':
            df_converted = _binarize_col()
            performance_stats(df_converted, fit, performance)
        else:
            df_converted = _quartilize_col()
            performance_stats(df_converted, fit, performance, type='quartile')


def hiring_plot(df, fit, hired_col='Estado', hired_status='HIRED', kind='pie'):
    hired = df[df[hired_col]==hired_status]
    recomendation = hired.apply(lambda row: _recommendation_col(row, fit), axis=1)
    counts = recomendation.value_counts()
    if kind == 'pie':
        #TODO: fix color assignation and add legend and title
        plt.figure()
        plt.pie(counts, colors = traffic_light, autopct='%.0f%%')
        plt.show()
        return 
    elif kind == 'pymetrics':
        pass
    elif kind == 'bar':
        plt.figure()
        sns.barplot(recomendation, order=["Recomendado", "Quizás", "No recomendado"], palette=traffic_light)
        plt.show()
        #TODO: add barplot with hue status (hired vs all, but with proportion instead of count)
    else:
        pass


def performance_plot(df, fit, performance, type='binary'):
    if type=='binary':
        pass
    elif type=='quartile':
        pass
    else:
        pass


def _binarize_col(row, median):
    if row <= median:
        return 0
    elif row > median:
        return 1
    return ""


def _quartilize_col(row, q1, q2, q3):
    if row <= q1:
        return 1
    elif row <= q2:
        return 2
    elif row <= q3:
        return 3
    elif row > q3:
        return 4
    else:
        return ""


def _recommendation_col(row, fit):
    if row[fit]>=85:
        return "Recomendado"
    elif row[fit]>=60:
        return "Quizás"
    elif row[fit]<60:
        return "No recomendado"


