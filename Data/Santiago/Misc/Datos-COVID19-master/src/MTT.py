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

import pandas as pd
from utils import *


def prod41(fte, prod):
    df_comuna = pd.read_csv(fte + 'TransaccionesBipComuna.csv')
    # No podemos normalizar estandar por comunas '-'
    df_dim_comunas = pd.read_excel("http://www.subdere.gov.cl/sites/default/files/documentos/CUT_2018_v04.xls",
                                   encoding="utf-8")
    df_dim_comunas["Comuna"] = df_dim_comunas["Nombre Comuna"].str.normalize("NFKD") \
        .str.encode("ascii", errors="ignore").str.decode("utf-8").str.lower().str.replace(' ', '')

    df_comuna["Comuna"] = df_comuna["Comuna"].str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8") \
        .str.lower().str.replace(' ', '')

    df_comuna = df_comuna.merge(df_dim_comunas, on="Comuna", how="outer")

    #drop all comunas without fecha
    df_comuna = df_comuna[df_comuna['Fecha'].notna()]

    #Get to Comuna proper name from Codigo comuna 2017
    df_comuna.loc[df_comuna.Comuna != '-', 'Comuna'] = df_comuna['Nombre Comuna']

    #drop redundant info
    df_comuna.drop(columns=['Código Región', 'Nombre Región', 'Código Provincia', 'Nombre Provincia', 'Nombre Comuna',
                            'Abreviatura Región'],
                   inplace=True)
    df_comuna.rename(columns={'Código Comuna 2018': 'Codigo comuna'}, inplace=True)

    #print(df_comuna.to_string())
    df_comuna = df_comuna[['Comuna', 'Codigo comuna', 'Transacciones', 'Fecha']]
    #este es el prod _std
    df_comuna.to_csv(prod + 'BIPComuna_std.csv', index=False)

    df_total = pd.read_csv(fte + 'TransaccionesBipTotal.csv')
    df_total.to_csv(prod + 'BIPTotal_std.csv', index=False)


def prod42(fte, prod):
    df = pd.read_csv(fte)
    #print(df.to_string())
    df.to_csv(prod + 'ViajesComunas_std.csv', index=False)


if __name__ == '__main__':
    print('generando producto 41')
    prod41('../input/MTT/', '../output/producto41/')

    print('generando producto 42')
    prod42('../input/MTT/ViajesComunasTransportePublico.csv', '../output/producto42/')