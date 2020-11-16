# DP25 - Casos actuales por fecha de inicio de síntomas y comuna: Descripción
Archivo que da cuenta del número de casos actuales en cada una de las comunas de Chile según su fecha de inicio de síntomas, residencia, y concatena la historia de los informes epidemiológicos publicados por el Ministerio de Salud del país.

Se entiende por caso  actual por fecha de inicio de síntomas a la persona que cumple con los criterios de definición de casos sospechoso con una muestra positiva de SARS-CoV-2, cuya fecha de inicio de síntomas en la notificación es menor o igual a 14 días a la fecha del reporte (considera vivos y fallecidos).

Se entiende por fecha de inicio de síntomas el momento de la manifestación clínica de la enfermedad. Se entiende por comuna de residencia la comuna que la persona declara como su vivienda habitual.

# Columnas y valores
El archivo CasosActualesPorComuna.csv, contiene las columnas 'Región', 'Código región', 'Comuna', 'Código comuna', 'Población', y una serie de columnas '[fecha]', donde cada fecha tiene los 'Casos actuales' reportados en cada publicación de Epidemiología. El archivo CasosActualesPorComuna_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en: https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS.
 
# Frecuencia de actualización
Cada 2 a 3 días.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero.

**Nota aclaratoria 2:** Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs.

**Nota aclaratoria 3:** Previo al 13 de abril del 2020, los informes epidemiológicos del Ministerio de Salud no entregaban datos sobre los casos confirmados actuales notificados en comunas.

**Nota aclaratoria 4:** Los datos de población provienen de las proyecciones estadísticas del INE, con base en el CENSO 2017 (para más detalles revisar https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion).
