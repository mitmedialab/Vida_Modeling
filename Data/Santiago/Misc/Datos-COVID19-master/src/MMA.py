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
import datetime as dt
import time
import pandas as pd
import sys
import glob
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

'''
1.- RM, con archivos xlsx, cada uno corresponde a una particula, y el archivo tiene un tab por año.
2.- gases para estaciones fuera de santiago
Dado el volumen (un dato por hora) y complejidad de los datos, la primera separacion sera por años.

'''



def prod43_no_header(fte, prod, year='2020'):
    print('Generando producto 43')
    particles = ['CO', 'MP2.5', 'MP10', 'NO2', 'O3', 'SO2']
    # particles = ['SO2']
    for each_particle in particles:
        input_path = fte + each_particle
        print('Processing ' + each_particle + ' from  ' + input_path + ' for year ' + year)
        xlsx_file = glob.glob(input_path + '/' + each_particle + '-' + year + '*.xlsx')
        # fail if there's no file or more than one per year
        if len(xlsx_file) > 1:
            print('Got more than one file for ' + year + ' no processing')

        elif len(xlsx_file) == 0:
            print('No files for ' + year + ' no processing')

        # otherwise process
        elif len(xlsx_file) == 1:
            print(xlsx_file[0])
            # encontramos solo un archivo para el año
            df = pd.read_excel(xlsx_file[0], header=None)

            # separamos header y datos

            # Asumo que despues de UTM_Norte vienen fechas
            last_header_row = df.index[df[0] == 'UTM_Norte'].tolist()[0]
            print('Data starts after row ' + str(last_header_row))
            # en header boto date y time, por eso el slice cuenta desde la columna 2
            header = df.loc[:last_header_row, :]
            header.at[0, 0] = 'Nombre de estacion'
            header.at[2, 0] = 'Codigo region'
            header.at[3, 0] = 'Comuna'
            header.at[4, 0] = 'Codigo comuna'
            # print(header.to_string())

            # guardamos la data
            data = df.loc[last_header_row + 1:, :]
            data = data[data[0].notna()]
            # print(data.head().to_string())
            data[0].replace(to_replace=' 00:00:00', value='', inplace=True, regex=True)
            data[1].replace(to_replace='24:00:00', value='00:00:00', inplace=True, regex=True)
            data[0] = data[0].astype(str)
            data[0] = data[0] + ' ' + data[1]
            # print(data.head().to_string())

            # En header y data podemos botar 1
            header = header.drop(columns=[1])
            data = data.drop(columns=[1])
            # print(header.to_string())

            # print(data.head().to_string())

            df = pd.concat([header, data])

            print(df.head(10).to_string())
            df.to_csv(prod + each_particle + '-' + year + '_std.csv', index=False, header=False)


