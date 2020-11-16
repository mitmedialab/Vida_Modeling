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
Los productos que salen del las nuevas definiciones son:
37
"""

import pandas as pd


def prod37(fte,producto):
    print('Generando producto 37')
    df = pd.read_csv(fte)

    #split publicacion in serie and publicacion
    # new data frame with split value columns
    new = df["Publicacion"].str.split(pat="_", n=1, expand=True)

    # making separate first name column from new data frame
    df["Serie"] = new[0]

    # making separate last name column from new data frame
    df["Publicacion"] = new[1]


    identifiers = ['Serie', 'Publicacion']
    variables = [x for x in df.columns if x not in identifiers]
    var_aux = [x for x in df.columns if x not in identifiers + ['en verificación']]
    sorted_columns = identifiers + ['en verificación'] + var_aux
    df = df[sorted_columns]
    df[variables] = df[variables].fillna(0).astype(int)

    df.sort_values(by=['Publicacion'], inplace=True)
    df.to_csv(producto + '.csv', index=False)


    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    #print(df_t)

    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='Fecha', value_name='Numero defunciones')
    df_std['Numero defunciones'] = df_std['Numero defunciones'].fillna(0).astype(int)
    df_std.sort_values(by=['Fecha', 'Publicacion'], inplace=True)
    #print(df_std)
    df_std.to_csv(producto + '_std.csv', index=False)

if __name__ == '__main__':

    prod37('../input/NuevaDefDefunciones/DefuncionesDEIS.csv', '../output/producto37/Defunciones_deis')
