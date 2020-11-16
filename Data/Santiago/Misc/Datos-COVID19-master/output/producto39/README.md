# DP39 - Casos confirmados de COVID-19 según fecha de inicio de síntomas y notificación: Descripción
Set de 3 archivos que dan cuenta de los casos confirmados de COVID-19 según la fecha de inicio de síntomas y fecha de notificación a nivel nacional para los casos confirmados, no notificados y probables. Refleja la información del último informe epidemiológico publicado por el Ministerio de Salud del país.

Se entiende por fecha de inicio de síntomas el momento de la manifestación clínica de la enfermedad. Se entiende por fecha de notificación el día, mes y año en que el médico tratante realizó el registro del caso en el sistema epivigila. 

# Columnas y valores
El archivo NotificacionInicioSintomas.csv contiene la columna 'Categoria' para categorizar los casos por fecha de 'Notificación' y de 'Inicio de Sintomas', seguida por la 'Serie' que corresponde a la curva 'confirmada', 'no notificada' y 'probable'. A esto sigue la serie de columnas correspondientes a las fechas de los registros correspondientes a cada día reportado en el informe Epidemiológico. También se incluye su versión transpuesta con sufijo '_T.csv' y en formato estándar con sufijo '_std.csv'. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS. 

# Frecuencia de actualización

Cada 2 a 3 días. 

# Notas aclaratorias

**Nota aclaratoria 1:** Los datos son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la vigilancia e investigación epidemiológica desarrollada por el Departamento de Epidemiología del Ministerio de Salud del país.

**Nota aclaratoria 2:** Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 3:** Acorde a lo informado por Epidemiología MINSAL, la fecha de inicio de síntomas corresponde al momento de la manifestación clínica de la enfermedad, y son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la investigación epidemiológica.

**Nota aclaratoria 4:** En el informe epidemiológico correspondiente al 23 de Junio, la tabla 23 (páginas 67, 68 y 69) presenta errores entre las fechas 19 y 21 de junio que se corrigen en este repositorio

**Nota aclaratoria 5:** Las series 'confirmada', 'no notificada' y 'probable' han sido incluidas en el informe epidemiológico a partir del 31 de Julio 2020
