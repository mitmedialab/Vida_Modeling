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
import requests
from unidecode import unidecode

"""
Utilidades genéricas
"""
import pandas as pd
import re


def regionName(df):
    df["Region"] = df["Region"].replace({"Arica - Parinacota": "Arica y Parinacota",
                                         "Arica Parinacota": "Arica y Parinacota",
                                         "XV Región de Arica y Parinacota": "Arica y Parinacota",
                                         "I Región de Tarapacá": "Tarapacá",
                                         "Tarapaca": "Tarapacá",
                                         "II Región de Antofagasta": "Antofagasta",
                                         "III Región de Atacama": "Atacama",
                                         "IV Región de Coquimbo": "Coquimbo",
                                         "V Región de Valparaíso": "Valparaíso",
                                         "Valparaiso": "Valparaíso",
                                         "Región Metropolitana de Santiago": "Metropolitana",
                                         "Metropolitana de Santiago": "Metropolitana",
                                         "Región Metropolitana de Santiago": "Metropolitana",
                                         "Del Libertador General Bernardo O’Higgins": "O’Higgins",
                                         "Libertador General Bernardo OHiggins": "O’Higgins",
                                         "Libertador General Bernardo O'Higgins": "O’Higgins",
                                         "Libertador Gral. B. O'Higgins": "O’Higgins",
                                         "VI Región del Libertador General Bernardo O'Higgins": "O’Higgins",
                                         "VII Región del Maule": "Maule",
                                         "Nuble": "Ñuble",
                                         "XVI Región de Ñuble": "Ñuble",
                                         "Biobio": "Biobío", "Concepción": "Biobío",
                                         "VIII Región del Biobío": "Biobío",
                                         "La Araucania": "Araucanía",
                                         "la Araucanía": "Araucanía",
                                         "La Araucanía": "Araucanía",
                                         "IX Región de la Araucanía": "Araucanía",
                                         "Los Rios": "Los Ríos", "de Los Ríos": "Los Ríos", "De los Rios": "Los Ríos",
                                         "XIV Región de los Ríos": "Los Ríos",
                                         "De los Lagos": "Los Lagos",
                                         "X Región de Los Lagos": "Los Lagos",
                                         "Aysen": "Aysén",
                                         "Aysén del General Carlos Ibañez del Campo": "Aysén",
                                         "Aysén del General Carlos Ibáñez del Campo": "Aysén",
                                         "XI Región de Aisén del General Carlos Ibáñez del Campo": "Aysén",
                                         "Magallanes y la Antartica": "Magallanes",
                                         "Magallanes y de la Antártica Chilena": "Magallanes",
                                         "XII Región de Magallanes y de la Antártica Chilena": "Magallanes"
                                         })


def regionNameRegex(df):
    df['Region'] = df['Region'].replace(regex=True, to_replace=r'.*Región de ', value=r'')
    df['Region'] = df['Region'].replace(regex=True, to_replace=r'.*Región del ', value=r'')


def normalizaNombreCodigoRegionYComuna(df):
    # standards:
    if 'comuna' in df.columns:
        df.rename(columns={'comuna': 'Comuna'}, inplace=True)

    df["Comuna"] = df["Comuna"].replace({"Coyhaique": "coihaique",
                                         "Paihuano": "paiguano",
                                         "La Calera": "Calera",
                                         "Llay-Llay": "Llaillay"
                                         })

    # Lee IDs de comunas desde página web oficial de SUBDERE
    df_dim_comunas = pd.read_excel("http://www.subdere.gov.cl/sites/default/files/documentos/CUT_2018_v04.xls",
                                   encoding="utf-8")

    ##AYSEN issue

    df_dim_comunas['Nombre Comuna'] = df_dim_comunas['Nombre Comuna'].replace({"Aisén": "Aysen"})
    df['Comuna'] = df['Comuna'].replace({"Aisén": "Aysen"})
    # print(df_dim_comunas.to_string())
    print("change comuna Aisen to Aysen from subdere")

    # Crea columna sin tildes, para hacer merge con datos publicados
    # df_dim_comunas["Comuna"] = df_dim_comunas["Nombre Comuna"].str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8")
    df_dim_comunas["Comuna"] = df_dim_comunas["Nombre Comuna"].str.normalize("NFKD") \
        .str.encode("ascii", errors="ignore").str.decode("utf-8").str.lower().str.replace(' ', '')

    df["Comuna"] = df["Comuna"].str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8") \
        .str.lower().str.replace(' ', '')

    # print(df.to_string())

    # df = df.merge(df_dim_comunas, on="Comuna", how="outer")
    df = df.merge(df_dim_comunas, on="Comuna", how="inner")

    df['Comuna'] = df['Nombre Comuna']
    df['Codigo comuna'] = df['Código Comuna 2018']
    df['Region'] = df['Nombre Región']
    df['Codigo region'] = df['Código Región']

    df.drop(columns={'Código Región', 'Nombre Región',
                     'Código Comuna 2018', 'Nombre Comuna',
                     'Código Provincia', 'Nombre Provincia',
                     'Abreviatura Región'
                     }, inplace=True)

    # Sort Columns
    columnsAddedHere = ['Region', 'Codigo region', 'Comuna', 'Codigo comuna']
    originalColumns = [x for x in list(df) if x not in columnsAddedHere]
    sortedColumns = columnsAddedHere + originalColumns

    # # report on missing
    # df1 = df[df.isnull().any(axis=1)]
    # if df1.size > 0:
    #     print('These are missing')
    #     print(df1.to_string())

    df = df[sortedColumns]
    df['Codigo region'] = df['Codigo region'].astype(str)
    return df