def prod43_from_mma_api(usr, password, auth_url, url, prod):
    '''
    Cosultamos la API una vez cada semana, y nos traemos los ultimos 2 dias para sobreescribir.
    Los ultimos datos estan corregidos
    '''
    print('Querying MMA API for daily update of product 43')
    # necesitamos el año para saber en que archivo escribir.

    to_date = dt.datetime.now() - dt.timedelta(days=1)
    to_year = to_date.year

    # debemos actualizar semanalmente, respondio Marcelo Corral
    # https: // stackoverflow.com / questions / 18200530 / get - the - last - sunday - and -saturdays - date - in -python
    from_date = to_date - dt.timedelta(days=7)
    from_year = from_date.year
    print('We\'ll query from ' + str(from_date) + ' to ' + str(to_date))
    # BUT the API receives unix time
    a_week_ago_unix = round(time.mktime(from_date.timetuple()))
    now_unix = round(time.mktime(to_date.timetuple()))
    print('Unix: We\'ll query from ' + str(a_week_ago_unix) + ' to ' + str(now_unix))

    # usr and pass must be retrieve from github secrets
    # auth_url returns a cookie that must be passed then for the query
    data = {
        'username': usr,
        'password': password
    }
    s = requests.Session()
    # github action failing
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.post(auth_url, data=data)
    #cookie = cookie.json()['data']['authenticator']
    # get list of stations and metadata to build queries
    estaciones = pd.read_csv('../input/MMA/Estaciones.csv')
    estaciones = estaciones[estaciones['Key'].notna()]
    # print(estaciones.to_string())
    # la consulta es asi: https://sinca.mma.gob.cl/api/domain/SMA/timeserie/117+MPM25VAL
    # SSSRTPPPPLLL, donde:
    # SSS : Estación (código Airviro)
    # R : resolución de tiempo (código Airviro) + es hora, * es dia
    # T : tipo (v: crudo M: validado)
    # PPPP : parámetro (código Airviro)
    # LLL: Instancia, variación de serie de tiempo. Por ejemplo en las meteorológicas se usa para la altura.
    # Pero sirve para diferenciar series de tiempo según se requiera
    particulas = {'MP10': 'MPM10',
                  'MP2.5': 'MPM25',
                  'SO2': 'M0001',
                  'O3': 'M0008',
                  'NO2': 'M0003',
                  'CO': 'M0004'
                  }
    for each_particula in particulas:
        data_particula = []
        print('\nUpdating ' + each_particula)
        for index in estaciones.index:
            # debemos consultar VAL, respondio Marcelo Corral
            api_call = url + '/' + estaciones.loc[index, 'Key'] + '+' + particulas[each_particula] + 'VAL'
            print("Querying " + estaciones.loc[index, 'Nombre estacion'] + ' to ' + api_call)
            response = s.get(api_call, timeout=15)
            if response.status_code == 200:
                # for k in response.json():
                #     print(k)
                #     for l in response.json()[k]:
                #         print('\t' + l)
                # proper_data = response.json()['data']['sampleQueries']['links']['lastMonth'] + '/ds61'
                # proper_data = response.json()['data']['sampleQueries']['links']['yesterday'] + '/ds61'
                proper_data = api_call + '/' + str(a_week_ago_unix) + '/' + str(now_unix) + '/ds61'
                # print('Actual query ' + proper_data)
                proper_data = s.get(proper_data)
                #print(proper_data.json())
                # header from local metadata:
                header = {'Nombre de estacion': estaciones.loc[index, 'Nombre estacion'],
                          'Region': estaciones.loc[index, 'Region'],
                          'Codigo region': estaciones.loc[index, 'Codigo region'],
                          'Comuna': estaciones.loc[index, 'Comuna'],
                          'Codigo comuna': estaciones.loc[index, 'Codigo comuna'],
                          'UTM_Este': estaciones.loc[index, 'UTM_Este'],
                          'UTM_Norte': estaciones.loc[index, 'UTM_Norte']
                          }
                #print(header)
                # put the json above in a dataframe
                data = pd.DataFrame(proper_data.json()['data']['timeserie'])
                #data['Nombre estacion'] = estaciones.loc[index, 'Nombre estacion']
                data.rename(columns={'value': estaciones.loc[index, 'Nombre estacion']}, inplace=True)
                #transform time from YYYYmmdd HHMM to YYYY-mm-dd hh:MM:SS

                data['fecha'] = data['time'].map(lambda x: x[0:4] + '-' + x[4:6] + '-' + x[6:8])
                data['hora'] = data['time'].map(lambda x:  x[9:11] + ':' + x[11:13] + ':00')
                data['fecha'] = pd.to_datetime(data['fecha'])
                # Identify the hour 24 (!!!!!!) and move a day forward, and subtract an hour
                # a.- a day earlier
                check = data.loc[data['hora'] == '24:00:00']
                for idx in check.index:
                    data.at[idx, 'fecha'] = data.at[idx, 'fecha'] + dt.timedelta(days=1)
                # b.- the hour
                data.loc[data['hora'] == '24:00:00', 'hora'] = '00:00:00'

                #replace the former time with the corrected values
                data['time'] = data['fecha'].dt.strftime('%Y-%m-%d') + ' ' + data['hora']
                #print(data.to_string())
                data.drop(columns=['fecha', 'hora', 'statusCode'], inplace=True)

                # we should make sure we're writing on the file for this year
                data_particula.append(data)



            else:
                print('Instead of a status code 200, we got ' + str(response.status_code))


        # this goes to the file
        # df_particula = pd.DataFrame()
        # for j in data_particula:
        #     print(j.dtypes)
        #     df_particula.join(j)
        for j in range(0, len(data_particula)):
            #print(data_particula[i])
            if j == 0:
                final_df = data_particula[j]
                final_df['time'] = pd.to_datetime((final_df['time']))
            else:
                aux = data_particula[j]
                aux['time'] = pd.to_datetime(aux['time'])
                final_df = pd.merge(final_df, aux, on='time')

        #data_particula = pd.concat(data_particula, axis=1)
        #print(data_particula.to_string())
        #print(final_df)
        final_df.rename(columns={'time': 'Nombre de estacion'}, inplace=True)

        # read the file
        if from_year == to_year:
            file = prod + '/' + each_particula + '-' + str(to_year) + '_std.csv'
            print('Appending to ' + file)
            df_file = pd.read_csv(file)
            # append to the file
            df_file = pd.concat([df_file, final_df], axis=0, ignore_index=True)

            # Drop duplicates
            df_file['Nombre de estacion'] = df_file['Nombre de estacion'].astype(str)
            df_file = df_file.drop_duplicates(subset='Nombre de estacion', keep='last')

            df_file.to_csv(file, index=False)
        else:
            print('we jumped years!')
            file_from_year = prod + '/' + each_particula + '-' + str(from_year) + '_std.csv'
            print('Appending to ' + file_from_year)
            df_file1 = pd.read_csv(file_from_year)
            threshold = dt.datetime.strptime(str(to_year) +'-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            df_from_year = final_df[final_df['Nombre de estacion'] < threshold]
            # append to the file
            df_file1 = pd.concat([df_file1, df_from_year], axis=0, ignore_index=True)

            # Drop duplicates
            df_file1['Nombre de estacion'] = df_file1['Nombre de estacion'].astype(str)
            df_file1 = df_file1.drop_duplicates(subset='Nombre de estacion', keep='last')

            # sort values
            df_f1_headers = df_file1.iloc[0:6, :]
            df_f1_data = df_file1.iloc[6:, :]

            df_f1_data.sort_values(by=['Nombre de estacion'], inplace=True)
            print(df_file1.head(10).to_string())
            print(df_f1_headers.to_string())
            print(df_f1_data.head(5).to_string())
            df_file1 = pd.concat([df_f1_headers, df_f1_data])

            df_file1.to_csv(file_from_year, index=False)


            file_to_year = prod + '/' + each_particula + '-' + str(to_year) + '_std.csv'
            print('Appending to ' + file_to_year)
            df_file2 = pd.read_csv(file_to_year)
            df_to_year = final_df[final_df['Nombre de estacion'] >= threshold]
            # append to the file
            df_file2 = pd.concat([df_file2, df_to_year], axis=0, ignore_index=True)

            # Drop duplicates
            df_file2['Nombre de estacion'] = df_file2['Nombre de estacion'].astype(str)
            df_file2 = df_file2.drop_duplicates(subset='Nombre de estacion', keep='last')

            # sort values
            df_f2_headers = df_file2.iloc[0:6, :]
            df_f2_data = df_file2.iloc[6:, :]

            df_f2_data.sort_values(by=['Nombre de estacion'], inplace=True)

            df_file2 = pd.concat([df_f2_headers, df_f2_data])


            df_file2.to_csv(file_to_year, index=False)

if __name__ == '__main__':
    history = False
    if history:
        for i in range(2010, 2020):
            prod43_no_header('../input/MMA/', '../output/producto43/', year=str(i))

    else:
        #prod43_no_header('../input/MMA/', '../output/producto43/')
        if len(sys.argv) == 3:
            auth_url ='https://sinca.mma.gob.cl/api/auth.cgi'
            url = 'https://sinca.mma.gob.cl/api/domain/SMA/timeserie'
            prod43_from_mma_api(sys.argv[1], sys.argv[2], auth_url, url, '../output/producto43')
