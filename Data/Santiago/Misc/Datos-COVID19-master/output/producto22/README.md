# DP22 - Pacientes COVID-19 hospitalizados por grupo de edad: Descripción
Este producto contiene dos archivos, 1) el número acumulado del total de pacientes hospitalizados con diagnóstico COVID-19 por rango de edad y género y 2) el número acumulado de pacientes internados con diagnóstico COVID-19 en la Unidad de Cuidados Intensivos (UCI) por rango de edad. Se concatena la historia de los informes de Situación Epidemiológica publicados por el Ministerio de Salud del país.
Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por EPIVIGILA.
# Columnas y Valores
El archivo HospitalizadosEtario_Acumulado.csv contiene las columnas 'Grupo de edad','Sexo' y una serie de columnas con '[Fecha]', donde para cada fila con rango etareo (en bloques de 15 años), se indica por fecha la cantidad acumulada de hospitalizados por género. En el archivo HospitalizadosUCI_Acumulado.csv está la columa 'Grupo de edad' y una serie de columnas con '[Fecha]', donde para cada fila con rango etareo (en bloques distintos al primero), se reportan los hospitalizados UCI acumulados. Este último no tiene desglose por género. Cada archivo tiene una versión traspuesta (serie de tiempo) con el sufijo "\_T". 

Debido a un cambio en los rangos etareos el 22 de abril del 2020 los archivos presentan dos bloques con rangos de edad diferentes. Entre las filas 2 a 13 del archivo HospitalizadosEtario_Acumulado.csv, se encuentran los registros entre el 24 de marzo del 2020 al 20 de abril del 2020, para los géneros Masculino y Femenino, con rangos de edad:

00-15 años<br/>
15-29 años<br/>
30-44 años<br/>
45-59 años<br/>
60-79 años<br/>
80 y más años<br/>

A partir del 22 de abril del 2020 los rangos de edad, para los género Masculino y Femenino, publicados se describen entre las filas 14 a 27 como:

00-5 años<br/>
5-17 años<br/>
18-49 años<br/>
50-59 años<br/>
60-69 años<br/>
70-79 años<br/>
80 y más años<br/>

En el caso del archivo HospitalizadosUCI_Acumulado.csv, entre el 13 y el 20 de abril del 2020, los rangos de edad que presentan registros se encuentran entre las filas 2 a 7, y están descritos por:

< 1 años<br/>
1 - 4 años<br/>
5 - 14 años<br/>
15 - 44 años<br/>
45 - 64 años<br/>
65 y más años<br/>

A partir del 22 de abril del 2020 los rangos de edad que presentan registros se encuentran entre las filas 8 a 14, descritos como:

00-5 años<br/>
5-17 años<br/>
18-49 años<br/>
50-59 años<br/>
60-69 años<br/>
70-79 años<br/>
80 y más años<br/>

# Fuente

Informes de Situación Epidemiológica publicados períodicamente por el departamento de Epidemiología del Ministerio de Salud con los datos reportados por EPIVIGILA. Ver en: http://epi.minsal.cl/informes-covid-19/

# Frecuencia de actualización

Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo contempla el número acumulado de pacientes hospitalizados.

**Nota aclaratoria 2:** Previo al 23 de marzo del 2020, los informes de situación Epidemiológica del Ministerio de Salud no entregaban datos sobre la distribución del número de pacientes hospitalizados por rango etario.

**Nota aclaratoria 3:** Los informes de Situación Epidemiológica con fecha de publicación posterior al 21 de abril presentan un cambio en los rangos etarios. Por esta razón, hay dos escalas para los dichos rangos.

**Nota aclaratoria 4:** Los informes de situación Epidemiológica del Ministerio de Salud se publican con fecha del día de corte. Los datos en este repositorio cotejan las fechas indicadas en el texto de la fuente utilizada con las dadas en el reporte diario e informe Epidemiológico del Ministerio de Salud.
