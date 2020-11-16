# DP18 - Tasa de incidencia historica por comuna y total regional: Descripción
Archivo que da cuenta de la tasa de incidencia acumulada en cada una de las comunas de Chile, y concatena la historia de los informes epidemiológicos publicados por el Ministerio de Salud del país.

Se entiende por tasa de incidencia al número total de casos confirmados desde el primer caso confirmado hasta la fecha de elaboración del informe epidemiológico, en relación a la población susceptible de enfermar en un periodo determinado.

Se entiendo por caso confirmado a la persona que cumple con los criterios de definición de casos sospechoso con una muestra positiva de SARS-CoV-2.

# Columnas y valores
El archivo TasadeIncidencia.csv, contiene las columnas 'Región', 'Código región', 'Comuna', 'Código comuna', 'Población', y varias columnas '[Fecha]', donde cada una tiene la 'Tasa de incidencia' reportadas en cada publicación de Epidemiología, para cada comuna, en las fechas reportadas. El archivo TasadeIncidencia_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en: https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS.
 
# Frecuencia de actualización
Cada 2 a 3 días.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero.

**Nota aclaratoria 2:** Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs.

**Nota aclaratoria 3:** Previo al 15 de abril de 2020 los informes epidemiológicos del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas.

**Nota aclaratoria 4:** Los datos de población provienen de las proyecciones estadísticas del INE, con base en el CENSO 2017 (para más detalles revisar https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion).