####
def normalizaNombreCodigoRegionYCodigoComuna(df):
    # standards:
    if 'comuna' in df.columns:
        df.rename(columns={'comuna': 'Comuna'}, inplace=True)

    # df["Comuna"] = df["Comuna"].replace({"Coyhaique": "coihaique",
    #                                      "Paihuano": "paiguano",
    #                                      "La Calera": "Calera",
    #                                      "Llay-Llay": "Llaillay"
    #                                      })

    # Lee IDs de comunas desde página web oficial de SUBDERE
    df_dim_comunas = pd.read_excel("http://www.subdere.gov.cl/sites/default/files/documentos/CUT_2018_v04.xls",
                                   encoding="utf-8")

    ##AYSEN issue

    df_dim_comunas['Nombre Comuna'] = df_dim_comunas['Nombre Comuna'].replace({"Aisén": "Aysen"})
    # print(df_dim_comunas.to_string())
    df_dim_comunas.rename(columns={'Código Comuna 2018': 'Codigo comuna'}, inplace=True)

    # df = df.merge(df_dim_comunas, on="Comuna", how="outer")
    df = df.merge(df_dim_comunas, on="Codigo comuna", how="inner")

    df['Comuna'] = df['Nombre Comuna']
    df['Region'] = df['Nombre Región']
    df['Codigo region'] = df['Código Región']

    df.drop(columns={'Código Región', 'Nombre Región',
                     'Nombre Comuna',
                     'Código Provincia', 'Nombre Provincia',
                     'Abreviatura Región'
                     }, inplace=True)

    # Sort Columns
    columnsAddedHere = ['Region', 'Codigo region', 'Comuna', 'Codigo comuna']
    originalColumns = [x for x in list(df) if x not in columnsAddedHere]
    sortedColumns = columnsAddedHere + originalColumns

    # # report on missing
    # df1 = df[df.isnull().any(axis=1)]
    # if df1.size > 0:
    #     print('These are missing')
    #     print(df1.to_string())

    df = df[sortedColumns]
    df['Codigo region'] = df['Codigo region'].astype(str)
    return df


########
def normalizaNombreCodigoRegionYProvincia(df):
    # Lee IDs de provincias desde página web oficial de SUBDERE
    df_dim_provincias = pd.read_excel("http://www.subdere.gov.cl/sites/default/files/documentos/CUT_2018_v04.xls",
                                      encoding="utf-8")

    df_dim_provincias.drop(columns=['Código Comuna 2018',
                                    'Nombre Comuna',
                                    'Abreviatura Región']
                           , inplace=True)
    df_dim_provincias.drop_duplicates(inplace=True)

    df = pd.merge(df, df_dim_provincias, left_on="provincia", right_on="Código Provincia", how="left")

    df['Provincia'] = df['Nombre Provincia']
    df['Codigo provincia'] = df['Código Provincia']
    df['Region'] = df['Nombre Región']
    df['Codigo region'] = df['Código Región']

    df.drop(columns={'Código Región', 'Nombre Región',
                     'Código Provincia', 'Nombre Provincia'
                     }, inplace=True)

    # Sort Columns
    columnsAddedHere = ['Region', 'Codigo region', 'Provincia', 'Codigo provincia']
    originalColumns = [x for x in list(df) if x not in columnsAddedHere]
    sortedColumns = columnsAddedHere + originalColumns

    df = df[sortedColumns]
    df['Codigo region'] = df['Codigo region'].astype(str)
    return df


