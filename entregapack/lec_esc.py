import pandas as pd
import numpy as np


def escribir_df(file, sep=";", header=False):
    """
    Descripcion:
        Dado un fichero file, un separador para las columnas sep y si estan los encabezados de las columnas
        en la primera fila, devuelve un dataframe con la información del fichero
    Parametros:
        file: Fichero de entrada.
        sep: Separador de las columnas en el fichero de entrada.
        header: Si existe en la primera fila del fichero los titulos de las columnas.
    Devuelve:
        Un dataframe con los datos del fichero."""
    f = open(file, "r")
    try:
        lineas = f.readlines()
        if header:
            titulos = lineas[0]
            head = titulos.split(sep)
            lineas = lineas[1:]
        total = []
        for linea in lineas:
            linea = linea.rstrip('\n')
            line_data = linea.split(sep)
            total += [line_data]
        if header:
            df = pd.DataFrame(data=total, columns=head)
        else:
            df = pd.DataFrame(data=total)
        return df
    finally:
        f.close()


def leer_fichero(df, file, sep=';', header=True):
    """
    Descripcion:
        Dado un dataframe, df, el nombre de un fichero file, un separador sep y si se quiere que se incluyan el nombre
        de las columnas en el fichero de salida. Crea un fichero con el nombre file y la información del dataframe df.
    Parametros:
        df: dataframe de entrada para escribir en el fichero.
        file: Fichero de salida.
        sep: Separador de las columnas en el fichero.
        header: Si se añaden los titulos del daframe en el fichero de salida.
    """
    string = ''
    if header:
        columnas = df.columns
        for i in range(len(columnas)):
            string += columnas[i]
            if (i+1) != len(df):
                string += sep
        string += '\n'         
    for i in range(len(df.columns)):
        for j in range(len(df)):
            string += str(df.iloc[j,i])
            if (j+1) != len(df):
                string += sep
        string += '\n'
    f = open(file, "w")
    try:
        f.write(string)
    finally:
        f.close()