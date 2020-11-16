# DP26 - Casos nuevos con síntomas por región: Descripción
Set de 3 archivos que dan cuenta del número de casos confirmados nuevos por día según resultado del diagnóstico y que han presentado síntomas, por región de residencia, reportados por el Ministerio de Salud.

Esta serie de tiempo incluye los casos nuevos denominados "con síntomas" por la autoridad sanitaria.

También existe el [producto 15: Casos nuevos por fecha de inicio de sintomas](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto15) que reporta casos nuevos por fecha de inicio de síntomas, resultado de la vigilancia e investigación epidemiológica del Ministerio de Salud de Chile.

# Columnas y valores
El archivo CasosNuevosConSintomas.csv contiene la columna ‘Región’, seguida por columnas correspondientes a ‘[Fecha]’. Estas últimas columnas, ‘[Fecha]’, indican el número de casos nuevos con síntomas por día hasta la fecha. El archivo CasosNuevosConSintomas_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. El archivo CasosNuevosConSintomas_std.csv contiene la misma data de CasosNuevosConSintomas.csv en formato estándar (unpivoted). Todos estos valores están separados entre sí por comas (csv).

# Fuente
Reporte diario del Ministerio de Salud. Ver en:
https://www.gob.cl/coronavirus/cifrasoficiales/#reportes

# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs.
