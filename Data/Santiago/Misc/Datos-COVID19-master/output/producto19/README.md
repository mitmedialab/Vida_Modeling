# D19 - Casos activos por fecha de inicio de síntomas y comuna: Descripción
Archivo que da cuenta del número de casos confirmados activos notificados en cada una de las comunas de Chile, según residencia, y concatena la historia de los informes epidemiológicos publicados por el Ministerio de Salud del país.

Se entiende por caso confirmado activo a la persona viva que cumple con los criterios de definición de casos sospechoso con una muestra positiva de SARS-CoV-2, cuya fecha de inicio de síntomas en la notificación es menor o igual a 14 días a la fecha del reporte actual (considera solo vivos).

# Columnas y valores
El archivo CasosActivosPorComuna.csv, contiene las columnas 'Región', 'Código región', 'Comuna', 'Código comuna', 'Población', y una serie de columnas '[Fecha]', donde en cada una están los 'Casos activos' reportados en cada publicación de Epidemiología, por cada comuna, en cada fecha reportada. El archivo CasosActivosPorComuna_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en: https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS.
 
# Frecuencia de actualización
Cada 2 a 3 días.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero.

**Nota aclaratoria 2:** Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs.

**Nota aclaratoria 3:** Previo al 13 de abril del 2020, los informes epidemiológicos del Ministerio de Salud no entregaban datos sobre los casos confirmados activos notificados en comunas.

**Nota aclaratoria 4:** Casos activos en este reporte (a diferencia del reporte en el [Producto 5](../producto5), corresponde al resultado de la investigación epidemiológica y considera activos a casos durante los primeros 14 días después de la fecha de inicio de sus síntomas.

**Nota aclaratoria 5:** Los datos de población provienen de las proyecciones estadísticas del INE, con base en el CENSO 2017 (para más detalles revisar https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion).
