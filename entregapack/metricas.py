from argparse import Namespace
from cmath import sqrt
from dis import dis
from statistics import mean, median
from xml.dom import IndexSizeErr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log

def __caracterizar(x, y):
    if x and y:
        return "TP"
    elif x and not(y):
        return "FN"
    elif not(x) and y:
        return "FP"
    else:
        return "TN"


def __valores_columna(x, y):

    v = pd.DataFrame({
        "TP" :[0],
        "TN" :[0],
        "FP" :[0],
        "FN" :[0] 
    })
    for i in range(len(x)):
        if x[i] and y[i]:
            v.iloc[0,0] += 1
        elif x[i] and not(y[i]):
            v.iloc[0, 3] += 1
        elif not(x[i]) and y[i]:
            v.iloc[0,2] += 1
        else:
            v.iloc[0,1] += 1
    return v


def __TPR(x):
    """Dado un vector con los TP, TN, FP y FN, se devuelve el TPR"""
    return x[0]/(x[0]+x[3])
    

def __FPR(x):
    """Dado un vector con los TP, TN, FP y FN, se devuelve el FPR"""
    return x[2]/(x[2]+x[1])


def __ROCprec(df):
    ncol = list(df.columns)
    name = ncol[0]
    df.sort_values(by=[name])
    for v_corte in range(0, df.shape[0] + 1):
        trues = [True]*v_corte
        falses = [False]*(df.shape[0] - v_corte)
        pred = trues + falses
        title = 'pred' + str(v_corte)
        df[title] = pred
    return df


def __metrics(df):
    v = pd.DataFrame({'TPR': [],
                        'FPR': []})
    for i in range(df.shape[0]):
        linea = df.iloc[i]
        df1 = pd.DataFrame({'TPR': [__TPR(linea)],
                        'FPR': [__FPR(linea)]})
        v = v.append(df1)
    return v


def ROCcalc(df):
    """
    Descripcion:
        Dado un dataframe calcula los valores TPR y FPR para la curva ROC

    Parametros:
        df: dataframe de dos columnas, siendo la segunda de ellas un vector logico

    Devuelve:
        Un dataframe con los TPR y los FPR.
        """
    df = __ROCprec(df)
    ncol = list(df.columns)
    df1 = pd.DataFrame({'TP': [],
                        'TN': [],
                        'FP': [],
                        'FN': []})
    for i in range(2, len(df.columns)):
        v1 = __valores_columna(df.iloc[:,1], df.iloc[:,i])
        df1 = df1.append(v1)
    dff = __metrics(df1)
    return dff
    

def ROC(df):
    """
    Descripcion:
        Dado un dataframe devuelve el area bajo la curva ROC que se genera.
    Parametros:
        df: Un dataframe de dos columnas siendo la segunda de ellas un vector logico.
    Devuelve:
        El area bajo la cuerva ROC.
    """
    df1 = ROCcalc(df)
    area = np.trapz(df1['TPR'], dx=1)
    return(area)


def ROC_plot(df):
    """
    Descripcion:
        Dado un dataframe muestra la curva ROC que se genera.
    Parametros:
        df: dataframe que contiene el TPR y el FPR
    """
    df = ROCcalc(__ROCprec(df))
    plt.plot(df['TPR'], df['FPR'])
    plt.show()

# CORRELACION E INFORMACION MUTUA

def informacion_mutua(x, y):
    """
    Descripcion:
        Calcula la información mutua para dos vectores.
    Parametros:
        x: vector con valores discretos
        y: vector con valores discretos
    Devuelve:
        La informacion mutua entre x e y.
        """
    d = {'col1': x, 'col2': y}
    df = pd.DataFrame(data=d)
    sum = 0
    filas = df.shape[0]
    for i in range(filas):
        dos = df[(df.iloc[:,0] == df.iloc[i,0]) & (df.iloc[:,1] == df.iloc[i,1])]
        pxy = dos.shape[0]/filas
        px = (df[(df.iloc[:,0] == df.iloc[i,0])].shape[0])/filas
        py = (df[(df.iloc[:,1] == df.iloc[i,1])].shape[0])/filas
        sparc = pxy*(log(pxy/(px*py),2))
        sum += sparc
    return sum


