# DP15 - Casos nuevos por fecha de inicio de síntomas por comuna: Descripción
Set de 4 archivos que dan cuenta de los casos nuevos por fecha de inicio de sus síntomas en cada una de las comunas 
de Chile, según residencia. Refleja la información del último informe epidemiológico publicado por el Ministerio de 
Salud del país. Se indexan estos casos según semana epidemiológica reportada en el informe, con fechas incluidas en los archivos.

Se entiende por fecha de inicio de síntomas el momento de la manifestación clínica de la enfermedad. Se entiende por 
comuna de residencia la comuna que la persona declara como su vivienda habitual. 

# Columnas y valores
El archivo FechaInicioSintomas.csv contiene las columnas 'Region', 'Código región', 'Comuna', 'Código comuna', 'Población' 
y una serie de columnas 'SE7', 'SE8', ..., que corresponden a semanas epidemiológicas. Los valores por fila corresponden 
a tuplas de comunas con sus respectivos metadatos, y la cantidad de casos confirmados por semana epidemiológica en cada 
columna 'SE...'. El archivo FechaInicioSintomas_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. 
Se incluye el archivo FechaInicioSintomas_std.csv que contiene la misma data de FechaInicioSintomas.csv en formato 
estándar (unpivoted). El tercer archivo (SemanasEpidemiologicas.csv) contiene una columna de Fecha, y columnas 
'SE...', con dos filas que indican la fecha de inicio de la semana epidemiológica, y la fecha de término de la misma. 
Todos estos valores están separados entre sí por comas (csv).

El archivo FechaInicioSintomas_std.csv contiene la misma data de FechaInicioSintomas.csv en formato estándar (unpivoted)

El archivo FechaInicioSintomasHistorico_std.csv contiene el registro de los reportes, dado que su naturaleza es dinámica,
ofreciendo una manera rápida para comparar los datos entregados en distintos períodos para las mismas semanas epidemiológicas.

# Fuente
Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS. 

# Frecuencia de actualización

Cada 2 a 3 días. 

# Notas aclaratorias

**Nota aclaratoria 1:** Los datos son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la vigilancia e investigación epidemiológica desarrollada por el Departamento de Epidemiología del Ministerio de Salud del país.

**Nota aclaratoria 2:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero. 

**Nota aclaratoria 3:** Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 4:** Previo al 15 de abril de 2020 los informes epidemiológicos del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas. 

**Nota aclaratoria 5:** Acorde a lo informado por Epidemiología MINSAL, la fecha de inicio de síntomas corresponde al momento de la manifestación clínica de la enfermedad, y son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la investigación epidemiológica.

**Nota aclaratoria 6:** Los datos de población provienen de las proyecciones estadísticas del INE, con base en el CENSO 2017 (para más detalles revisar https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion).
