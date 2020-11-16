# DP53 - Series corregidas sobre el número de casos confirmados, provistos por el grupo ICOVID Chile. 
Este producto surge del trabajo colaborativo entre el Ministerio de Salud, el Ministerio de Ciencias, e investigadores del grupo ICOVID Chile (https://www.icovidchile.cl).

Durante una epidemia, contar con información oportuna sobre el número de casos nuevos es crucial. Sin embargo, la toma de conocimiento de su existencia por parte de la autoridad sanitaria generalmente está sujeta a demoras o rezagos debido al periodo de incubación de la enfermedad, el tiempo de consulta a un especialista, el tiempo al diagnóstico y el tiempo al reporte del diagnóstico, entre otros. Esto implica que el número de casos nuevos recientemente observados, corresponde a una fracción de los casos que han iniciado la infección, lo que resulta en una subestimación de la cantidad de casos activos y en sesgos importantes en la estimación de indicadores de interés, tales como el número de reproducción efectivo, basados en los datos disponibles.

El presente producto contiene información sobre el número de casos confirmados, según fecha de inicio de los síntomas (utilizado como un proxy de la fecha de infección), corregidos por la presencia de datos faltantes respecto de la fecha de inicio de los síntomas y por los tiempos de rezago de la información. En lugar de reportar la estimación sobre el número de casos ocurridos y de una medida de su incertidumbre, se entregan 200 series generadas a través de la técnica de imputación múltiple, en base a modelos estadísticos desarrollados por el grupo ICOVID Chile y aplicados a diferentes unidades territoriales, a partir de los datos del Ministerio de Salud de Chile. Los detalles técnicos sobre los modelos de corrección de datos y el proceso de imputación se pueden encontrar en sitio web de grupo ICOVID Chile (https://www.icovidchile.cl). 

# Columnas y valores
El archivo 'confirmados_nacionales.csv' contiene la columna 'fecha' que corresponde a la fecha de inicio de los síntomas, y una serie de columnas  'confirmados.1' , ... , 'conformados.200', que corresponden a las diferente series generadas a través de imputación múltiple conteniendo el número de casos confirmados en cada día a nivel nacional. Todos estos valores están separados entre sí por comas (csv).

El archivo 'confirmados_regionales.csv' contiene la columna 'Region', 'Codigo region' y 'fecha' que corresponden al nombre de la región, el número de la región y la fecha de inicio de los síntomas, respectivamente, y una serie de columnas  'confirmados.1' , ... , 'conformados.200', que corresponden a las diferente series generadas a través de imputación múltiple conteniendo el número de casos confirmados en cada día a nivel nacional. Todos estos valores están separados entre sí por comas (csv).

El archivo 'confirmados_provinciales.csv' contiene la columna 'Region', 'Codigo region', 'Provincia', 'Codigo provincia' y 'fecha' que corresponden al nombre de la región, el número de la región, el nombre de la provincia, el número de la provincia y la fecha de inicio de los síntomas, respectivamente, y una serie de columnas  'confirmados.1' , ... , 'conformados.200', que corresponden a las diferente series generadas a través de imputación múltiple conteniendo el número de casos confirmados en cada día a nivel nacional. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Datos publicados periódicamente por el grupo ICOVID Chile (https://www.icovidchile.cl). 

# Frecuencia de actualización
Asociado a los informes epidemiológicos publicados por el Ministerio de Salud de Chile.

# Notas aclaratorias
ICOVID Chiles es grupo interdisciplinario convocado inicialmente por los Prorrectores de la Pontificia Universidad Católica de Chile, la Universidad de Chile, y a que se suma posteriormente la Universidad de Concepción. El cálculo de estas series corregidas se enmarcan en un proyecto de colaboración entre el Ministerio de Salud de Chile, el Ministerio de Ciencia, Tecnología, Conocimiento e Innovación de Chile, la Pontificia Universidad Católica de Chile y la Universidad de Chile.