def normalizaNombreCodigoRegion(df):
    # Lee IDs de provincias desde página web oficial de SUBDERE
    df_dim_regiones = pd.read_excel("http://www.subdere.gov.cl/sites/default/files/documentos/CUT_2018_v04.xls",
                                    encoding="utf-8")

    df_dim_regiones.drop(columns=['Código Comuna 2018',
                                  'Nombre Comuna',
                                  'Abreviatura Región',
                                  'Código Provincia',
                                  'Nombre Provincia']
                         , inplace=True)
    df_dim_regiones.drop_duplicates(inplace=True)

    # print(df)
    df = pd.merge(df, df_dim_regiones, left_on="region", right_on="Código Región", how="left")
    # print(df)

    df['Region'] = df['Nombre Región']
    df['Codigo region'] = df['Código Región']

    df.drop(columns={'Código Región', 'Nombre Región'
                     }, inplace=True)

    # Sort Columns
    columnsAddedHere = ['Region', 'Codigo region']
    originalColumns = [x for x in list(df) if x not in columnsAddedHere]
    sortedColumns = columnsAddedHere + originalColumns

    # report on missing
    # df1 = df[df.isnull().any(axis=1)]
    # if df1.size > 0:
    #     print('These are missing')
    #     print(df1.to_string())

    df = df[sortedColumns]
    df['Codigo region'] = df['Codigo region'].astype(str)
    return df


#######

def FechaAlFinal(df):
    if 'Fecha' in df.columns:
        columns = [x for x in list(df) if x != 'Fecha']
        columns.append('Fecha')
        df = df[columns]
        return df
    else:
        print('No hay una columna Fecha en tu dataframe')


def transpone_csv(csvfile):
    df = pd.read_csv(csvfile)
    return (df.T)


def std_getSuperficieComunasOfficial(input):
    '''
    Bienes nacionales noticed we got superficies from wikipedia, so they contributed with a proper source
    ['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Superficie_km2']
    '''
    df = pd.read_excel(input)
    df.drop(columns={'CUT_PROV', 'PROVINCIA'}, inplace=True)

    df.rename(columns={
        'CUT_REG': 'Codigo region',
        'CUT_COM': 'Codigo comuna',
        'REGION': 'Region',
        'COMUNA': 'Comuna',
        'SUPERFICIE': 'Superficie_km2'
    }, inplace=True)

    # missing antartica comuna 12202
    # df["Comuna"] = df["Comuna"].replace({"La Calera": "Calera", "Llay-Llay": "Llaillay"})
    print("change comuna Aisen to Aysen from bienes")
    df['Comuna'] = df['Comuna'].replace({"Aisén": "Aysen"})
    df = normalizaNombreCodigoRegionYComuna(df)
    # print(df.to_string())
    # print(df['Comuna'].to_string())

    return df


def std_getPoblacion(fte, std_df):
    '''
    Agregamos poblacion a input/Otros/InformacionComunas.csv
    '''
    df = pd.read_csv(fte)
    # standards:
    df["Comuna"] = df["Comuna"].replace({"OHiggins": "O'Higgins"})
    df = normalizaNombreCodigoRegionYComuna(df)

    columnsToKeep = ['Codigo comuna', 'Poblacion']
    df = df[columnsToKeep]
    print('Keeping ' + str(df.columns))
    # if there is a poblacion columns, drop it
    print('std_df.columns = ' + str(std_df.columns))
    if 'Poblacion' in std_df:
        std_df = std_df.drop(columns=['Poblacion'])

    columnsToKeep = list(std_df)
    columnsToKeep.append('Poblacion')
    std_df = std_df.merge(df, on="Codigo comuna", how="outer")
    print('Poblacion total es ' + str(std_df['Poblacion'].sum()))
    return std_df


def writeStandardsToFile(prod):
    '''
    Actualizamos y/o generamos el archivo con entradas mas estables para las comunas:
    Region,Codigo region,Comuna,Codigo comuna,Superficie_km2,Poblacion
    '''
    out = std_getSuperficieComunasOfficial('../input/Otros/2020.xlsx')
    out = std_getPoblacion('../output/producto1/Covid-19.csv', out)
    out.to_csv(prod, index=False)


def insertSuperficiePoblacion(df):
    df_std = pd.read_csv('../input/Otros/InformacionComunas.csv')
    df_sup = df_std[['Codigo comuna', 'Superficie_km2', 'Poblacion']]
    df = df.merge(df_sup, on="Codigo comuna", how="outer")

    # Sort Columns
    columnsAddedHere = ['Superficie_km2', 'Poblacion']
    originalColumns = [x for x in list(df) if x not in columnsAddedHere]
    sortedColumns = columnsAddedHere + originalColumns

    df = df[sortedColumns]

    return df


