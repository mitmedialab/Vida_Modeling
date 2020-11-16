# DP23 - Pacientes críticos COVID-19: Descripción
Este producto da cuenta del número de pacientes hospitalizados con diagnóstico COVID-19 en la Unidad de Cuidados Intensivos (UCI) y se consideran en situación médica crítica. Se concatena la historia de reportes diarios publicados por el Ministerio de Salud del país.

Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por la Unidad de Gestión Centralizada de Camas (UGCC).

# Columnas y valores
El archivo PacientesCriticos.csv contiene el reporte diario de la cantidad de pacientes críticos, por cada '[Fecha]' reportada en las columnas. El archivo PacientesCriticos_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Reportes diarios publicados períodicamente por el Ministerio de Salud con los datos reportados por la Unidad de Gestión de Camas Críticas. Ver en: https://www.gob.cl/coronavirus/cifrasoficiales/#reportes

# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo contempla el número de pacientes internados en UCI en condición crítica, reportado al día.

**Nota aclaratoria 2:** Previo al 23 de marzo del 2020, los reportes diarios del Ministerio de Salud no entregaban datos sobre el número de pacientes en UCI en situación crítica.

