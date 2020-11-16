# DP34 - Cruce entre cuarentenas y manzanas censales
Los datos publicos del Censo 2017 cuentan con información demografica valiosa para distintas regiones geografica, como lo son la cantidad de habitantes, calidad de las viviendas o la distribución etarea. La región geografica más desagregada para la cual se encuentra disponible esta información se denomina **Manzana Censal**. Este producto indica las manzanas censales que pertenecen a cada zona de cuarentena (1).

# Columnas y valores
El archivo cuenta con 4 columnas, las cuales se describen a continuación:
* 'CuarentenaID': Id de la cuarentena en el GeoJson publicado en (1).
* 'Nombre': Nombre de la cuarentena según (1).
* 'ManzanasInFull': Listado de manzanas censales **completamente contenidas** en la zona de cuarentena (corresponden al MANZENT en los datos del censo).
* 'ManzanasInPartial': Listado de manzanas censales **parcialmente contenidas** en la zona de cuarentena (corresponden al MANZENT en los datos del censo). Se considera que una manzana censal está parcialmente contenida si tiene al menos un punto de su interior dentro de la zona de cuarentena

# Datos utilizados
* (1) Zonas de cuarentenas: Se utiliza el archivo GeoJSON de las cuarentenas publicado en https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto29
* (2) Microdatos Censo 2017 a nivel de manzana censal: Publicados por el Instituto Nacional de Estadisticas (INE) desde http://geoine-ine-chile.opendata.arcgis.com/datasets/54e0c40680054efaabeb9d53b09e1e7a_0

# Información adicional
* El producto29 (https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto29) contiene la información de los días que cada cuarentena está activa.

