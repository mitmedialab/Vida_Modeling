# DP48 - Encuesta Diaria Realidad Nacional Medicina Intensiva: Descripción
Archivo que da cuenta del número de camas ocupadas por servicio de salud a lo largo del país, considerando los tipos de 
camas, incluyendo: camas intensivas ocupadas, camas intensivas totales, camas intermedias ocupadas, camas intermedias 
totales, ventiladores mecanicos invasivos (VMI) en uso por pacientes Covid19 confirmados y Covid19 sospechosos, Vmi 
ocupados y Vmi totales. Estos valores son levantados y reportados de manera diaria por los miembros de la SOCHIMI y la 
Universidad Finis Terrae, por fecha y servicio de salud, y disponibilizados por el Laboratorio de Biología Computacional
 de la Fundación Ciencia & Vida.

El archivo 'SOCHIMI.csv' tiene las siguientes columnas:

* **Codigo region**: código regional
* **Region**: nombre de la región
* **Servicio salud**: Servicio de Salud
* **Serie**: nombre de la serie de datos
    * **Camas ocupadas intensivo**: número de camas UCI ocupadas
    * **Camas totales intensivo**: número de camas UCI totales
    * **Camas ocupadas intermedio**: número de camas UTI ocupadas
    * **Camas totales intermedio**: número de camas UTI totales
    * **VMI COVID19 confirmados**: número de pacientes conectados a ventilación con COVID19
    * **VMI COVID19 sospechosos**:  número de pacientes conectados a ventilación con sospecha de COVID19
    * **VMI ocupados**: número de ventiladores ocupados por todo tipo de pacientes
    * **VMI totales**: número de ventiladores totales
* **Fechas**: valor de la serie correpondiente para la fecha indicada en el título de la columna

# Fuente
* Ingreso y recopilación de datos: SOCHIMI
* Preprocesamiento y manejo de datos: Fundación Ciencia y Vida

# Frecuencia de actualización
Semanal

# Notas aclaratorias
