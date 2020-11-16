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
import sys

import pandas as pd
import requests
from datetime import datetime

def prod40(fte, prod):
    df = pd.read_csv(fte, encoding='latin-1')

    #drop Region = Nan: includes all invalid dates
    df = df[df['Region_origen'].notna()]

    df['Cod_region_origen'] = df['Cod_region_origen'].astype(int)
    df['Cod_region_destino'] = df['Cod_region_destino'].astype(int)

    #stardardize fechas
    df['Inicio_semana'] = pd.to_datetime(df['Inicio_semana'], format='%d-%m-%Y')
    df['Fin_semana'] = pd.to_datetime(df['Fin_semana'], format='%d-%m-%Y')
    df['Inicio_semana'] = df['Inicio_semana'].astype(str)
    df['Fin_semana'] = df['Fin_semana'].astype(str)


    #drop columnas Año y mes
    df.drop(columns=['Año', 'Mes'], inplace=True)

    print(df.to_string())
    df.to_csv(prod + 'TransporteAereo_std.csv', index=False)

def prod40_from_API(url, api_key, prod):
    print('Generating prod40 from API')
    response = requests.get(url + api_key)
    my_list = response.json()['aéreo nacional - movimientos y pasajeros']

    df = pd.DataFrame(my_list)
    # drop unused columns
    df.drop(columns=['anio', 'mes'], inplace=True)

    df_localidades = pd.read_csv('../input/JAC/JAC_localidades.csv')

    # add to origen codigo_region, y region
    df_aux = pd.merge(df, df_localidades, left_on='origen', right_on='Localidad')


    df_aux.rename(columns={'semana': 'Semana',
                           'inicioSemana': 'Inicio_semana',
                           'finsemana': 'Fin_semana',
                           'origen': 'Origen',
                           'destino': 'Destino',
                           'operaciones': 'Operaciones',
                           'pasajeros': 'Pasajeros',
                           'Region': 'Region_origen',
                           'Cod_region': 'Cod_region_origen'}, inplace=True)

    df_aux.drop(columns='Localidad', inplace=True)



    # add to destino codigo_region y region
    df_aux = pd.merge(df_aux, df_localidades, left_on='Destino', right_on='Localidad')

    df_aux.rename(columns={'Region': 'Region_destino',
                           'Cod_region': 'Cod_region_destino'}, inplace=True)

    df_aux.drop(columns='Localidad', inplace=True)

    #sort columnas
    columns = ['Semana', 'Inicio_semana', 'Fin_semana',
               'Origen', 'Cod_region_origen', 'Region_origen',
               'Destino', 'Cod_region_destino', 'Region_destino',
               'Operaciones', 'Pasajeros']
    df_aux = df_aux[columns]

    #fechas estan en dd-mm-YYYY
    for i in ['Inicio_semana', 'Fin_semana']:
        df_aux[i] = pd.to_datetime(df_aux[i], format='%d-%m-%Y')

    df_aux.to_csv(prod + '_std.csv', index=False)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = 'https://api.desarrolladores.observatoriologistico.cl/aereo-nacional/v1/movimientosypasajeros.json/?auth_key='
        api_key = sys.argv[1]
        prod40_from_API(url, api_key, '../output/producto40/TransporteAereo')
    else:
        print('Generating prod40 from CSV')
        prod40('../input/JAC/TransporteAereo.csv', '../output/producto40/')

