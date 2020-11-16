# DP38 - Casos fallecidos por comuna: Descripción
Archivo que da cuenta del número de casos fallecidos en cada una de las comunas de Chile según su residencia, y concatena la historia de los informes epidemiológicos publicados por el Ministerio de Salud del país.

Se entiende por casos fallecidos a las muertes confirmadas debido a COVID-19 y que se encuentran debidamente registradas en la base de datos del Registro Civil e Identificación. Para estos casos, la comuna de residencia fue obtenida desde la plataforma EPIVIGILA, o bien, se asignó la comuna de circunscripción donde fue inscrita la defunción en los casos sin comuna de residencia.

# Columnas y valores
El archivo CasosFallecidosPorComuna.csv, contiene las columnas 'Región', 'Código región', 'Comuna', 'Código comuna', 'Población', y una serie de columnas '[Fecha]', donde cada fecha tiene los 'Casos fallecidos' reportados en cada publicación de Epidemiología. El archivo CasosFallecidosPorComuna_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en: https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS.
 
# Frecuencia de actualización
Cada 2 a 3 días.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero.

**Nota aclaratoria 2:** Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs.

**Nota aclaratoria 3:** Previo al 12 de junio del 2020, los informes epidemiológicos del Ministerio de Salud no entregaban datos sobre los casos fallecidos por COVID-19 en comunas.

**Nota aclaratoria 4:** Los datos de población provienen de las proyecciones estadísticas del INE, con base en el CENSO 2017 (para más detalles revisar https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion).
