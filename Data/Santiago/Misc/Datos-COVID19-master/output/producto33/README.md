# DP33 - Movilidad en Chile: Descripción
Este producto contiene 3 series de tiempo que provienen del análisis realizado por el Instituto de Data Science de la Universidad del Desarrollo considerando el movimiento de los teléfonos móviles conectados a la red de Telefónica en el territorio nacional, de manera agrupada y anónima.  

La primera serie de tiempo (IM interno) representa la evolución del índice de movilidad interno a la comuna es una medida de los viajes que ocurren al interior de dicha unidad administrativa.  

La segunda serie de tiempo (IM externo) representa la evolución del índice de movilidad externo la comuna es una medida tanto de los viajes que tienen origen al interior de la comuna y destino al exterior de la comuna, como de los viajes que tienen origen al exterior de la comuna y destino al interior de la comuna.

La tercera serie de tiempo (IM) representa la evolución del índice de movilidad, que es la suma de estos últimos dos índices.

# Columnas y valores
Los archivos contienen las columnas 'Región', 'Código Región', 'Comuna', 'Código comuna', 'Población','Superficie_km2' y múltiples columnas correspondientes a '[fecha]'. Estas últimas columnas, '[fecha]', contienen el valor para el índice en la fecha indicada.

# Fuente
Instituto de Data Science de la Universidad del Desarrollo Bravo, Loreto, and Ferres, Leo. (2020). *The IM (Mobility Index) dataset*, electronic dataset, UDD and Ministry of Science, Chile.

# Frecuencia de Actualización
Mensual.

# Más información sobre cómo se obtienen estos datos
El Instituto de Data Science (IDS) de la Facultad de Ingeniería de la Universidad del Desarrollo (UDD) con el apoyo de Telefónica Chile y CISCO, convocaron a un equipo de expertos nacionales e internacionales para para proveer información actualizada y precisa sobre la movilidad en Chile en tiempos de cuarentena.

## Método
Los índices en este producto consideran datos anonimizados del periodo desde antes del comienzo de la crisis sanitaria (26 de febrero, 2020).

Se utilizaron registros anonimizados y agregados de telefonía para estimar el número de viajes entre comunas.  Es importante destacar que este set de datos no da la ubicación exacta de los dispositivos sino que la antena a la que se conectó. Es decir, ya por diseño tenemos una primera anonimización de la ubicación. El tema de la privacidad es fundamental para los participantes en esta iniciativa y se han adoptado los protocolos internacionales más estrictos.

Para efectos de este trabajo, consideramos un viaje el paso de una antena a otra. Para dos comunas A y B, tenemos entonces que el número de viajes de A a B queda estimado como la suma de los viajes entre antenas que se encuentran dentro de A y antenas que se encuentran dentro de B.

Para poder comparar las comunas, se utiliza un índice de movilidad (IM). El IM corresponde a cuantos viajes se realizaron dentro de una comuna específica normalizado por el número de habitantes de la comuna.

Es interesante distinguir entre los viajes dentro de la comuna `IM_interno` y los que cruzan el límite comunal `IM_externo`.
