# DP16 - Casos por genero y grupo de edad: Descripción
Archivo que da cuenta del número acumulado de casos confirmados distribuidos por género y grupo de edad, para cada fecha reportada. Este concatena la historia de los informes epidemiológicos publicados por el Ministerio de Salud del país.

Se entiendo por caso confirmado a la persona que cumple con los criterios de definición de casos sospechoso con una muestra positiva de SARS-CoV-2.

# Columnas y valores
El archivo CasosGeneroEtario.csv contiene las columnas 'Grupo de edad' tal como lo reporta el departamento de Epidemiología para esta categoría, en incrementos de 5 años, desde 0 hasta 79, con '80 y más' como último rango; 'Sexo' con dos distinciones 'M' (las 17 primeras filas) y 'F' (las 17 últimas filas); y una serie de columnas '[Fecha]', donde se encuentra el número acumulado de casos confirmados para el rango etario y género reportados en cada publicación de Epidemiología MINSAL. El archivo CasosGeneroEtario_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en: https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

Informes de situación COVID-19 publicados periódicamente por el Ministerio de Salud de Chile. Ver en: http://epi.minsal.cl/informes-covid-19/
 
A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS.

# Frecuencia de actualización
Informe epidemiológico: Cada 2 a 3 días.

Informe situación COVID-19: Diaria

# Notas aclaratorias

**Nota aclaratoria 1:** Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs.

**Nota aclaratoria 2:** Previo al 5 de abril de 2020 los informes epidemiológicos del Ministerio de Salud no entregaban datos de distribución de casos confirmados por género y grupo de edad.

