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
import requests
import pandas as pd
from utils import *

def prod_48(url, user, password, prod):
    print('generando prod46')
    #print('asking to ' + url)
    #print('user: ' + '*' * len(user))
    #print('password: ' + '*' * len(password))
    r = requests.get(url, auth=(user, password))
    #print(r.json())
    #for each_fecha in r.json():
    #    print(each_fecha)
    df_std = pd.DataFrame(r.json())
    #print(df.head(20).to_string())
    #print(df.columns)
    df_std.columns = map(str.capitalize, df_std.columns)
    df_std.columns = df_std.columns.str.replace('_', ' ')
    df_std.rename(columns={'Region id': 'Codigo region'}, inplace=True)

    df_std['Fecha'] = df_std['Fecha'].str[:10]

    df_std['Region'] = df_std['Region'].str.replace('De ', '')
    df_std['Region'] = df_std['Region'].str.replace('Del ', '')
    regionName(df_std)

    #df es el _std
    #print(df_std.head(50).to_string())
    df_std.to_csv(prod + '_std.csv', index=False)

    df = df_std.set_index(['Fecha','Codigo region','Region', 'Servicio salud']).unstack(level=0)
    #print(df.head(20).to_string())
    data = []
    for each_value in df.columns.get_level_values(0).drop_duplicates().to_list():
        df_aux = df[each_value]
        df_aux['Serie'] = each_value
        data.append(df_aux)
    data = pd.concat(data)

    #ordenamos las columnas
    sorted_columns = ['Serie'] + [x for x in data.columns if x != 'Serie']
    data = data[sorted_columns]
    data.to_csv(prod + '.csv')

    data_t = data.T

    data_t.to_csv(prod + '_T.csv', index_label=False)




if __name__ == '__main__':
    if len(sys.argv) == 4:
        url = sys.argv[1]
        user = sys.argv[2]
        password = sys.argv[3]
        prod_48(url, user, password, '../output/producto48/SOCHIMI')

