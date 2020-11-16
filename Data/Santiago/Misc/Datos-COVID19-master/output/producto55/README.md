# DP - Positividad de examenes PCR según fecha del examen, provistos por ICOVID Chile. 

Este producto surge del trabajo colaborativo entre el Ministerio de Salud, el Ministerio de Ciencias, e investigadores del grupo ICOVID Chile (https://www.icovidchile.cl). El producto contiene información sobre la media movil de los último 7 días de la positividad de los examenes de PCR a SARS-CoV-2, definida como la proporción de los test que resultan positivos, sobre el total de test efectuados ese día (test positivos / test totales).  

# Columnas y valores
El archivo 'Positividad nacional.csv' contiene la columna 'fecha' que corresponde a la fecha de toma del examen y la columna 'positividad' que indica la media movil de los último 7 días de la proporción de examenes positivos. Todos estos valores están separados entre sí por comas (csv).

El archivo 'Positividad por región.csv' contiene la columna 'codigo_region' indicando el código de la región de residencia, 'region_residencia' indicando el nombre de la región de residencia, 'fecha' indicando la fecha de toma del examen, y 'positividad'  que indica la media movil de los último 7 días de la proporción de examenes positivos. Todos estos valores están separados entre sí por comas (csv).

El archivo 'Positividad por provincia.csv' contiene la columna 'codigo_provincia' indicando el código de la provincia de residencia, 'provincia_residencia' indicando el nombre de la provincia de residencia, 'fecha' indicando la fecha de toma del examen, y 'positividad' que indica la media movil de los último 7 días de la proporción de examenes positivos. Todos estos valores están separados entre sí por comas (csv).

El archivo 'Positividad por comuna.csv' contiene la columna 'codigo_comuna' indicando el código de la comuna de residencia, 'comuna_residencia' indicando el nombre de la comuna de residencia, 'fecha' indicando la fecha de toma del examen, y 'positividad' que indica la media movil de los último 7 días de la proporción de examenes positivos. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Datos publicados periódicamente por el grupo ICOVID Chile (https://www.icovidchile.cl). 

# Frecuencia de actualización
Asociado a los informes epidemiológicos publicados por el Ministerio de Salud de Chile.

# Notas aclaratorias
(1) La informacion sobre la comuna de residencia tiene una mayor frecuencia de datos faltantes. Por esta razón, 
las series de datos de mayor nivel de agregacion no necesariamente pueden obtenerse de la simple agregación de áreas geográficas menores. Para aquellas personas sin informacion de residencia, pero para quienes existía informacion sobre el lugar de toma de muestra, este último fue utilizado para asignar el test a una determinada área geográfica

(2) ICOVID Chiles es grupo interdisciplinario convocado inicialmente por los Prorrectores de la Pontificia Universidad Católica de Chile, la Universidad de Chile, y a que se suma posteriormente la Universidad de Concepción. El cálculo de estas series corregidas se enmarcan en un proyecto de colaboración entre el Ministerio de Salud de Chile, el Ministerio de Ciencia, Tecnología, Conocimiento e Innovación de Chile, la Pontificia Universidad Católica de Chile y la Universidad de Chile.
