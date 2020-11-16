# DP13 - Casos nuevos totales por región incremental: Descripción
Set de 2 archivos que dan cuenta del número de casos nuevos por día según resultado del diagnóstico, por región de residencia, reportados por el Ministerio de Salud desde el 03-03-2020. 

A partir del 29 de abril esta serie de tiempo incluye los casos nuevos sin síntomas, es decir es el total de casos nuevos (sin síntomas + con síntomas)

También existe el [producto 15: Casos nuevos por fecha de inicio de sintomas](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto15) que reporta casos nuevos por fecha de inicio de síntomas, resultado de la vigilancia e investigación epidemiológica del Ministerio de Salud de Chile.

# Columnas y valores
El archivo CasosNuevosCumulativo.csv contiene la columna ‘Región’, seguida por columnas correspondientes a ‘[Fecha]’. Estas últimas columnas, ‘[Fecha]’, indican el número de casos nuevos acumulativos, por región, desde el 03-03-2020 hasta la fecha. El archivo CasosNuevosCumulativo_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Reporte diario del Ministerio de Salud. Ver en:
https://www.gob.cl/coronavirus/cifrasoficiales/#reportes

# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs.
