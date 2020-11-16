import pandas as pd
import glob
import re

regions_id = {"Arica y Parinacota": 15, "Tarapacá": 1, "Antofagasta": 2, "Atacama": 3,
              "Coquimbo": 4, "Valparaíso": 5, "Metropolitana": 13, "O’Higgins": 6,
              "Maule": 7, "Ñuble": 16, "Biobío": 8, "Araucanía": 9, "Los Ríos": 14,
              "Los Lagos": 10, "Aysén": 11, "Magallanes": 12
              }

regions_pob = {"Arica y Parinacota": 252110, "Tarapacá": 382773, "Antofagasta": 691854, "Atacama": 314709,
               "Coquimbo": 836096, "Valparaíso": 1960170, "Metropolitana": 8125072, "O’Higgins": 991063,
               "Maule": 1131939, "Ñuble": 511551, "Biobío": 1663696, "Araucanía": 1014343, "Los Ríos": 405835,
               "Los Lagos": 891440, "Aysén": 107297, "Magallanes": 178362
               }

data = []
for file in glob.glob("../output/producto4/*.csv"):
    date = re.search("\d{4}-\d{2}-\d{2}", file).group(0).replace("-", "/")
    df = pd.read_csv(file, sep=",", encoding="utf-8")
    df.columns = df.columns.str.replace(" ", "")

    # Estandarización de nombres de columnas
    if "Casosfallecidos" in list(df):
        df = df.rename(columns={"Casosfallecidos": "Fallecidos"})

    if "Fallecidos" not in list(df):
        df["Fallecidos"] = 0

    if "Región" in list(df):
        df = df.rename(columns={"Región": "Region"})

    df["Fecha"] = date

    df = df.rename(columns={"Casosnuevos": "Nuevos Casos",
                            "Casostotales": "Casos Confirmados"})

    # Elimina la filas "total"
    df = df[df["Region"] != "Total"]

    # Corrige un error de la data
    if date == "2020/03/03":
        df.loc[df["Region"] == "Maule", ["Nuevos Casos"]] = 1
    data.append(df)

data = pd.concat(data)

# Borra columnas innecesarias
data = data.drop(columns={"%Casostotales**", "Casosrecuperados"})

# Soluciona problemas con los nombres de regiones
data["Region"] = data.apply(lambda x: " ".join(x["Region"].split()), axis=1)
data["Region"] = data["Region"].replace({"Tarapaca": "Tarapacá", "Valparaiso": "Valparaíso", "Metropolita": "Metropolitana",
                                         "O'Higgins": "O’Higgins", "Nuble": "Ñuble", "Biobio": "Biobío", "Los Rios": "Los Ríos",
                                         "Araucania": "Araucanía", "Aysen": "Aysén", "Arica y Paricota": "Arica y Parinacota"
                                         })
# Crea el identificador regional
data["Region ID"] = data["Region"].replace(regions_id)

# Crea columna con la población regional
data["Poblacion"] = data["Region"].replace(regions_pob).astype(int)

# Obtiene la tasa de contagios cada 100 mil habitantes
data["Tasa"] = (data["Casos Confirmados"]/data["Poblacion"])*100000

# Crea output de datos en CSV / JSON
data.to_csv("../output/producto11/bulk/producto4.csv", index=False)
data.to_json("../output/producto11/bulk/producto4.json", orient="records")
