# DP54 - Número de reproducción efectivo, provisto por el grupo ICOVID Chile.

Este producto surge del trabajo colaborativo entre el Ministerio de Salud, el Ministerio de Ciencias, e investigadores del grupo ICOVID Chile (https://www.icovidchile.cl).

El presente producto contiene información sobre el número de reproducción efectivo, estimado en base a los casos confirmados según la fecha de inicio de los síntomas, utilizado como un proxy de la fecha de infección. El número de reproducción efectivo se estimó empleando el método propuesto por:

Cori, A., Ferguson, N.M., Fraser, C., Cauchemez, S. (2013). A new framework and software to estimate time-varying reproduction numbers during epidemics. American Journal of Epidemiology, 178: 1505 - 1512.

El método de Cori, así como los otros métodos de estimación del número de reproducción efectivo, asumen que la cantidad de casos que inician la infección son completamente observados. Sin embargo, la observación de casos nuevos generalmente está sujeta a demoras o rezagos debido al periodo de incubación de la enfermedad, el tiempo de consulta a un especialista, el tiempo al diagnóstico y el tiempo al reporte del diagnóstico, entre otros. En lugar de imputar la cantidad de casos esperada, lo que genera una sub-estimación de las incertidumbres de las estimaciones, se utilizó el método de imputación múltiple, en base a los datos descritos en el producto 53.  Los detalles técnicos sobre la implementación del método de estimación del número de reproducción efectivo se pueden encontrar en sitio web de grupo ICOVID Chile (https://www.icovidchile.cl).

# Columnas y valores
El archivo 'r.nacional.csv' contiene la columna 'fecha' , 'r.estimado', 'r.liminf' y 'r.lisup'  que corresponden a fecha, la estimación puntal del número de reproducción efectivo,
el límite inferior del intervalo de 95% de confianza y el límite superior del intervalo de 95% de confianza. Todos estos valores están separados entre sí por comas (csv).

El archivo 'r.regional.csv' contiene la columna  'Region', 'Codigo region', 'fecha' , 'r.estimado', 'r.liminf' y 'r.lisup'  que corresponden al nombre de la región, el código de la región, la fecha, la estimación puntal del número de reproducción efectivo,  el límite inferior del intervalo de 95% de confianza y el límite superior del intervalo de 95% de confianza. Todos estos valores están separados entre sí por comas (csv).

El archivo 'r.provincial.csv' contiene la columna   'Region', 'Codigo region', 'Provincia', 'Codigo provincia', 'fecha' , 'r.estimado', 'r.liminf' y 'r.lisup'  que corresponden al nombre de la región, el código de la región, el nombre de la provincia, el número de la provincia, la fecha, la estimación puntal del número de reproducción efectivo,  el límite inferior del intervalo de 95% de confianza y el límite superior del intervalo de 95% de confianza. Todos estos valores están separados entre sí por comas (csv).