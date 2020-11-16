import pandas as pd
import numpy as np
from itertools import groupby
import utils
import unidecode
import datetime as dt
import sys

'''
MIT License

Copyright (c) 2020 Faviola Molina

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
Los productos que son alimentados con estos inputs son:
50
"""


class UpdateOutput:
    def __init__(self, template_file, input_file, output_file):
        self.template_name = template_file
        self.input_file = input_file
        self.output_file = output_file

    def header_file(self):
        # for this case we use a template file and update the data
        df_base = pd.read_csv(self.template_name)
        df_base['Codigo region'] = df_base['Codigo region'].fillna(0)
        df_base['Codigo comuna'] = df_base['Codigo comuna'].fillna(0)
        df_base['Comuna'] = df_base['Comuna'].fillna(0)
        todrop = df_base.loc[df_base['Comuna'] == 0]
        df_base.drop(todrop.index, inplace=True)
        df_base['Codigo region'] = df_base['Codigo region'].astype(int)
        df_base['Codigo comuna'] = df_base['Codigo comuna'].astype(int)

        desconocido = df_base['Codigo comuna'] != 0
        df_base['Codigo comuna'].where(desconocido, '', inplace=True)

        self.Comp = df_base.loc[df_base['Comuna'] != 'Total']
        self.Comp.reset_index(inplace=True)
        utils.desconocidoName(self.Comp)

        for k in range(len(self.Comp)):
            if self.Comp.loc[k,'Codigo region'] < 10:
                self.Comp.loc[k,'Codigo region'] = '0' + str(self.Comp.loc[k,'Codigo region'])
            else:
                self.Comp.loc[k,'Codigo region'] = str(self.Comp.loc[k,'Codigo region'])

            if self.Comp.loc[k,'Codigo comuna'] != '':
                if self.Comp.loc[k,'Codigo comuna'] < 10000:
                    self.Comp.loc[k,'Codigo comuna'] = '0' + str(self.Comp.loc[k,'Codigo comuna'])
                else:
                    self.Comp.loc[k,'Codigo comuna'] = str(self.Comp.loc[k,'Codigo comuna'])

        self.comuna = self.Comp['Comuna']

    def new_input(self,serie):

        if serie == 'confirmados':
            k = 2
        elif serie == 'sospechosos':
            k = 3

        self.inputDF = pd.read_csv(self.input_file)

        self.inputDF = self.inputDF.fillna(0)

        utils.comunaName(self.inputDF)
        utils.regionDEISName(self.inputDF)

        idxDesconocido = self.inputDF.loc[self.inputDF['comuna_residencia'] == 'Ignorada'].index.values

        for i in idxDesconocido:
            region = self.inputDF['region_residencia'][i]
            unaccentedRegion = unidecode.unidecode(region)
            self.inputDF.loc[i, 'comuna_residencia'] = 'Ignorada ' + unaccentedRegion

            if region == "O’Higgins":
                self.inputDF.loc[i,'comuna_residencia'] = 'Ignorada O’Higgins'
                print(region,self.inputDF.loc[i,'comuna_residencia'])

        self.inputDF.set_index('comuna_residencia', inplace=True)

        columns_name = self.inputDF.columns.values

        maxSE = self.inputDF[columns_name[1]].max()
        minSE = self.inputDF[columns_name[1]].min()


        print(minSE,maxSE)
        lenSE = (pd.to_datetime(maxSE)-pd.to_datetime(minSE)).days + 1
        startdate = pd.to_datetime(minSE)
        date_list = pd.date_range(startdate, periods=lenSE).tolist()
        date_list = [dt.datetime.strftime(x, "%Y-%m-%d") for x in date_list]
        print(date_list)

        self.df = pd.DataFrame(np.zeros((len(self.comuna), lenSE)))

        dicts = {}
        keys = range(lenSE)
        #values = [i for i in range(lenSE)]

        for i in keys:
            dicts[i] = date_list[i]

        self.df.rename(columns=dicts, inplace=True)

        SE_comuna = self.inputDF[columns_name[1]]
        value_comuna = self.inputDF[columns_name[k]]

        i = 0
        for row in self.inputDF.index:
            idx = self.comuna.loc[self.comuna == row].index.values
            if idx.size > 0:
                col = SE_comuna[i]
                self.df[col][idx] = value_comuna[i].astype(int)

            i += 1

        j = 0

        



    def join(self,serie):

        df_output = pd.concat([self.Comp, self.df], axis=1)
        df_output.drop(columns=['index'], axis=1, inplace=True)

        nComunas = [len(list(group)) for key, group in groupby(df_output['Codigo region'])]

        identifiers = ['Region', 'Codigo region', 'Comuna', 'Codigo comuna']
        variables = [x for x in df_output.columns if x not in identifiers]

        begRow = 0

        for i in range(len(nComunas)):

            endRow = begRow + nComunas[i]

            firstList = df_output[identifiers].iloc[endRow - 1].values.tolist()
            firstList[2] = 'Total'
            firstList[3] = ''

            valuesTotal = df_output[variables][begRow:endRow].sum(axis=0).tolist()

            regionTotal = pd.DataFrame((firstList + valuesTotal), index=df_output.columns.values).transpose()

            if i < len(nComunas) - 1:
                blank_line = pd.Series(np.empty((len(regionTotal), 0)).tolist())

                regionTotal = pd.concat([regionTotal, blank_line], axis=0)
                regionTotal.drop(columns=0, axis=1, inplace=True)

            temp = pd.concat([df_output.iloc[begRow:endRow], regionTotal], axis=0)
            if i == 0:
                outputDF2 = temp
            else:
                outputDF2 = pd.concat([outputDF2, temp], axis=0)

            if i < len(nComunas) - 1:
                begRow = endRow

        outputDF2.reset_index(inplace=True)
        outputDF2.drop(columns=['index'], axis=1, inplace=True)
        outputDF2[variables] = outputDF2[variables].dropna()#.astype(int)

        print(outputDF2.head(20))
 
        outputDF2.dropna(how='all', inplace=True)
        todrop = outputDF2.loc[outputDF2['Comuna'] == 'Total']
        outputDF2.drop(todrop.index, inplace=True)

        name = self.output_file
        if serie == 'sospechosos':
            name = self.output_file.replace('_confirmadosPorComuna.csv','_sospechososPorComuna.csv')
 
        outputDF2.to_csv(name, index=False)
        outputDF2_T = outputDF2.T
        outputDF2_T.to_csv(name.replace('.csv', '_T.csv'), header=False)
        identifiers = ['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Poblacion']
        variables = [x for x in outputDF2.columns if x not in identifiers]
        outputDF2_std = pd.melt(outputDF2, id_vars=identifiers, value_vars=variables, var_name='Fecha', value_name='Defunciones')
        outputDF2_std.to_csv(name.replace('.csv', '_std.csv'), index=False)


if __name__ == '__main__':

    Update = UpdateOutput('../input/DistribucionDEIS/baseFiles/DEIS_template.csv',
                          '../input/DistribucionDEIS/df_deis.csv',
                          '../output/producto50/DefuncionesDEIS_confirmadosPorComuna.csv')

    Update.header_file()
    Update.new_input('confirmados')
    Update.join('confirmados')
    Update.new_input('sospechosos')
    Update.join('sospechosos')
