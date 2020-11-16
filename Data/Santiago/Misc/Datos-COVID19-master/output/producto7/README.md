# DP7 - Exámenes PCR por región: Descripción
Set de 2 archivos que dan cuenta del número de exámenes PCR realizados por región reportados diariamente por el Ministerio de Salud, desde el 09-04-2020. 

El proceso ocurre hasta la fecha de la siguiente manera: 1) Paciente va al médico 2) Médico identifica síntomas que constituyen caso sospechoso y ordena tomar muestras y realizar test PCR 3) Las muestras van al laboratorio para test PCR.

# Columnas y valores
El archivo (PCR.csv) contiene las columnas ‘Región’, ‘Código Región’ y ‘Población’, seguidas por columnas correspondientes a ‘[Fecha]’. Estas últimas columnas, ‘[Fecha]’ indican el número de exámenes realizados por región, desde el 09-04-2020 hasta la fecha. El archivo PCR_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Reporte diario del Ministerio de Salud. Ver en: https://www.gob.cl/coronavirus/cifrasoficiales/#reportes

# Frecuencia de actualización
Actualización diaria. 

# Notas aclaratorias

**Nota aclaratoria 1:** Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 2:** El número de exámenes PCR realizados no refleja necesariamente la cantidad de muestras tomadas por región. En algunos casos el número de exámenes PCR realizados es menor al número de muestras dado que ha sido alcanzada la capacidad máxima de diagnóstico de la región. Por lo mismo, algunas de las muestras son enviadas a laboratorios ubicados fuera de la región de referencia. 
