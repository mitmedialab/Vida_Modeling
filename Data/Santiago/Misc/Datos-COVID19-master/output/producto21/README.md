# DP21 - Sintomas por Casos Confirmados e informado en el último día: Descripción
Este producto da cuenta de la sintomatología reportada por los casos confirmados. También da cuenta de la sintomatología reportada por casos confirmados que han requerido hospitalización. Se concatena la historia de los informes de Situación Epidemiológica publicados por el Ministerio de Salud del país.

Los archivos Sintomas('.csv', '_T.csv' y '_std.csv') ensamblan la sintomatología de casos sin hospitalización y casos hospitalizados. 

Los archivos SintomasCasosConfirmados('.csv', '_T.csv' y '_std.csv') contienen la información de los archivos 'Sintomas' con categoría 'Hospitalización == NO', mientras que los archivos SintomasHospitalizados('.csv', '_T.csv' y '_std.csv') contienen la sintomatología de los archivos 'Sintomas' con categoría 'Hospitalización == SI'. Estos sets de archivos serán deprecados en 2 semanas. Se mantendrá la información concatenada en los archivos Sintomas('.csv', '_T.csv' y '_std.csv').

Se entiende por caso confirmado la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2.

Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por EPIVIGILA.

# Columnas y valores

El archivo Sintomas.csv contienen la columna 'Sintomas' y una serie de columnas '[Fecha]', donde por cada síntoma en una fila se reporta el número acumulado a cada fecha de casos que han reportado dicho síntoma. La sintomatología de los casos que no han requerido hospitalización a la fecha está reflejada entre las filas: 2 - 16 ('Hospitalización == NO'). Mientras que la sintomatología de los casos hospitalizados está reflejada entre las filas 17 - 31 ('Hospitalización == SI').

Los archivos SintomasCasosConfirmados.csv y SintomasHospitalizados.csv tienen una columna 'Síntomas' y una serie de columnas '[Fechas]', donde por cada síntoma en una fila, se reporta el número acumulado a cada fecha de casos confirmados con dicho síntoma (entre casos confirmados y hospitalizados, respectivamente). Cada archivo tiene una versión traspuesta (serie de tiempo) con el sufijo "\_T". Todos estos valores están separados entre sí por comas (csv).

# Fuente
Informes de Situación Epidemiológica publicados períodicamente por el departamento de Epidemiología del Ministerio de Salud con los datos reportados por EPIVIGILA. Ver en: http://epi.minsal.cl/informes-covid-19/

# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo contempla el número acumulado de casos reportando la sintomatología.

**Nota aclaratoria 2:** Posterior al 11 de abril del 2020, Los informes de Situación Epidemiológica no entregan información sobre la sintomatología de casos confirmados u hospitalizados.

**Nota aclaratoria 3:** Previo al 24 de marzo del 2020, los  informes de situación Epidemiológica del Ministerio de Salud no entrega información sobre la sintomatología de pacientes hospitalizados.

**Nota aclaratoria 4:** Previo al 10 de marzo del 2020, no hay publicaciones de los informes de situación Epidemiológica del Ministerio de Salud.

**Nota aclaratoria 5:** No todos los informes de situación COVID - 19 de EPI MINSAL contienen información sobre los síntomas.

**Nota aclaratoria 6:** Los informes de situación Epidemiológica del Ministerio de Salud se publican con fecha del día de corte. Los datos en este repositorio cotejan las fechas indicadas en el texto de la fuente utilizada con las dadas en el reporte diario e informe Epidemiológico del Ministerio de Salud.
