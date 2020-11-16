# DP30 - Pacientes Hospitalizados en UCI con Ventilación Mecánica: Descripción
Este producto da cuenta del número de pacientes hospitalizados y que se encuentran en la Unidad de Cuidados intensivos. Específicamente se describe el número de pacientes conectados a ventilación mecánica invasiva, pacientes sin ventilación mecánica y aquellos conectados a ventilación mecánica no invasiva y que son casos confirmados por COVID-19. Se concatena la historia de reportes diarios publicados por el Ministerio de Salud del país.

Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por la Unidad de Gestión de Camas Críticas.

# Columnas y valores
El archivo PacientesVMI.csv contiene el reporte diario de la cantidad de pacientes conectados a ventilación mecánica invasiva, sin ventilación mecánica y en ventilación mecánica no invasiva, por cada '[Fecha]' reportada en las columnas. El archivo PacientesVMI_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. El archivo PacientesVMI_std.csv muestra la información del archivo PacientesVMI.csv pero en formato estándar (unpivoted). Todos estos valores están separados entre sí por comas (csv).

# Fuente
Reportes diarios publicados períodicamente por el Ministerio de Salud con los datos reportados por la Unidad de Gestión de Camas Críticas. Ver en: https://www.gob.cl/coronavirus/cifrasoficiales/#reportes

# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** Previo al 11 de abril del 2020, los reportes diarios del Ministerio de Salud no entregaban datos sobre el número de pacientes hospitalizados conectados a ventilación mecánica invasiva confirmados por COVID-19.

**Nota aclaratoria 2:** Previo al 24 de mayo del 2020, los reportes diarios del Ministerio de Salud no entregaban datos sobre el número de pacientes hospitalizados en la unidad de cuidados intensivos que no estuvieran conectados a ventilación mecánica invasiva o que estuvieran conectados a ventilación mecánica no invasiva y que fuesen casos confirmados por COVID-19.
