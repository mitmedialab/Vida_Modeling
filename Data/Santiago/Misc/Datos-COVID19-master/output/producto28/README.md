# DP28 - Casos nuevos por fecha de inicio de síntomas por Región, informado por SEREMI regionales: Descripción
Set de 3 archivos que dan cuenta de los casos nuevos por fecha de inicio de síntomas notificados por SEREMI regionales. Se indexan según semana epidemiológica reportada en el último informe epidemiológico publicado por el Ministerio de Salud del país. Estos casos tienen residencia indeterminada al momento de notificación (turistas sin domicilio conocido, pasajeros de cruceros, tripulantes de barcos mercantes, entre otros). Estos reflejan la información del último informe epidemiológico publicado por el Ministerio de Salud. Se recomienda sumar estos casos confirmados e informados por SEREMI a la suma de casos confirmados por comuna (totales regionales) dados en el [Data Product 15 - Casos nuevos por fecha de inicio de síntomas por comuna](../producto15) y a otros productos que cuenten casos con fuente el Informe Epidemiológico.

Se entiende por fecha de inicio de síntomas el momento de la manifestación clínica de la enfermedad. Se entiende por comuna de residencia la comuna que la persona declara como su vivienda habitual. 

# Columnas y valores

El archivo FechaInicioSintomas_reportadosSEREMI.csv contiene las columnas 'SEREMI notificacion', 'Codigo Region' y una serie de columnas 'SE7', 'SE8', ..., que corresponden a las semanas epidemiológicas. Los valores por fila corresponden a tuplas de SEREMI regionales con sus respectivos metadatos y la cantidad de casos confirmados por semana epidemiológica en cada columna 'SE...'. El archivo FechaInicioSintomas_reportadosSEREMI_T.csv es la versión traspuesta del primer archivo. El archivo FechaInicioSintomas_reportadosSEREMI_std.csv contiene la misma data de FechaInicioSintomas_reportadosSEREMI.csv en formato estándar (unpivoted). El archivo ([SemanasEpidemiologicas.csv](../producto15)) es útil para la lectura de estos archivos, este contiene una columna de Fecha, y columnas 'SE...', con dos filas que indican la fecha de inicio de la semana epidemiológica, y la fecha de término de la misma. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS. 

# Frecuencia de actualización

Cada 2 a 3 días. 

# Notas aclaratorias

**Nota aclaratoria 1:** Los datos son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la vigilancia e investigación epidemiológica desarrollada por el Departamento de Epidemiología del Ministerio de Salud del país.

**Nota aclaratoria 2:** Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 3:** Acorde a lo informado por Epidemiología MINSAL, la fecha de inicio de síntomas corresponde al momento de la manifestación clínica de la enfermedad, y son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la investigación epidemiológica.
