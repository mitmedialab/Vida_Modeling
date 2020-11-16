'''
MIT License

Copyright (c) 2020 Sebastian Cornejo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

"""
Los productos que salen del reporte diario son:
3
4
5
7
8
9
10
11
12
13
14
17
20
23
24
26
27
30
36
44
47
49
"""

import pandas as pd
from utils import *
from shutil import copyfile
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta
import numpy as np


def prod4(fte, producto):
    print('Generando producto 4')
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    output = producto + today + '-CasosConfirmados-totalRegional.csv'
    df = pd.read_csv(fte, quotechar='"', sep=',', thousands=r'.', decimal=",")
    df.rename(columns={'Unnamed: 0': 'Region'}, inplace=True)
    if 'Unnamed: 7' in df.columns:
        df.drop(columns=['Unnamed: 7'], inplace=True)

    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    regionName(df)
    df.at[16, 'Region'] = 'Se desconoce región de origen'
    df.at[17, 'Region'] = 'Total'
    # texttract reconoce 0 como o
    df.replace({'O': 0}, inplace=True)
    df.fillna('', inplace=True)
    numeric_columns = [x for x in df.columns if x != 'Region']
    for i in numeric_columns:
        df[i] = df[i].astype(str)
        # df[i] = df[i].replace({r'\.': ''}, regex=True)
        df[i] = df[i].replace({r'\,': '.'}, regex=True)

    df.to_csv(output, index=False)


def prod5(fte, producto):
    print('Generando producto 5')
    # necesito series a nivel nacional por fecha:
    # Casos nuevos con sintomas
    # Casos totales
    # Casos recuperados  #ya no se reporta
    # Fallecidos
    # Casos activos
    # Casos nuevos sin sintomas
    # Casos nuevos sin notificar
    # Casos activos confirmados

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    df_input_file = pd.read_csv(fte + 'CasosConfirmadosTotales.csv')
    df_input_file['Fecha'] = pd.to_datetime(df_input_file['Fecha'], format='%d-%m-%Y')
    # print(df_input_file.to_string())
    # las columnas son :
    # Casos totales acumulados  Casos nuevos totales  Casos nuevos con sintomas  Casos nuevos sin sintomas*  Casos nuevos sin notificar Fallecidos totales  Casos activos confirmados

    df_input_file.rename(columns={'Casos totales acumulados': 'Casos totales',
                                  'Casos nuevos totales': 'Casos nuevos totales',
                                  'Casos nuevos con sintomas': 'Casos nuevos con sintomas',
                                  'Casos nuevos sin sintomas*': 'Casos nuevos sin sintomas',
                                  'Fallecidos totales': 'Fallecidos'}, inplace=True)

    # print(timestamp)
    last_row = df_input_file[df_input_file['Fecha'] == timestamp]
    # print(last_row.to_string())

    df_output_file = pd.read_csv(producto)

    df_output_file = df_output_file.T
    df_output_file.columns = df_output_file.iloc[0]
    df_output_file.drop(df_output_file.index[0], inplace=True)

    df_output_file.index = pd.to_datetime(df_output_file.index, format='%Y-%m-%d')
    df_output_file.index.name = 'Fecha'
    # print(df_output_file.index)
    # print(last_row['Fecha'].values[0])
    if last_row['Fecha'].values[0] in df_output_file.index:
        print('Fecha was there, overwriting it')
        df_output_file.drop(last_row['Fecha'].values[0], axis=0, inplace=True)
        # print(df_output_file.to_string())
        last_row.index = last_row['Fecha']
        last_row.drop(columns=['Fecha'], inplace=True)
        df_output_file = df_output_file.append(last_row)
        # print(df_output_file.to_string())

    else:
        print('new date, adding row')
        last_row.index = last_row['Fecha']
        last_row.drop(columns=['Fecha'], inplace=True)
        df_output_file = df_output_file.append(last_row)

        ################################## Lo de Demian
        # Faltan  recuperados por FIS

    # el 2 de junio hubo un cambio: Casos activos y recuperados por FIS y FD se calculan a partir de ese dia.
    # antes de eso es None
    fecha_de_corte = datetime(2020, 6, 2)

    correccion_2020_06_17 = datetime(2020, 6, 17)

    for i in df_output_file.index:
        if i >= fecha_de_corte:
            # print(str(i))
            # Casos activos por FIS parten el 2 de Junio por definicion y corresponden a los casos activos del reporte diario
            df_output_file.loc[i, 'Casos activos por FIS'] = df_output_file.loc[i, 'Casos activos']
            # Recuperados FIS se calculan restando fallecidos y activos FIS
            df_output_file.loc[i, 'Casos recuperados por FIS'] = \
                df_output_file.loc[i, 'Casos totales'] - \
                df_output_file.loc[i, 'Casos activos'] - \
                df_output_file.loc[i, 'Fallecidos']
            # Falta casos activos y recuperados por FD: ocupar numeros antiguos para calcular
            fourteen_days = timedelta(days=14)

            # Casos activos por FD = casos activos hasta el 2 de Junio. Antes de eso se copian casos activos

            # df.loc[i, 'C'] = df.loc[i - 1, 'C'] * df.loc[i, 'A'] + df.loc[i, 'B']
            # print(i)
            if (i - fourteen_days) in df_output_file.index:
                # print('14 days ago is on the df')
                df_output_file.loc[i, 'Casos activos por FD'] = df_output_file.loc[i, 'Casos totales'] - \
                                                                df_output_file.loc[i - fourteen_days, 'Casos totales']
                if i == correccion_2020_06_17:
                    # activos de hoy = activos de ayer + casos de hoy - casos (t-14) - muertos hoy .  Les daría 75346 ...
                    print('Corrigiendo el 2020-06-17')
                    df_output_file.loc[i, 'Casos activos por FD'] = \
                        df_output_file.loc[i - timedelta(days=1), 'Casos activos por FD'] + \
                        df_output_file.loc[i, 'Casos nuevos totales'] - \
                        df_output_file.loc[i - fourteen_days, 'Casos nuevos totales'] - \
                        df_output_file.loc[i, 'Fallecidos'] + \
                        df_output_file.loc[i - timedelta(days=1), 'Fallecidos']
                    # print('Casos activos por FD hoy: ' + str(df_output_file.loc[i, 'Casos activos por FD']))
                    # print(
                    #     'Casos activos ayer: ' + str(df_output_file.loc[i - timedelta(days=1), 'Casos activos por FD']))
                    # print('Casoso nuevos totales hoy : ' + str(df_output_file.loc[i, 'Casos nuevos totales']))
                    # print('Casos totales 14 dias atras: ' + str(
                    #     df_output_file.loc[i - fourteen_days, 'Casos nuevos totales']))
                    # print('Fallecidos hoy: ' + str(df_output_file.loc[i, 'Fallecidos']))
                    # print('Fallecidos ayer: ' + str(df_output_file.loc[i - timedelta(days=1), 'Fallecidos']))
            else:
                print(str(i) + ' has no data 14 days ago')
                # df_output_file.loc[i, 'Casos activos por FD'] = df_output_file['Casos totales'] - \
                #                                    df_output_file.loc[i - fourteen_days_ago, 'Casos totales']

            # Es igual a recuperados hasta el 1 de junio (inclusive), desde el 2 se calcula
            # Recuperados FD se calculan restando fallecidos y activos FD
            df_output_file.loc[i, 'Casos recuperados por FD'] = (
                    df_output_file.loc[i, 'Casos totales'] -
                    df_output_file.loc[i, 'Casos activos por FD'] -
                    df_output_file.loc[i, 'Fallecidos'])

        # lo que pasa antes de la fecha de corte
        else:
            # Casos activos por FD = casos activos hasta el 2 de Junio. Antes de eso se copian casos activos
            df_output_file.loc[i, 'Casos activos por FD'] = df_output_file.loc[i, 'Casos activos']
            df_output_file.loc[i, 'Casos activos por FIS'] = np.NaN
            df_output_file.loc[i, 'Casos recuperados por FIS'] = np.NaN
            df_output_file.loc[i, 'Casos recuperados por FD'] = df_output_file.loc[i, 'Casos recuperados']

    ################################## Lo de Demian

    df_output_file.sort_index(inplace=True)
    totales = df_output_file.T

    # print(totales.to_string())
    # print(totales.columns[1:])

    ## esto es estandar
    # totales = pd.read_csv(producto)
    # print(totales.columns.dtype)
    totales.columns = totales.columns.astype(str)

    # print(totales.to_string())

    totales.to_csv(producto, index_label='Fecha')
    totales_t = totales.transpose()
    totales_t.to_csv(producto.replace('.csv', '_T.csv'))
    # print(totales.to_string())

    df_std = pd.melt(totales.reset_index(), id_vars='index', value_vars=totales.columns)
    # df_std = pd.read_csv(producto.replace('.csv', '_T.csv'))
    df_std.rename(columns={'index': 'Dato', 'value': 'Total'}, inplace=True)
    # print(df_std.to_string())
    df_std.to_csv(producto.replace('.csv', '_std.csv'), index=False)


def prod3_13_14_26_27_47(fte, fte2, ft3):
    # ------------------ input directory: CasosProbables. In Reporte Diario since 2020-06-21

    onlyfiles = [f for f in listdir(fte2) if isfile(join(fte2, f))]

    casosProbablesAcumulados = pd.DataFrame({'Region': [],
                                             'Fecha': []})
    casosActivosProbables = pd.DataFrame({'Region': [],
                                          'Fecha': []})

    onlyfiles.sort()
    for eachfile in onlyfiles:
        #print('processing ' + eachfile)
        date = eachfile.replace("-CasosProbables-totalRegional", "").replace(".csv", "")
        dataframe2 = pd.read_csv(fte2 + eachfile)

        # sanitize headers

        dataframe2.rename(columns={'Región': 'Region'}, inplace=True)
        dataframe2.rename(columns={'Casos  probables acumulados': 'Casos probables acumulados'}, inplace=True)
        dataframe2.rename(columns={' Casos probables acumulados': 'Casos probables acumulados'}, inplace=True)
        dataframe2.rename(columns={'Casos  probables  acumulados': 'Casos probables acumulados'}, inplace=True)

        dataframe2.rename(columns={'Casos  activos probables': 'Casos activos probables'}, inplace=True)
        dataframe2.rename(columns={' Casos activos probables': 'Casos activos probables'}, inplace=True)
        dataframe2.rename(columns={'Casos  activos  probables': 'Casos activos probables'}, inplace=True)

        if 'Casos probables acumulados' in dataframe2.columns:
            if casosProbablesAcumulados['Region'].empty:
                casosProbablesAcumulados[['Region', 'Fecha']] = dataframe2[['Region', 'Casos probables acumulados']]
                casosProbablesAcumulados.rename(columns={'Fecha': date}, inplace=True)
            else:
                casosProbablesAcumulados[date] = dataframe2['Casos probables acumulados']

        if 'Casos activos probables' in dataframe2.columns:
            if casosActivosProbables['Region'].empty:
                casosActivosProbables[['Region', 'Fecha']] = dataframe2[['Region', 'Casos activos probables']]
                casosActivosProbables.rename(columns={'Fecha': date}, inplace=True)
            else:
                casosActivosProbables[date] = dataframe2['Casos activos probables']

    # ------------- producto3 (before 2020-06-21 and addition to Tabla 1 in Reporte Diario)

    onlyfiles = [f for f in listdir(fte) if isfile(join(fte, f))]
    cumulativoCasosNuevos = pd.DataFrame({'Region': [],
                                          'Casos nuevos': []})
    cumulativoCasosTotales = pd.DataFrame({'Region': [],
                                           'Casos totales': []})
    cumulativoFallecidos = pd.DataFrame({'Region': [],
                                         'Fallecidos': []})
    casosNuevosConSintomas = pd.DataFrame({'Region': [],
                                           'Fecha': []})
    casosNuevosSinSintomas = pd.DataFrame({'Region': [],
                                           'Fecha': []})
    casosNuevosSinNotificar = pd.DataFrame({'Region': [],
                                            'Fecha': []})
    casosConfirmadosRecuperados = pd.DataFrame({'Region': [],
                                                'Fecha': []})
    casosActivosConfirmados = pd.DataFrame({'Region': [],
                                            'Fecha': []})

    onlyfiles.sort()
    onlyfiles.remove('README.md')
    for eachfile in onlyfiles:
        #print('processing ' + eachfile)
        date = eachfile.replace("-CasosConfirmados-totalRegional", "").replace(".csv", "")
        dataframe = pd.read_csv(fte + eachfile)
        # sanitize headers
        # print(eachfile)
        dataframe.rename(columns={'Región': 'Region'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  totales': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos totales ': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos totales': 'Casos nuevos'}, inplace=True)

        dataframe.rename(columns={'Casos  totales': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={' Casos totales': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={'Casos  totales  acumulados': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={'Casos totales acumulados ': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={'Casos totales acumulados': 'Casos totales'}, inplace=True)

        dataframe.rename(columns={' Casos fallecidos': 'Fallecidos'}, inplace=True)
        dataframe.rename(columns={'Fallecidos totales ': 'Fallecidos'}, inplace=True)
        dataframe.rename(columns={'Fallecidos totales': 'Fallecidos'}, inplace=True)

        dataframe.rename(columns={'Casos nuevos con síntomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos con síntomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  con  síntomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos con sintomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos con sintomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  con  sintomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos con sintomas ': 'Casos nuevos con sintomas'}, inplace=True)

        dataframe.rename(columns={'Casos nuevos sin síntomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin síntomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  síntomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos sin síntomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin síntomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  síntomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos sin sintomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin sintomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  sintomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos sin sintomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin sintomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  sintomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos sin sintomas* ': 'Casos nuevos sin sintomas'}, inplace=True)

        dataframe.rename(columns={'Casos nuevos sin notificar': 'Casos nuevos sin notificar'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin notificar': 'Casos nuevos sin notificar'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  notificar': 'Casos nuevos sin notificar'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos sin notificar**': 'Casos nuevos sin notificar'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin notificar**': 'Casos nuevos sin notificar'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  notificar**': 'Casos nuevos sin notificar'}, inplace=True)

        dataframe.rename(columns={'Casos  confirmados recuperados': 'Casos confirmados recuperados'}, inplace=True)
        dataframe.rename(columns={' Casos confirmados recuperados': 'Casos confirmados recuperados'}, inplace=True)
        dataframe.rename(columns={'Casos  confirmados  recuperados': 'Casos confirmados recuperados'}, inplace=True)

        dataframe.rename(columns={'Casos  activos confirmados': 'Casos activos confirmados'}, inplace=True)
        dataframe.rename(columns={' Casos activos confirmados': 'Casos activos confirmados'}, inplace=True)
        dataframe.rename(columns={'Casos  activos  confirmados': 'Casos activos confirmados'}, inplace=True)

        # if 'Se desconoce región de origen' in dataframe['Region']:
        dataframe = dataframe[dataframe['Region'] != 'Se desconoce región de origen']
        dataframe.reset_index(drop=True, inplace=True)

        if cumulativoCasosNuevos['Region'].empty:
            cumulativoCasosNuevos[['Region', 'Casos nuevos']] = dataframe[['Region', 'Casos nuevos']]
            cumulativoCasosNuevos.rename(columns={'Casos nuevos': date}, inplace=True)
            cumulativoCasosTotales[['Region', 'Casos totales']] = dataframe[['Region', 'Casos totales']]
            cumulativoCasosTotales.rename(columns={'Casos totales': date}, inplace=True)
        else:
            # print(dataframe.columns)
            cumulativoCasosNuevos[date] = dataframe['Casos nuevos']
            cumulativoCasosTotales[date] = dataframe['Casos totales']

        if 'Fallecidos' in dataframe.columns:
            if cumulativoFallecidos['Region'].empty:
                cumulativoFallecidos[['Region', 'Fallecidos']] = dataframe[['Region', 'Fallecidos']]
                cumulativoFallecidos.rename(columns={'Fallecidos': date}, inplace=True)
            else:
                cumulativoFallecidos[date] = dataframe['Fallecidos']

        if 'Casos nuevos con sintomas' in dataframe.columns:
            if casosNuevosConSintomas['Region'].empty:
                casosNuevosConSintomas[['Region', 'Fecha']] = dataframe[['Region', 'Casos nuevos con sintomas']]
                casosNuevosConSintomas.rename(columns={'Fecha': date}, inplace=True)
            else:
                casosNuevosConSintomas[date] = dataframe['Casos nuevos con sintomas']
        else:
            date2 = (pd.to_datetime(date)).strftime('%Y-%m-%d')
            if date2 < '2020-04-29':
                if casosNuevosConSintomas['Region'].empty:
                    casosNuevosConSintomas[['Region', 'Fecha']] = dataframe[['Region', 'Casos nuevos']]
                    casosNuevosConSintomas.rename(columns={'Fecha': date}, inplace=True)
                else:
                    casosNuevosConSintomas[date] = dataframe['Casos nuevos']

        if 'Casos nuevos sin sintomas' in dataframe.columns:
            if casosNuevosSinSintomas['Region'].empty:
                casosNuevosSinSintomas[['Region', 'Fecha']] = dataframe[['Region', 'Casos nuevos sin sintomas']]
                casosNuevosSinSintomas.rename(columns={'Fecha': date}, inplace=True)
            else:
                casosNuevosSinSintomas[date] = dataframe['Casos nuevos sin sintomas']

        if 'Casos nuevos sin notificar' in dataframe.columns:
            if casosNuevosSinNotificar['Region'].empty:
                casosNuevosSinNotificar[['Region', 'Fecha']] = dataframe[['Region', 'Casos nuevos sin notificar']]
                casosNuevosSinNotificar.rename(columns={'Fecha': date}, inplace=True)
            else:
                casosNuevosSinNotificar[date] = dataframe['Casos nuevos sin notificar']

        if 'Casos confirmados recuperados' in dataframe.columns:
            if casosConfirmadosRecuperados['Region'].empty:
                casosConfirmadosRecuperados[['Region', 'Fecha']] = dataframe[
                    ['Region', 'Casos confirmados recuperados']]
                casosConfirmadosRecuperados.rename(columns={'Fecha': date}, inplace=True)
            else:
                casosConfirmadosRecuperados[date] = dataframe['Casos confirmados recuperados']

        if 'Casos activos confirmados' in dataframe.columns:
            if casosActivosConfirmados['Region'].empty:
                casosActivosConfirmados[['Region', 'Fecha']] = dataframe[['Region', 'Casos activos confirmados']]
                casosActivosConfirmados.rename(columns={'Fecha': date}, inplace=True)
            else:
                casosActivosConfirmados[date] = dataframe['Casos activos confirmados']

        if date > '2020-07-02':

            dataframe.rename(columns={'Región': 'Region'}, inplace=True)
            dataframe.rename(columns={'Casos  probables acumulados': 'Casos probables acumulados'}, inplace=True)
            dataframe.rename(columns={'Casos probables acumulados ': 'Casos probables acumulados'}, inplace=True)
            dataframe.rename(columns={' Casos probables acumulados': 'Casos probables acumulados'}, inplace=True)
            dataframe.rename(columns={'Casos  probables  acumulados': 'Casos probables acumulados'}, inplace=True)

            dataframe.rename(columns={'Casos  activos probables': 'Casos activos probables'}, inplace=True)
            dataframe.rename(columns={'Casos activos probables ': 'Casos activos probables'}, inplace=True)
            dataframe.rename(columns={' Casos activos probables': 'Casos activos probables'}, inplace=True)
            dataframe.rename(columns={'Casos  activos  probables': 'Casos activos probables'}, inplace=True)

            if 'Casos probables acumulados' in dataframe.columns:
                # print(date, type(date))
                if casosProbablesAcumulados['Region'].empty:
                    casosProbablesAcumulados[['Region', 'Fecha']] = dataframe[['Region', 'Casos probables acumulados']]
                    casosProbablesAcumulados.rename(columns={'Fecha': date}, inplace=True)
                else:
                    casosProbablesAcumulados[date] = dataframe['Casos probables acumulados']

            if 'Casos activos probables' in dataframe.columns:
                if casosActivosProbables['Region'].empty:
                    casosActivosProbables[['Region', 'Fecha']] = dataframe[['Region', 'Casos activos probables']]
                    casosActivosProbables.rename(columns={'Fecha': date}, inplace=True)
                else:
                    casosActivosProbables[date] = dataframe['Casos activos probables']

    # estandarizar nombres de regiones
    regionName(casosProbablesAcumulados)
    regionName(casosActivosProbables)
    regionName(cumulativoCasosNuevos)
    regionName(cumulativoCasosTotales)
    regionName(cumulativoFallecidos)
    regionName(casosNuevosConSintomas)
    regionName(casosNuevosSinSintomas)
    regionName(casosNuevosSinNotificar)
    regionName(casosConfirmadosRecuperados)
    regionName(casosActivosConfirmados)
    cumulativoCasosNuevos_T = cumulativoCasosNuevos.transpose()
    cumulativoCasosTotales_T = cumulativoCasosTotales.transpose()
    cumulativoFallecidos_T = cumulativoFallecidos.transpose()
    casosNuevosConSintomas_T = casosNuevosConSintomas.transpose()
    casosNuevosSinSintomas_T = casosNuevosSinSintomas.transpose()
    casosNuevosSinNotificar_T = casosNuevosSinNotificar.transpose()
    casosConfirmadosRecuperados_T = casosConfirmadosRecuperados.transpose()
    casosActivosConfirmados_T = casosActivosConfirmados.transpose()
    casosProbablesAcumulados_T = casosProbablesAcumulados.transpose()
    casosActivosProbables_T = casosActivosProbables.transpose()

    #### PRODUCTO 3

    names = ['Casos acumulados', 'Casos nuevos totales', 'Casos nuevos con sintomas', 'Casos nuevos sin sintomas',
             'Casos nuevos sin notificar', 'Fallecidos totales', 'Casos confirmados recuperados',
             'Casos activos confirmados', 'Casos activos probables', 'Casos probables acumulados']
    frames = [cumulativoCasosTotales, cumulativoCasosNuevos, casosNuevosConSintomas, casosNuevosSinSintomas,
              casosNuevosSinNotificar, cumulativoFallecidos, casosConfirmadosRecuperados,
              casosActivosConfirmados, casosActivosProbables, casosProbablesAcumulados]

    for i in range(len(names)):

        list = [names[i]] * len(cumulativoCasosTotales)
        temp = pd.DataFrame.copy(frames[i])
        temp.insert(1, 'Categoria', list)

        if i == 0: TotalesPorRegion = temp
        if i > 0:
            TotalesPorRegion = pd.concat([TotalesPorRegion, temp], axis=0)

    TotalesPorRegion = TotalesPorRegion.fillna('')
    TotalesPorRegion_T = TotalesPorRegion.transpose()

    TotalesPorRegion.to_csv('../output/producto3/TotalesPorRegion.csv', index=False)
    TotalesPorRegion_T.to_csv('../output/producto3/TotalesPorRegion_T.csv', header=False)
    identifiers = ['Region', 'Categoria']
    variables = [x for x in TotalesPorRegion.columns if x not in identifiers]
    df_std = pd.melt(TotalesPorRegion, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Total')
    df_std.to_csv('../output/producto3/TotalesPorRegion_std.csv', index=False)

    cumulativoCasosTotales.to_csv('../output/producto3/CasosTotalesCumulativo.csv', index=False)
    cumulativoCasosTotales_T.to_csv('../output/producto3/CasosTotalesCumulativo_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in cumulativoCasosTotales.columns if x not in identifiers]
    df_std = pd.melt(cumulativoCasosTotales, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Total')
    df_std.to_csv('../output/producto3/CasosTotalesCumulativo_std.csv', index=False)

    #### PRODUCTO 13
    cumulativoCasosNuevos.to_csv('../output/producto13/CasosNuevosCumulativo.csv', index=False)
    cumulativoCasosNuevos_T.to_csv('../output/producto13/CasosNuevosCumulativo_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in cumulativoCasosTotales.columns if x not in identifiers]
    df_std = pd.melt(cumulativoCasosNuevos, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Total')
    df_std.to_csv('../output/producto13/CasosNuevosCumulativo_std.csv', index=False)

    #### PRODUCTO 14
    cumulativoFallecidos.to_csv('../output/producto14/FallecidosCumulativo.csv', index=False)
    cumulativoFallecidos_T.to_csv('../output/producto14/FallecidosCumulativo_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in cumulativoFallecidos.columns if x not in identifiers]
    df_std = pd.melt(cumulativoFallecidos, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Total')
    df_std.to_csv('../output/producto14/FallecidosCumulativo_std.csv', index=False)

    #### PRODUCTO 26
    casosNuevosConSintomas.to_csv('../output/producto26/CasosNuevosConSintomas.csv', index=False)
    casosNuevosConSintomas_T.to_csv('../output/producto26/CasosNuevosConSintomas_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in casosNuevosConSintomas.columns if x not in identifiers]
    df_std = pd.melt(casosNuevosConSintomas, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Casos confirmados')
    df_std.to_csv('../output/producto26/CasosNuevosConSintomas_std.csv', index=False)

    #### PRODUCTO 27
    casosNuevosSinSintomas.to_csv('../output/producto27/CasosNuevosSinSintomas.csv', index=False)
    casosNuevosSinSintomas_T.to_csv('../output/producto27/CasosNuevosSinSintomas_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in casosNuevosSinSintomas.columns if x not in identifiers]
    df_std = pd.melt(casosNuevosSinSintomas, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Casos confirmados')
    df_std.to_csv('../output/producto27/CasosNuevosSinSintomas_std.csv', index=False)

    #### PRODUCTO 47

    #pop = pd.read_csv(ft3)
    pop2 = pd.read_csv(ft3)
    aux = pop2.groupby(['Region', 'Codigo region'])['Poblacion'].sum()
    aux = aux.reset_index()
    regionName(aux)

    Total_row = {'Region': 'Total', 'Codigo region': np.NaN, 'Poblacion': aux['Poblacion'].sum()}
    aux = aux.append(Total_row, ignore_index=True)
    pop = aux

    mediamovil = pd.merge(pop, cumulativoCasosNuevos, on='Region', how='outer')
    #print(mediamovil.head(20).to_string())
    df_t = mediamovil.T[3:].rolling(7).mean()
    mediamovil = mediamovil.T[0:1]
    columnas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    # for i in columnas:
    for i in df_t.columns:
        df_t[i] = df_t[i].div(pop.iloc[i]['Poblacion'])
        df_t[i] = df_t[i].mul(100000)
        df_t[i] = df_t[i].round(1)
    df = mediamovil.append(df_t, ignore_index=False, sort=False)

    df.T.to_csv('../output/producto47/MediaMovil.csv', index=False)
    df.to_csv('../output/producto47/MediaMovil_T.csv', header=False)
    df_t = df.T

    identifiers = ['Region']
    variables = [x for x in df_t.columns if x not in identifiers]
    df_std = pd.melt(df.T, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Media movil')
    df_std.to_csv('../output/producto47/MediaMovil_std.csv', index=False)


def prod7_8(fte, producto):
    df = pd.read_csv(fte, dtype={'Codigo region': object})
    regionName(df)
    df = df.replace('-', '', regex=True)
    df_t = df.T
    df.to_csv(producto + '.csv', index=False)
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Region', 'Codigo region', 'Poblacion']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='numero')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod9_10(fte, producto):
    copyfile(fte, producto + '.csv')
    HospitalizadosUCIEtario_T = transpone_csv(producto + '.csv')
    HospitalizadosUCIEtario_T.to_csv(producto + '_T.csv', header=False)
    df = pd.read_csv(fte)
    identifiers = ['Grupo de edad']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='Casos confirmados')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod17(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Establecimiento', 'Examenes']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='Numero de PCR')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod20(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Ventiladores']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='numero')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod23(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Casos']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='Casos confirmados')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod24(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Tipo de cama']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='Casos confirmados')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod30(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Casos']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='Fecha', value_name='Casos confirmados')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod36(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Region', 'Categoria']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Numero')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod44(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Egresos semanales']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Egresos')
    df_std.to_csv(producto + '_std.csv', index=False)

def prod49(fte, fte2, producto):
    # massage casos nuevos diarios
    df2 = pd.read_csv(fte2, header=None).T
    df2 = df2[[0, 7]]
    df2 = df2[1:]
    df2.rename(columns={0: 'Fecha', 7: 'casos'}, inplace=True)

    # massage tests diarios
    df = pd.read_csv(fte, header=None).T
    df = df[[0, 8]]
    df = df[2:]
    df.rename(columns={0: 'Fecha', 8: 'pcr'}, inplace=True)

    # positividad
    positividad = pd.merge(df, df2, on='Fecha', how='left')
    positividad['positividad'] = positividad['casos'].astype(float).div(positividad['pcr'].astype(float)).round(4)

    # moving average
    positividad['mediamovil_positividad'] = positividad['positividad'].rolling(7).mean().round(4)

    #write
    positividad.index = positividad['Fecha']
    positividad.to_csv(producto + '_T.csv', header=True, index=False)
    positividad.T.to_csv(producto + '.csv', header=False, index=True)


    df_std = pd.melt(positividad, id_vars=['Fecha'], value_name='Total', var_name='Serie')
    #print(df_std.to_string())
    df_std.to_csv(producto + '_std.csv', index=False)




if __name__ == '__main__':
    prod4('../input/ReporteDiario/CasosConfirmados.csv', '../output/producto4/')
    prod5('../input/ReporteDiario/', '../output/producto5/TotalesNacionales.csv')

    print('Generando productos 3, 13, 14, 26 y 27')
    prod3_13_14_26_27_47('../output/producto4/', '../input/ReporteDiario/CasosProbables/',
                          '../input/Otros/InformacionComunas.csv')

    print('Generando producto 11')
    print('Generando producto 11: bulk_producto4.py hay un bug, debes generarlo a mano')
    # exec(open('bulk_producto4.py').read())
    #
    print('Generando producto 7')
    prod7_8('../input/ReporteDiario/PCR.csv', '../output/producto7/PCR')

    print('Generando producto 8')
    prod7_8('../input/ReporteDiario/UCI.csv', '../output/producto8/UCI')

    print('Generando producto 9')
    prod9_10('../input/ReporteDiario/HospitalizadosUCIEtario.csv', '../output/producto9/HospitalizadosUCIEtario')

    print('Generando producto 10')
    prod9_10('../input/ReporteDiario/FallecidosEtario.csv', '../output/producto10/FallecidosEtario')

    print('Generando producto 12')
    exec(open('bulk_producto7.py').read())

    print('Generando producto 17')
    prod17('../input/ReporteDiario/PCREstablecimiento.csv', '../output/producto17/PCREstablecimiento')

    print('Generando producto 20')
    prod20('../input/ReporteDiario/NumeroVentiladores.csv', '../output/producto20/NumeroVentiladores')

    print('Generando producto 23')
    prod23('../input/ReporteDiario/PacientesCriticos.csv', '../output/producto23/PacientesCriticos')

    print('Generando producto 24')
    prod24('../input/ReporteDiario/CamasHospital_Diario.csv', '../output/producto24/CamasHospital_Diario')

    print('Generando producto 30')
    prod30('../input/ReporteDiario/PacientesVMI.csv', '../output/producto30/PacientesVMI')

    print('Generando producto 36')
    prod36('../input/ReporteDiario/ResidenciasSanitarias.csv', '../output/producto36/ResidenciasSanitarias')

    print('Generando producto 44')
    prod44('../input/ReporteDiario/EgresosHospitalarios.csv', '../output/producto44/EgresosHospitalarios')

    print('Generando producto 49')
    prod49('../input/ReporteDiario/PCREstablecimiento.csv','../output/producto5/TotalesNacionales.csv', '../output/producto49/Positividad_Diaria_Media')
