# DP2 - Casos totales por comuna: Descripción
Serie de archivos que dan cuenta de los casos confirmados y casos probables (desde el 19 de junio, informe #27) notificados en cada una de las comunas de Chile, según residencia. Cada uno de los archivos corresponde a un informe publicado por el Ministerio de Salud del país, por fechas en que fueron publicados. 

Se entiende por Caso probable: persona que cumple los criterios de definición de caso sospechoso con una muestra “indeterminada” a SARS-CoV-2 o bien personas en contacto estrecho con un caso confirmado que desarrollan al menos un síntoma compatible con COVID-19. 

Se entiende por Caso confirmado: persona notificada que cumple los criterios de definición de caso sospechoso o probable con una muestra positiva a SARS-CoV-2, o bien persona no notificada con un registro de resultado de laboratorio positiva a SARS-CoV-2.

Se entiende por comuna de residencia la comuna que la persona declara como su vivienda habitual. 

# Columnas y valores
El archivo contiene las columnas 'Región', ‘Código Región’, 'Comuna', ‘Código comuna’, 'Población' y 'Casos Confirmados'. Estos valores están separados entre sí por comas (csv).

# Fuente

Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS. 

# Frecuencia de actualización
Cada 2 a 3 días. 

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero. 

**Nota aclaratoria 2:**  Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 3:** Previo al 15 de abril de 2020 los informes epidemiológicos del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas. 

**Nota aclaratoria 4:** Acorde a lo informado por Epidemiología MINSAL, los datos de residencia son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la investigación epidemiológica. A raíz de eso se recomienda utilizar el [Data Product 1 - Casos totales por comuna incremental](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto1) para contar con la información más actualizada.

**Nota aclaratoria 5:** Los datos de población provienen de las proyecciones estadísticas del INE, con base en el CENSO 2017 (para más detalles revisar https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion).
