# DP3 - Casos totales por región: Descripción
Este producto da cuenta de los casos totales diarios confirmados por laboratorio en cada una de las regiones de Chile, según residencia, y concatena la información reportada por el Ministerio de Salud del país. 

Los archivos TotalesPorRegion('.csv', '_T.csv' y '_std.csv') ensamblan las distribuciones regionales de: Casos acumulados, Casos nuevos totales, Casos nuevos con sintomas, Casos nuevos sin sintomas, Casos nuevos sin notificar y Fallecidos totales.

Se entiende por caso confirmado la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2.

Se entiende por región de residencia la región que la persona declara como su vivienda habitual. Se entiende por porcentaje de casos totales el porcentaje del número total de casos registrados en el país. 

# Columnas y valores
El archivo TotalesPorRegion.csv contiene una columna 'Region' seguida por 'Categoria', seguida por columnas correspondientes a ['fecha']. 
Estas últimas columnas contienen los casos por 'Categoria' ordenados de la siguiente manera:

filas, Distribución:<br/>
2-17 Distribución de los Casos acumulados, fila 18: total de esta distribución<br/>
19-34 Distribución de los Casos nuevos totales, fila 35: total de esta distribución<br/>
36-51 Distribución de los Casos nuevos con sintomas, fila 52: total de esta distribución<br/>
53-68 Distribución de los Casos nuevos sin sintomas, fila 69: total de esta distribución<br/>
70-85 Distribución de los Casos nuevos sin notificar, fila 86: total de esta distribución<br/>
87-102 Distribución de los Fallecidos totales, fila 103 total de esta distribución<br/>
104-119 Distribución de los Casos confirmados recuperados, fila 120 total de esta distribución<br/>
121-136 Distribución de los Casos activos confirmados, fila 137 total de esta distribución<br/>
138-153 Distribución de los Casos activos probables, fila 154 total de esta distribución<br/>
155-170 Distribución de los Casos probables acumulados, fila 171 total de esta distribución<br/>

Cada una de las Categorías son reportadas por el Ministerio de Salud de Chile.

El archivo CasosTotalesCumulativo.csv contiene una columna 'Región', seguida por columnas correspondientes a '[fecha]'. Estas últimas columnas, ‘[fecha]’, contienen los 'Casos acumulados' reportados por el Ministerio de Salud de Chile en cada una de las fechas que se indican en las respectivas columnas. El archivo CasosTotalesCumulativo_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Ministerio de Salud. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/

# Frecuencia de actualización
Actualización diaria. 

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero.

**Nota aclaratoria 2:**  Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 3:** Previo al 15 de abril de 2020 los reportes del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas. 

**Nota aclaratoria 4:** Dado que los archivos TotalesPorRegion('.csv', '_T.csv' y '_std.csv') contienen los datos reportados en CasosTotalesCumulativo, este último se deprecará en dos semanas.