def informacion_mutua_df(df):
    """
        Descripcion:
            Calcula la información mutua entre todas las columnas del dataframe y las devuelve en un dataframe.
        Parametros:
            df: Un dataframe con valores discretos.
        Devuelve:
            Un data frame con la informacion mutua.
            """
    col = df.columns
    ncol = len(col)
    m = np.array([[0.0]*ncol]*ncol)

    for i in range(ncol):
        for j in range(i, ncol):
            if i != j:
                m[i][j] = informacion_mutua(df.iloc[:, i], df.iloc[:, j])
                m[j][i] = m[i][j]
            else:
                m[i][i] = informacion_mutua(df.iloc[:, i], df.iloc[:, j])
    dff = pd.DataFrame(m, columns=df.columns)
    return dff


def varianza(x):
    """
        Descripcion:
            Calcula la varianza de un vector.
        Parametros:
            x: Un vector con valores numericos.
        Devuelve:
            La varianza de x.
            """
    m = mean(x)
    r = 0
    for i in range(len(x)-1):
        r += pow((x[i] - m), 2)
    tam = len(x)
    return (r/tam)


def varianza_df(df):
    """
            Descripcion:
                Calcula la varianza por columnas de un dataframe
            Parametros:
                df: Un dataframe con valores numericos
            Devuelve:
                La varianza por columnas del dataframe.
                """
    return df.apply(varianza, axis=1)


def desviacion(x):
    """
            Descripcion:
                Calcula la desviación estándar de un vector.
            Parametros:
                x: Un vector numerico.
            Devuelve:
                La desviacion estandar de x.
                """
    return sqrt(varianza(x)).real


def correlacion_pearson(x, y):
    """
    Descripcion:
        Calcula la correlacion de pearson para dos vectores.
    Parametros:
        x: vector con valores numericos.
        y: vector con valores numericos.
    Devuelve:
        La correlacion de pearson entre x e y.
        """
    media_x = mean(x)
    media_y = mean(y)
    var_x = varianza(x)
    var_y = varianza(y)
    sd_x = sqrt(var_x).real
    sd_y = sqrt(var_y).real
    prod_xy = x*y
    media_xy = mean(prod_xy)
    sd_xy = media_xy - (media_x*media_y)
    return sd_xy/(sd_x*sd_y)


def correlacion_pearson_df(df):
    """
        Descripcion:
            Calcula la correlacion de pearson entre todas las columnas del dataframe y las devuelve en un dataframe.
        Parametros:
            df: Un dataframe con valores discretos.
        Devuelve:
            Un data frame con la informacion mutua.
            """
    col = df.columns
    ncol = len(col)
    m = np.array([[0.0]*ncol]*ncol)

    for i in range(ncol):
        for j in range(i, ncol):
            if i != j:
                m[i][j] = correlacion_pearson(df.iloc[:, i], df.iloc[:, j])
                m[j][i] = m[i][j]
            else:
                m[i][i] = correlacion_pearson(df.iloc[:, i], df.iloc[:, i])
    dff = pd.DataFrame(m, columns=df.columns, index=df.columns)
    return dff


def normalize(vec):
    """
        Descripcion:
            Dado un vector lo normaliza y lo devuelve normalizado
        Parametros:
            vec: Un vector numerico
        Devuelve:
            Un vector normalizado.
        """
    mean_vec = mean(vec)
    sd_vec = desviacion(vec)
    estandar = (vec - mean_vec)/sd_vec
    return estandar


def normalize_df(df):
    """
    Descripcion:
        Dado un dataframe df normaliza las columnas.
    Parametros:
        df: un dataframe numerico
    Devuelve:
        Un dataframe con las columnas normalizadas"""
    return df.apply(normalize, 0)


def entropy(x):
    """
    Descripcion:
        Calcula la entropia de un vector
    Parametros:
        x: vector numerico
    Devuelve:
        La entropia del vector
        """
    values = x.unique()
    suma = 0
    for i in range(len(x)-1):
        prob = len(x[x[:] == values[i]])/len(x)
        logarit = log(prob,2)
        res = -prob*logarit
        suma += res
    return suma


def entropy_df(df):
    """
    Descripcion:
        Calcula la entropía para cada columna de un dataframe df.
    Parametros:
        df: un dataframe numerico
    Devuelve:
        La entropia por cada columna."""
    sr = df.apply(entropy, axis=1)
    sr.index = df.columns
    return sr