# DP35 - Comorbilidad por Casos Confirmados: Descripción
Este producto da cuenta de la distribución de las enfermedades crónicas más frecuentes en los casos confirmados no hospitalizados, también da cuenta de la distribución para los casos que han requerido hospitalización. Se concatena la historia de los informes de Situación Epidemiológica publicados por el Ministerio de Salud del país.

Se entiende por caso confirmado la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2.

Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por EPIVIGILA.

# Columnas y valores
El archivo Comorbilidad.csv tiene una columna 'Comorbilidad' donde se listan las enfermedades crónicas más frecuentes, 'Hospitalización' para mostrar si la categoría corresponde a 'NO' para los casos sin hospitalización y 'SI' para aquellos que han requerido hospitalización. También hay una serie de columnas '[Fechas]', donde por cada enfermedad crónica en una fila, se reporta el número de casos confirmados que padecen dicha enfermedad (entre casos sin y con hospitalización, respectivamente). El archivo tiene una versión traspuesta (serie de tiempo) con el sufijo "\_T". Todos estos valores están separados entre sí por comas (csv). Además se presenta un archivo en formato estándar con el sufijo "\_std.csv".

# Fuente

Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en: https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS.

# Frecuencia de actualización
Cada 2 a 3 días.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo contempla el número de casos reportando la enfermedad crónica que ha sido calculado a lo reportado en el informe Epidemiológico. En el informe epidemiológico se publican gráficos de porcentajes de casos confirmados con enfermedad crónica de base en las categorías sin y con hospitalización. Adicionalmente, en estos gráficos se muestra la población total en cada categoría (sin y con hospitalización). Los datos de porcentajes y población sin y con hospitalización provenientes del informe epidemiológico pueden encontrarse en https://github.com/MinCiencia/Datos-COVID19/blob/DP34/input/InformeEpidemiologico/Comorbilidad.csv.


**Nota aclaratoria 2:** Previo al 18 de mayo del 2020, los informes de situación Epidemiológica del Ministerio de Salud no entrega información sobre la comorbilidad de pacientes hospitalizados.
