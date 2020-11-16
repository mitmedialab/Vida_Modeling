# DP 34 - Datos históricos de calidad del aire por hora: Descripción

Cada archivo entrega los datos de la emisión de un contaminante durante un año con frecuencia horaria junto con la información de las estaciones de medición. Existe un archivo para cada contaminante y para cada año.

Los contaminantes disponibles y sus unidades de medida son los siguientes: Dióxido de azufre (SO2) en partes por billón (ppb), Dióxido de Nitrógeno (NO2) en partes por billón (ppb), Monóxido de Carbono (CO) en partes por millón (ppm), Ozono (O3) en partes por billón (ppb), Material Particulado MP 10 en microgramos por metro cúbico normalizado (μg/m3N) y Material Particulado MP 2.5 en microgramo por metro cúbico (μg/m3).

Las coordenadas de la estación se encuentran en las filas UTM_Este y UTM_Norte. Corresponden a la ubicación de las estaciones y están en formato UTM y se entregan en dos filas distintas la coordenada Este (E) y la coordenada Norte (N). Para todas las estaciones el Huso horario es 19.

La comuna corresponde a donde está ubicada la estación.

# Columnas y valores

Cada archivo [CONTAMINANTE]-[20XX].csv contiene las filas  correspondientes al [CONTAMINANTE] medido en la Estación ‘[Nombre de estacion]’. Además, las primeras filas corresponden a ‘Region’, ‘Codigo Region’, ‘Comuna’, ‘Codigo Comuna’, 'UTM_Este’ y UTM_Norte’, para luego entregar las fechas y horas de medición. Todos estos valores están separados entre sí por comas (csv).

# Fuente

Los datos fueron entregados por el Sistema Nacional de Calidad del Aire del Ministerio de Medio Ambiente. Estos datos son públicos en una mayor agregación en https://sinca.mma.gob.cl/

# Frecuencia de Actualización

Esta información es histórica, por lo que no se actualizará.

# Notas Aclaratorias

**Nota Aclaratoria 1**: La información disponible para todo el país es de Material Particulado 2.5 (MP 2.5) y Material particulado 10 (MP 10). El resto de las emisiones (gases) solo están disponibles para la Región Metropolitana y algunas estaciones en regiones.

**Nota Aclaratoria 2**: Los espacios en blanco corresponden a datos invalidados. Las invalidaciones pueden deberse a distintos motivos (falla de equipo, falla de energía, mantención, etc.) y se les asigna el código de invalidación correspondiente (códigos definidos en el artículo 17 del decreto Nº 61, de 2008, del Ministerio de Salud). 