def desconocidoName(df):
    df["Comuna"] = df["Comuna"].replace(
        {"Desconocido Del Libertador General Bernardo O’Higgins": "Desconocido O’Higgins",
         "Desconocido La Araucania": "Desconocido Araucania",
         "Desconocido Magallanes y la Antartica": "Desconocido Magallanes"
         })


def comunaName(df):
    df["comuna_residencia"] = df["comuna_residencia"].replace(
        {"Camiña": "Camina", "Ollagüe": "Ollague", "María Elena": "Maria Elena",
         "Copiapó": "Copiapo", "Chañaral": "Chanaral", "Vicuña": "Vicuna",
         "Combarbalá": "Combarbala", "Río Hurtado": "Rio Hurtado",
         "Valparaíso": "Valparaiso", "Con con": "Concon", "Con cón": "Concon", "Concón": "Concon",
         "Con Con": "Concon", "Con Cón": "Concon",
         "Juan Fernández": "Juan Fernandez", "Puchuncaví": "Puchuncavi",
         "Viña del Mar": "Vina del Mar", "Santa María": "Santa Maria",
         "Quilpué": "Quilpue", "Olmué": "Olmue", "Doñihue": "Donihue",
         "Machalí": "Machali", "Requínoa": "Requinoa", "Chépica": "Chepica",
         "Constitución": "Constitucion", "Río Claro": "Rio Claro", "Curicó": "Curico",
         "Hualañé": "Hualane", "Licantén": "Licanten", "Vichuquén": "Vichuquen",
         "Colbún": "Colbun", "Longaví": "Longavi", "Concepción": "Concepcion",
         "Tomé": "Tome", "Cañete": "Canete", "Tirúa": "Tirua", "Mulchén": "Mulchen",
         "Santa Bárbara": "Santa Barbara", "Alto Biobío": "Alto Biobio",
         "Pitrufquén": "Pitrufquen", "Pucón": "Pucon", "Toltén": "Tolten",
         "Vilcún": "Vilcun", "Curacautín": "Curacautin", "Purén": "Puren",
         "Traiguén": "Traiguen", "Cochamó": "Cochamo", "Maullín": "Maullin",
         "Curaco de Vélez": "Curaco de Velez", "Puqueldón": "Puqueldon",
         "Queilén": "Queilen", "Quellón": "Quellon", "Río Negro": "Rio Negro",
         "Chaitén": "Chaiten", "Futaleufú": "Futaleufu", "Hualaihué": "Hualaihue",
         "Aisén": "Aysen", "Aysén": "Aysen", "O'Higgins": "OHiggins",
         "Río Ibáñez": "Rio Ibanez", "Río Verde": "Rio Verde", "Antártica": "Antartica",
         "Conchalí": "Conchali", "Estación Central": "Estacion Central",
         "Maipú": "Maipu", "Ñuñoa": "Nunoa", "Peñalolén": "Penalolen",
         "San Joaquín": "San Joaquin", "San Ramón": "San Ramon",
         "San José de Maipo": "San Jose de Maipo", "Alhué": "Alhue",
         "Curacaví": "Curacavi", "María Pinto": "Maria Pinto", "Peñaflor": "Penaflor",
         "Máfil": "Mafil", "La Unión": "La Union", "Río Bueno": "Rio Bueno",
         "Chillán": "Chillan", "Chillán Viejo": "Chillan Viejo", "Quillón": "Quillon",
         "Ñiquén": "Niquen", "San Fabián": "San Fabian", "San Nicolás": "San Nicolas",
         "Los Álamos": "Los Alamos", "Los Ángeles": "Los Angeles", "Hualpén": "Hualpen",
         "Ránquil": "Ranquil"
         })


def regionDEISName(df):
    df["region_residencia"] = df["region_residencia"].replace({
        "Metropolitana de Santiago": "Metropolitana",
        "De Antofagasta": "Antofagasta",
        "De Arica y Parinacota": "Arica y Parinacota",
        "De Atacama": "Atacama",
        "De Aisén del General Carlos Ibáñez del Campo": "Aysén",
        "De Coquimbo": "Coquimbo",
        "De Los Lagos": "Los Lagos",
        "De Los Ríos": "Los Ríos",
        "De Magallanes y la Antártica Chilena": "Magallanes",
        "De Tarapacá": "Tarapacá",
        "De Valparaíso": "Valparaíso",
        "De La Araucanía": "Araucanía",
        "Del Biobío": "Biobío",
        "Del Libertador General Bernardo OHiggins": "O’Higgins",
        "Del Maule": "Maule",
        "De Ñuble": "Ñuble"
    })


if __name__ == '__main__':
    writeStandardsToFile('../input/Otros/InformacionComunas.csv')
