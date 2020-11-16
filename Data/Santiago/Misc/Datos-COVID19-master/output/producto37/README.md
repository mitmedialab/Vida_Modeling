# DP37 - Defunciones por COVID en Chile (reporte diario, provisorio): Descripción.
 
Los datos en defunciones.csv (y sus versiones transpuestas y std) provienen de los registros de inscripciones de fallecimientos del Registro Civil de Chile, cruzados diariamente con el registro de los resultados de laboratorio para el diagnóstico COVID19 en Chile (RT-PCR), que consolida y cura el Departamento de Epidemiología del Minsal.
 
Los criterios para identificar fallecidos debido a COVID19 para efectos del reporte diario en defunciones.csv son:
1) Certificado de defunción incluye COVID19 o algún término relacionado (se excluyen causas externas, como trauma).
2) Existe un examen positivo de RT-PCR para SARS-CoV-2 en la base de datos de laboratorio.
 
A su vez, los datos en defunciones_deis.csv (y sus versiones transpuestas y std) provienen del Departamento de Estadística e Información del Minsal (DEIS). El DEIS hace mejoras al registro de defunciones a medida que analiza diversas fuentes de datos, estas mejoras estudian la causa de defunción indicada en el certificado médico y la presencia de resultados RT-PCR, en caso de ser la defunción por cuadro clínico compatible a COVID19, y contar con PCR(-), o no haber sido testeado se incluye como sospechoso, mientras que si existe PCR(+) se incluye como confirmado.

En ambos archivos, la columna “Defunciones” se refiere a la fecha de defunción (no es la fecha de inscripción).
 
# Columnas y valores
Los archivos defunciones contienen las columnas 'Defunciones' y múltiples columnas correspondientes a '[fecha]'. Estas últimas columnas, ‘[fecha]’, contienen las 'Defunciones (por fecha de fechas de defunción)' inscritas en el Registro Civil de Chile con relación a COVID19, que al cruzar con la base de laboratorios tienen PCR positivo, y son datos provisorios a la fecha de publicación que se pueden actualizar retroactivamente.

Los archivos defunciones_deis contienen las columnas 'Confirmados', 'Sospechosos' y múltiples columnas correspondientes a '[fecha]'. Estas últimas columnas, ‘[fecha]’, contienen las 'Defunciones (por fecha de fechas de defunción)' confirmadas o sospchosas.
 
# Fuente
Servicio de Registro Civil de Chile y División de Planificación Sanitaria del Ministerio de Salud de Chile.
 
# Frecuencia de actualización
Diaria (Registro Civil) y Semanal (DEIS)
 
# Notas aclaratorias
**Nota aclaratoria 1:** El Registro Civil de Chile y el Ministerio de Salud de Chile elaboran esta información en base a las actuaciones que le son propias y que se encuentran registradas en una fecha y hora determinada, sin embargo, estas son variables, ya que pueden ser objeto de rectificación no constituyendo, en consecuencia, una estadística oficial del Estado de Chile, materia que es competencia del Instituto Nacional de Estadísticas (INE) (número de fallecidos) y del Departamento de Estadísticas e Información en Salud (DEIS), Minsal (causas de defunción).
 
**Nota aclaratoria 2:** Los datos son provisorios. Los valores reportados por día pueden variar retroactivamente en cada actualización, en la medida que se recibe información de exámenes de laboratorio pendientes.
