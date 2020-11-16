import pandas as pd
import numpy

regions_id = {"Arica y Parinacota": 15, "Tarapacá": 1, "Antofagasta": 2, "Atacama": 3,
              "Coquimbo": 4, "Valparaíso": 5, "Metropolitana": 13, "O’Higgins": 6,
              "Maule": 7, "Ñuble": 16, "Biobío": 8, "Araucanía": 9, "Los Ríos": 14,
              "Los Lagos": 10, "Aysén": 11, "Magallanes": 12
              }

df = pd.read_csv("../output/producto7/PCR.csv", sep=",", encoding="utf-8")
df = df.drop('Codigo region', axis='columns')
df = pd.melt(df, id_vars=["Region", "Poblacion"],
             var_name="Fecha", value_name="PCR Realizados")

df["Region"] = df["Region"].replace({"Tarapaca": "Tarapacá", "Valparaiso": "Valparaíso",
                                     "Del Libertador General Bernardo O’Higgins": "O’Higgins", "Nuble": "Ñuble",
                                     "Biobio": "Biobío", "La Araucania": "Araucanía", "Los Rios": "Los Ríos",
                                     "Aysen": "Aysén", "Magallanes y la Antartica": "Magallanes"
                                     })

df["Region ID"] = df["Region"].replace(regions_id)

df["PCR Realizados"] = df["PCR Realizados"].fillna("-")



df["Fecha"] = df["Fecha"].str.replace("-", "/")

df["Tasa"] = df.apply(lambda x: (100000 * (int(x["PCR Realizados"]) /
                                           x["Poblacion"])) if x["PCR Realizados"] != "-" else "-", axis=1)

# Crea output de datos en CSV / JSON
df.to_csv("../output/producto12/bulk/producto7.csv", index=False)
df.to_json("../output/producto12/bulk/producto7.json", orient="records")
