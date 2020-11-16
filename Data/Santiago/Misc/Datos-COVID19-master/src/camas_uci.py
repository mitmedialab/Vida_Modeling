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

import boto3
import pandas as pd
from utils import *

class CamasUCI:
    def __init__(self, bucket, folder, access_key, secret_key, output):
        self.bucket = bucket
        self.folder = folder
        self.access_key = access_key
        self.secret_key = secret_key
        # init session
        self.session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name='us-east-1')
        self.s3 = self.session.resource('s3')
        self.actual_bucket = self.s3.Bucket(self.bucket)

        # store used variables
        self.output = output
        self.last_added = None
        self.date = None
        self.tables = None
        self.dataframes = None

    def get_last_camas_xlsx(self):
        get_last_modified = lambda obj: int(obj.last_modified.strftime('%s'))

        objs = [obj for obj in self.actual_bucket.objects.filter(Prefix=self.folder) if 'xlsx' in obj.key]

        objs = [obj for obj in sorted(objs, key=get_last_modified)]

        self.last_added = objs[-1]
        print('last added file is: ' + self.last_added.key)

    def last_file_to_csv(self):
        file_path = self.last_added.key

        s3_client = boto3.client('s3',
                                 aws_access_key_id=self.access_key,
                                 aws_secret_access_key=self.secret_key)

        obj = s3_client.get_object(Bucket=self.bucket, Key=file_path)

        df_uci_habilitada = pd.read_excel(obj['Body']._raw_stream.data, sheet_name='UCI HABILITADA')
        df_uci_habilitada.rename(columns={'Camas UCI habilitadas': 'Region'}, inplace=True)
        regionName(df_uci_habilitada)
        df_uci_habilitada = df_uci_habilitada[df_uci_habilitada['Region'].notna()]
        df_uci_habilitada['Serie'] = 'Camas UCI habilitadas'
       #print(df_uci_habilitada.to_string())

        df_uci_covid = pd.read_excel(obj['Body']._raw_stream.data, sheet_name='UCI OCUPADA COVID')
        df_uci_covid.rename(columns={'Camas UCI ocupadas COVID-19': 'Region'}, inplace=True)
        regionName(df_uci_covid)
        df_uci_covid = df_uci_covid[df_uci_covid['Region'].notna()]
        df_uci_covid['Serie'] = 'Camas UCI ocupadas COVID-19'
        #print(df_uci_covid.to_string())

        df_uci_no_covid = pd.read_excel(obj['Body']._raw_stream.data, sheet_name='UCI OCUPADA NO COVID')
        df_uci_no_covid.rename(columns={'Camas UCI ocupadas no COVID-19': 'Region'}, inplace=True)
        regionName(df_uci_no_covid)
        df_uci_no_covid = df_uci_no_covid[df_uci_no_covid['Region'].notna()]
        df_uci_no_covid['Serie'] = 'Camas UCI ocupadas no COVID-19'
        #print(df_uci_no_covid.to_string())

        df_camas_base = pd.read_excel(obj['Body']._raw_stream.data, sheet_name='CAMAS BASE')
        df_camas_base.rename(columns={'Camas base (2019)': 'Region'}, inplace=True)
        regionName(df_camas_base)
        df_camas_base = df_camas_base[df_camas_base['Region'].notna()]
        df_camas_base['Serie'] = 'Camas base (2019)'
        #print(df_camas_base.to_string())


        result = pd.concat([df_uci_habilitada, df_uci_covid, df_uci_no_covid, df_camas_base])


        identifiers = ['Region', 'Serie']
        variables = [x for x in result.columns if x not in identifiers]

        for i in range(len(variables)):
            result.rename(columns={variables[i]: variables[i].date()}, inplace=True)
            variables[i] = variables[i].date()

        result = result[identifiers + variables]
        result.to_csv(self.output + '.csv', index=False)

        df_t = result.T
        df_t.to_csv(self.output + '_t.csv', header=False)

        df_std = pd.melt(result, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                         value_name='Casos')

        df_std.to_csv(self.output + '_std.csv', index=False)

if __name__ == '__main__':
    if len(sys.argv) == 4:
        my_bucket_name = sys.argv[1]
        my_access_key = sys.argv[2]
        my_secret_key = sys.argv[3]
        my_camasUCI = CamasUCI(my_bucket_name, 'home/Minsal/CamasUCI', my_access_key, my_secret_key, '../output/producto52/Camas_UCI')
        my_camasUCI.get_last_camas_xlsx()
        my_camasUCI.last_file_to_csv()
