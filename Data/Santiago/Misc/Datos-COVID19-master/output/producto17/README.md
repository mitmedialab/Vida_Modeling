# DP17 - PCR acumulado e informado en el último día por tipo de establecimientos: Descripción

Archivo que da cuenta del número total acumulado de exámenes PCR a nivel nacional y los informados durante las últimas 24 hrs. Se consideran los distintos tipos de establecimientos: Instituto de Salud Pública, Hospitales públicos y Hospitales privados. Este archivo concatena la historia de los reportes diarios publicados por el Ministerio de Salud del país.

# Columnas y valores
El archivo (PCREstablecimiento.csv), contiene las columnas 'Establecimiento' para el tipo de institución; 'Examenes', cuyas 3 primeras filas muestran el total realizado acumulado y las 3 últimas los reportados durante las últimas 24 hrs; y una serie de columnas con '[Fecha]', donde se da el número de exámenes reportados por Epidemiología MINSAL a cada fecha.

# Fuente
Reportes diarios publicados períodicamente por el Ministerio de Salud. Ver en: https://www.gob.cl/coronavirus/cifrasoficiales/#reportes
 
# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** Previo al 30 de marzo de 2020 los reportes diarios del Ministerio de Salud no entregaban datos de exámenes PCR realizados en el país.

**Nota aclaratoria 2:** En este repositorio se corrigieron 3 errores (a la fecha)

1) Error de 87 exámenes adicionales en los exámenes realizados acumulados en establecimientos privados el 25 de mayo 2020. Junto a esto, se encontró un error de 87 exámenes menos en los realizados acumulados en Hospitales públicos en la misma fecha.

2) Error de 1968 exámenes menos en los exámenes realizados acumulados en establecimientos privados el día 27 de mayo. Junto a esto, se encontró un error de 1968 exámenes adicionales en los exámenes realizados acumulados en Hospitales públicos en ese mismo día (27 de mayo 2020)

3) Error de 929 exámenes adicionales en los exámenes realizados acumulados en establecimientos privados el día 1 de junio 2020. Junto a esto, se encontró un error de 929 exámenes menos en los realizados acumulados en Hospitales públicos en ese mismo día (1 de junio 2020)

4) Error de 335 exámenes adicionales en los exámenes realizados acumulados en establecimientos privados el día 4 de junio 2020. Junto a esto, se encontró un error de 335 exámenes menos en los realizados acumulados en Hospitales públicos en ese mismo día (4 de junio 2020)

5) Error de 452 exámenes adicionales en los exámenes realizados acumulados en establecimientos privados el día 24 de junio 2020. Junto a esto, se encontró un error de 452 exámenes menos en los realizados acumulados en Hospitales públicos en ese mismo día (24 de junio 2020)
