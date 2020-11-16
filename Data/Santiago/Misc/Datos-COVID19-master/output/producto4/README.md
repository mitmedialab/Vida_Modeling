# DP4 - Casos totales por región: Descripción
Serie de archivos que dan cuenta del número de casos nuevos, del total de casos confirmados, recuperados (antes del 21 de marzo) % de casos totales y casos fallecidos en cada una de las regiones de Chile, según residencia. Cada uno de los archivos corresponde a la información diaria que reporta el Ministerio de Salud del país. Existe variabilidad en los campos según la fecha (ver sección Columnas y valores).

Se entiende por caso confirmado la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2.

Se entiende en este reporte los casos recuperados como las personas que tras ser confirmadas de COVID-19, han estado en cuarentena pasando 14 días sin síntomas. Para calcular recuperados de otra manera, se puede utilizar el [producto 15: Casos nuevos por fecha de inicio de sintomas](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto15). 

Se entiende por región de residencia la región que la persona declara como su vivienda habitual. 

Se entiende por porcentaje de casos totales el porcentaje del número total de casos registrados en el país. 

# Columnas y valores
Los archivos correspondientes a fechas anteriores al 21-03-2020 (inclusive), contienen las columnas ‘Región’, ‘Casos nuevos’, ‘Casos totales’ y ‘Casos recuperados’. 

Los archivos correspondientes a fechas desde el 22-03-2020 al 25-03-2020 (inclusive), contienen las columnas 'Región', ‘Casos nuevos’, ‘Casos totales’ y ‘Fallecidos’. 

Los archivos correspondientes a fechas desde el 26-03-2020 al 04-04-2020 (inclusive), contienen las columnas 'Región', ‘Casos nuevos’, ‘Casos totales’, ‘Casos recuperados’ y ‘Fallecidos’.

Los archivos correspondientes a fechas desde el 05-04-2020 en adelante, contienen las columnas 'Región', ‘Casos nuevos’, ‘Casos totales’, ‘% de casos totales’ y ‘Fallecidos’.

La última fila contiene Totales. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Ministerio de Salud. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/

# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero. 

**Nota aclaratoria 2:**  Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 3:** Previo al 15 de abril de 2020 los reportes del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas. 

