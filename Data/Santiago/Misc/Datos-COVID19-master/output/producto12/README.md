# DP12 - Enriquecimiento del Data Product 7: Descripción
El [Data Product 7](../producto7) con todos los datos compilados en formato CSV y JSON, en un solo archivo, llamados producto7.csv y producto7.json respectivamente. Set de 2 archivos, en formato CSV y JSON, que dan cuenta de la tasa de incidencia acumulada y el número de PCR realizados en cada una de las regiones de Chile, según los datos diariamente reportados por el Ministerio de Salud, desde el 09-04-2020.

Se entiende por casos acumulados el número total de casos confirmados desde el primer caso confirmado hasta la fecha de elaboración del reporte o informe. 

Se entiende por tasa de incidencia acumulada el número total de casos acumulados en relación a la población susceptible de enfermar en un período determinado. 

# Columnas y valores
Los archivos contienen las columnas ‘Región’, ‘Población’, ‘Fecha’, ‘PCR Realizados’, ‘Región ID’, y ‘Tasa’. Estos valores están separados entre sí por comas (csv), y organizados en tuplas en el JSON.

# Fuente
Reporte diario del Ministerio de Salud. Ver en:
https://www.gob.cl/coronavirus/cifrasoficiales/#reportes

# Frecuencia de actualización
Actualización diaria. 

# Notas aclaratorias
**Nota aclaratoria 1**: Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs.

**Nota aclaratoria 2**: Los datos son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la vigilancia e investigación epidemiológica desarrollada por el Departamento de Epidemiología del Ministerio de Salud del país.

**Nota aclaratoria 3**: Los datos de población provienen de las proyecciones estadísticas del INE, con base en el CENSO 2017 (para más detalles revisar https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion).
