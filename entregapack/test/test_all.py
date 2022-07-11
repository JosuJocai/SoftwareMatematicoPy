from entregapack import discretizacion as dis
from entregapack import lec_esc as le
from entregapack import metricas as met
import numpy as np
import pandas as pd


def test_all():

    # ROC
    sample_arr = [True, False]
    bool_arr = np.random.choice(sample_arr, size=100)
    a = list(range(1,101))
    df = pd.DataFrame({'Nombre' : a,
                        'Bool' : bool_arr}, columns=['Nombre', 'Bool'])
    area = met.ROC(df)
    print(area)

    # ROC_plot
    # met.ROC_plot(df)

    # informacion_mutua_df
    df2 = pd.DataFrame({'frase': ['estas', 'como', 'no se', 'estas'],
                    'letras': ['a', 'b', 'c', 'd'],
                    'logic': [True, False, True, True],
                    'num': [3, 7, 96, 7]})
    i_f = met.informacion_mutua_df(df2)
    print(i_f)

    # varianza y varianza_df
    df1 = pd.DataFrame({'frase': [2,5,9,6],
                         'letras': [56,45,78,23],
                         'logic': [8,4,9,1],
                         'num': [3, 7, 96, 7]})
    v = met.varianza_df(df1)
    print(v)

    # correlacion_pearson y correlacion_pearson_df
    c = met.correlacion_pearson_df(df1)
    print(c)

    #normalize y normalize_df
    n= met.normalize_df(df1)
    print(v)

    df7 = pd.DataFrame({'c1': [43, 54, 69, 1, 3, 10],
                    'c2': [70, 89, 15, 37, 39, 84],
                    'c3': [22, 35, 67, 51, 9, 11],
                    'c4': [3, 7, 96, 7, 96, 45]})
    a = str(type(df7))
    discre = dis.discretize_general(df7, 3, "frecuency")

    v1 = [46, 3, 6, 72, 45, 92, 22]
    discre_v = dis.discretize_general(v1, 3, "width")

    # entropy y entropy_df
    e = met.entropy_df(df2)
    print(e)

    # entrada
    df = le.escribir_df("prueba.txt", sep=',', header=True)
    print(df)

    # salida
    le.leer_fichero(df=df, file="prueba1.txt", sep=',', header=True)


def main():
    test_all()

if __name__ == "__main__":
    main()