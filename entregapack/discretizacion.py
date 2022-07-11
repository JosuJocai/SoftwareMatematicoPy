import numpy as np
import pandas as pd

def __categorize(x, npoints):
    tam = len(npoints) - 1
    for i in range(tam):
        if x > npoints[i] and x <= npoints[i+1]:
            res = 'I' + str(i+1)
            n = '(' + str(npoints[i]) + ', ' + str(npoints[i+1]) + ']'
            return [res, n]
    if x > npoints[tam]:
        res = 'I' + str((tam+1))
        n = '(' + str(npoints[tam]) + ', Infty)'
    else:
        res = 'I0'
        n = '(-Infty, ' + str(npoints[0]) + ']'
    return [res, n]


def __discretize(x, cut_points):
    nombres = [('I'+ str(i)) for i in range(len(x))]
    df = pd.DataFrame(columns = nombres)
    names = []
    values = []
    for i in range(len(x)):
        col = 'I'+str(i)
        result = __categorize(x[i], cut_points)
        names += [result[1]]
        values += [result[0]]
    df2 = df.set_axis(names, axis=1, inplace=False)
    zip_iterator = zip(names, values)
    a_dictionary = dict(zip_iterator)
    serie = pd.Series(a_dictionary, index=names)
    df2 = df2.append(serie, ignore_index=True)
    return df2


def __discretizeEW(x, num_bins):
    mi = min(x)
    ma = max(x)
    interval = (ma - mi)/num_bins
    inames = [mi + (interval*i) for i in range(num_bins)]
    cut_points = inames[1:]
    return __discretize(x, cut_points)


def __discretizeEF(x, num_bins):
    x_num = np.sort(x)
    tam = len(x)
    num = int(tam/num_bins)
    cont = tam % num_bins
    a_cont = 0
    arr = []
    for i in range(num_bins):
        if cont != 0:
            for j in range((i * num) + a_cont, ((i + 1) * num)+1+a_cont):
                if (j+1) == (((i + 1) * num)+1+a_cont):
                    arr += [x_num[j]]
            cont -= 1
            a_cont += 1  
        else:
            for j in range((i * num) + a_cont, ((i + 1) * num)+a_cont):
                if j+1 == (((i + 1) * num)+a_cont):
                    arr += [x_num[j]]
    return __discretize(x, arr[:-1])


def discretize_vector(x, num, method):
    if method != "frecuency" and method != "width":
        raise Exception(method + "method does not exist.")
    else:
        if method == "frecuency":
            return __discretizeEF(x, num)
        else:
            return __discretizeEW(x, num)


def discretize_df(df, num, method):
    d  = []
    col = df.columns
    ncol = len(col)
    for i in range(ncol):
        v = df.iloc[:, i]
        new_v = discretize_vector(v, num, method)
        arr = new_v.iloc[0, :].array
        d.append(arr)
    ddf = pd.DataFrame(data=d)
    return ddf.transpose()


def discretize_general(df, num, method):
    """
    Descripcion:
        Discretiza un data frame o un vector por diferentes metodos
    Parametros:
        df: data frame o vector a discretizar
        num: numero de intervalos
        method: metodo de discretizacion, "frecuency" (equal frecuency) o "width" (equal width).
    Devuelve:
        El data frame o vector discretizado.
    """
    if isinstance(df, pd.DataFrame):
        return discretize_df(df, num, method)
    elif isinstance(df, pd.Series) or isinstance(df, list):
        return discretize_vector(df, num, method)
    else:
        raise Exception(df + "Tiene que ser un dataframe, un series o una lista.")