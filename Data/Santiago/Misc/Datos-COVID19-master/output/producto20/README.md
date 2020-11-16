# DP20 - Ventiladores a nivel nacional: Descripción
Este producto da cuenta del número total de ventiladores en el Sistema Integrado Covid 19, el número de ventiladores disponibles y el número de ventiladores ocupados, para cada fecha reportada.  Se concatena la historia de los reportes diarios publicados por el Ministerio de Salud del país.

Se entiende por número total a todos los ventiladores operativos en el Sistema Integrado Covid 19.

# Columnas y valores
En archivo NumeroVentiladores.csv, contiene las columnas 'Estado' (con valores total, disponibles, ocupados), una serie de columnas '[Fecha]', donde en cada una están los valores reportados a nivel nacional. El archivo NumeroVentiladores_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Reportes diarios publicados períodicamente por el Ministerio de Salud. Ver en: https://www.gob.cl/coronavirus/cifrasoficiales/#reportes
 
# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** Previo al 14 de abril del 2020, los reportes diarios del Ministerio de Salud no entrega información sobre la cantidad de ventiladores operativos, disponibles u ocupados.
