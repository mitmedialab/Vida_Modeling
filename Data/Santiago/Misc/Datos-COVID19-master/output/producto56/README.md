# DP - Proporción de casos confirmados tempranos, provistos por ICOVID Chile. 

Este producto surge del trabajo colaborativo entre el Ministerio de Salud, el Ministerio de Ciencias, e investigadores del grupo ICOVID Chile (https://www.icovidchile.cl). El producto contiene información sobre la proporción de casos confirmados para los cuales el tiempo transcurrido entre la fecha de inicio de los síntomas y la fecha en que el resultado del test de PCR a SARS-CoV-2 es recibido por la autoridad sanitaria es menor o igual a 48 horas (casos confirmados tempranos).  

# Columnas y valores
El archivo 'prob48.nacional.csv' contiene la columna 'fecha' que corresponde a la fecha del último día de la semana, la columna 'prob48.estimado' que contiene la estimación de la proporción de casos confirmados tempranos a nivel nacional la semana correspondiente, y las columnas 'prob48.linf' y 'prob48.lsup' que contienen los límites del intervalo de 95% de credibilidad para la proporción de casos confirmados tempranos a nivel nacional para la semana correspondiente. Todos estos valores están separados entre sí por comas (csv).

El archivo 'prob48.regional.csv' contiene la columna 'fecha' que corresponde a la fecha del último día de la semana, 'region' indicando el código de la región, la columna 'prob48.estimado' que contiene la estimación de la  proporción de casos confirmados tempranos en cada región la semana correspondiente, y las columnas 'prob48.linf' y 'prob48.lsup' que contienen los límites del intervalo de 95% de credibilidad para la proporción de casos confirmados tempranos en cada región para la semana correspondiente. Todos estos valores están separados entre sí por comas (csv).

El archivo 'prob48.provincial.csv' contiene la columna 'fecha' que corresponde a la fecha del último día de la semana, 'region' indicando el código de la región,
'provincia' indicando el código de la provincia, la columna 'prob48.estimado' que contiene la estimación de la proporción de casos confirmados tempranos en cada provincia la semana correspondient, y las columnas 'prob48.linf' y 'prob48.lsup' que contienen los límites del intervalo de 95% de credibilidad para la proporción de casos confirmados tempranos en cada provincia para la semana correspondiente. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Datos publicados periódicamente por el grupo ICOVID Chile (https://www.icovidchile.cl). 

# Frecuencia de actualización
Asociado a los informes epidemiológicos publicados por el Ministerio de Salud de Chile.

# Notas aclaratorias
(1) Estos resultados son estimados como parte de un modelo de estimación de casos presentes, cuyos resultados están disponibles en el Data Product 53, y corresponden a una característica de la distribución del rezago para cada semana epidemiológica.

(2) ICOVID Chiles es un grupo interdisciplinario convocado inicialmente por los Prorrectores de la Pontificia Universidad Católica de Chile, la Universidad de Chile, y al que se suma posteriormente la Universidad de Concepción. El cálculo de estas series corregidas se enmarcan en un proyecto de colaboración entre el Ministerio de Salud de Chile, el Ministerio de Ciencia, Tecnología, Conocimiento e Innovación de Chile, la Pontificia Universidad Católica de Chile y la Universidad de Chile.
