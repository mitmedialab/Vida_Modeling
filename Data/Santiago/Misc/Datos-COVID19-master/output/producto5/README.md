# DP5 - Totales Nacionales Diarios: Descripción
Set de 2 archivos sobre casos a nivel nacional. El primero de ellos (TotalesNacionales.csv) incluye los casos nuevos confirmados, totales o acumulados, fallecidos a nivel nacional, activos y recuperados según fecha de diagnóstico y según fecha de inicio de síntomas, reportados diariamente por el Ministerio de Salud desde el 03-03-2020 y proyectados desde el 8 de junio para el caso de activos y recuperados por fecha de dianóstoco según criterios de la autoridad sanitaria.

Se entiende por caso confirmado la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2.

Se entiende por caso nuevo sin síntomas por casos que han sido confirmados COVID-19 positivos pero no tienen manifestación clínica de la enfermedad. La autoridad de salud indicó que estos casos se han testeado por cercanía con contagiados de diversas índoles.

Se entiende por casos totales o acumulados el número total de casos confirmados desde el primer caso confirmado hasta la fecha de elaboración del reporte o informe. 

Se entiende en este reporte por "recuperados por fecha de diagnóstico" la proyección de personas que tras ser confirmadas de COVID-19, han estado en cuarentena pasando 14 días sin síntomas. Se entiende en este reporte por "recuperados por fecha de inicio de síntomas" la proyección de recuperados que tras ser confirmados, reportan su fecha de inicio de síntomas y han transcurrido 14 días o más desde ella.

Se entiende en este reporte por casos activos la diferencia entre el total de casos confirmados y (personas recuperadas y personas fallecidas). Para calcularlos segun fecha de incio de síntomas se utilizan los recuperados por fecha de incio de síntomas, y por fecha de diagnóstico los recuperados por fecha de diagnóstico.

# Columnas y valores
El primer archivo (TotalesNacionales.csv) contiene las filas ‘Fecha’, ‘Casos nuevos’, ‘Casos totales’, ‘Fallecidos’, ‘Casos activos por FIS’, ‘Casos recuperados por FIS’, 'Casos activos por FD’, ‘Casos recuperados por FD’. Estos valores están separados entre sí por comas (csv).

# Fuente
Ministerio de Salud. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/

# Frecuencia de actualización
Actualización diaria. 

# Notas aclaratorias

**Nota aclaratoria 1**:  Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 2**: Previo al 15 de abril de 2020 los reportes del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas.

**Nota aclaratoria 3**: A partir del 2 de junio las series por Fecha de Diagnóstico se dejaron de reportar diariamente, pero se mantiene el cálculo acá a pedida de varios usiarios que quieren continuar utilizando dichas curvas.

