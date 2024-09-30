# Capa de red

Un enlace típico hoy tiene 100 Gbps de capacidad. Por lo que se deben tomar decisiones muy rápidas para poder manejar este tráfico. Para esto se utilizan los switches y routers.

La capa de red tiene un diseño simple se encarga de reenviar los paquetes a travez de la red, de punto a punto.

Esta capa a diferncia de las demás ocurre a todos los niveles de la red, y no solo en el borde (edge) de la red.

En la capa de red se distinguen 2 planos principales:

- **Plano de control**: Se encarga de tomar decisiones sobre la ruta que deben seguir los paquetes.
- **Plano de datos**: Se encarga de reenviar los paquetes a través de la red.

Se puede pensar como una rotonda en una salida de una autopista, donde los paquetes son los autos y la rotonda es el router donde distribuimos a los autos a su destino vía la autopista. Este es el plano de datos. Por otro lado, el plano de control es el ente que coloca los carteles que indican a los autos por donde deben ir.

Estos carteles son las tablas de ruteo, que se encargan de indicar a los routers por donde deben enviar los paquetes. Estas tablas se actualizan con el protocolo de ruteo y no necesariamente tienen un ente centralizado que las controle. Existen protocolos de routing distribuidos que se encargan de actualizar estas tablas.

## Dirección IP

Las direcciones IP teóricamente son únicas e identifican a cada dispositivo en la red. En la práctica, las direcciones IP son asignadas por el ISP y son dinámicas, además hay redes privadas que no son accesibles desde internet por lo que se pueden repetir las direcciones IP.

Se puede dividir en 2 niveles:

- **Nivel de red**: Identifica la red a la que pertenece el dispositivo.
- **Nivel de host**: Identifica el dispositivo dentro de la red.

### Máscara de red

Esta frontera NO es fija, sino que se puede cambiar con las máscaras de red. Estas se identifican con `/n` donde `n` es la cantidad de bits que identifican la red y el resto identifican al host. Por ejemplo, `/24` significa que los primeros 24 bits identifican la red y los últimos 8 bits identifican al host.

El temaño de la máscara determina la clase de la red:

- **Clase A**: `/8` donde el primer bit es `0` y los siguientes 7 bits son la red.
- **Clase B**: `/16` donde los primeros 2 bits son `10` y los siguientes 14 bits son la red.
- **Clase C**: `/24` donde los primeros 3 bits son `110` y los siguientes 21 bits son la red.
- **Clase D**: `/32` donde los primeros 4 bits son `1110` y los siguientes 28 bits son la red.

Donde las clases A-C son unicast y la clase D es multicast.

Reservadas para futuras implementaciones:

- **Clase E**: `/32` donde los primeros 4 bits son `1111` y los siguientes 28 bits son la red.

Las máscaras de red se pueden representar en notación decimal o binaria. Por ejemplo, la máscara `/24` se puede representar como `255.255.255.0` o `11111111.11111111.11111111.00000000`. Donde con un AND entre la dirección IP y la máscara se obtiene la dirección de red. Y con un NOT a la máscara y un AND con la dirección IP se obtiene la dirección del host.

Existen algunas direcciones especiales:

- **Dirección de red**: Todos los bits del host son `0`.
- **Dirección de broadcast**: Todos los bits del host son `1`.

Hoy en día, esta máscara no es fija sino que puede ir variando de 1-31 bits para usos más específicos.

### Subredes

Las subredes son una división de una red en subredes más pequeñas. Por ejemplo, si se tiene una red `/24` se puede dividir en 2 redes `/25` o en 4 redes `/26`.

### Redes locales

Las redes locales son redes privadas que no son accesibles desde internet. Por lo que se pueden repetir las direcciones IP. Para poder acceder a internet se utiliza NAT (Network Address Translation) que traduce las direcciones privadas a una dirección pública.

Direcciones especiales:

- `255.255.255.255`: Broadcast a todas las redes a todos los hosts (no hay que saber la máscara de red)
- `0.0.0.0`: Dirección local. Se usa cuando no tenes una dirección IP asignada.
- `0.0.0.255`: Broadcast local (hay que saber la máscara de red).
- `255.255.255.0`: Broadcast en todas las redes (hay que saber la máscara de red).
- `127.0.0.0`: localhost, no sale del dispositivo se resuelve en el mismo dispositivo.

Para broadcast los routers no lo reenvían, sino que lo descartan excepto en la red local por lo que lo más normal es enviar un broadcast común para la red local ya que no se requiere saber la máscara de red.

Redes especiales:

- `10.0.0.0/8`: Red privada clase A.
- `172.16-32.0.0/16`: Red privada clase B.
- `192.168.0-255.0/24`: Red privada clase C.

## Plano de datos

El plano de datos se encarga de reenviar los paquetes a través de la red. Para esto se utilizan los routers que se encargan de reenviar los paquetes a través de la red. Estos leen la dirección IP de destino y la comparan con la tabla de ruteo para saber por donde enviar el paquete.

El puerto de entrada del router se encarga de leer la dirección IP de destino.

Tenemos 2 tablas para esto:

- **Tabla de ruteo**: Contiene las reglas, los prefijos y las interfaces por donde enviar los paquetes. O(log n)
- **Tabla de forwarding**: Contiene los mapeos de las direcciones IP a las interfaces. O(1)

El routeo lo realiza el procesador central y en primera instancia se intenta el `forwarding` y si no se encuentra se realiza el `routeo`.

Como normalmente se hacen muchas peticiones a la misma dirección IP tiene mucho sentido tener una tabla de forwarding para no tener que hacer el routeo cada vez.

Una técnica medio hardcore sería tener una entrada en la tabla de forwarding por cada dirección IP, pero esto puede no ser muy eficiente.

### Head of Line Blocking

Este es un problema que tenemos cuando muchos paquetes quieren salir por la misma salida, es como cuando tenemos una salida muy común y todos los autos quieren salir por ahí.

Cada router lo resuelve de manera diferente, pero normalmente se hace una cola de paquetes en la salida y se van enviando de a uno.

Estas colas pueden ser FIFO, pueden ser RR o pueden ser por prioridad. La idea es que no haya perdidas ni starvations.

## Datagramas IP

El datagrama IP es el átomo a nivel de red. Es el paquete que se envía a través de la red. Este paquete esta compuesto por:

- **versión**: Versión del protocolo IP (IPv4 o IPv6 normalmente).
- **dirección IP origen**: Dirección IP del host que envía el paquete.
- **dirección IP destino**: Dirección IP del host que recibe el paquete.
- **protocolo**: Protocolo de la capa superior (TCP, UDP, ICMP, incluso IPv6 cuando se encapsula).
- **robustez**: TTL, tiempo de vida del paquete. Incialmente se pensaba para medir tiempo pero era imposible determinar por lo cual se mide en saltos. Cada router que recibe un paquete le resta 1 al TTL y si llega a 0 lo descarta. La red tiene un diámetro aproximado de 30 saltos. Normalmente se setea en 64 para evitar loops infinitos y sobrecargar la red.
- **tamaño del encabezado**: Tamaño del encabezado en palabras de 32 bits.
- **fragmentación**: un offset y un identificador y un par de flags.
- **checksum**: Checksum del paquete para detectar errores.
- **opciones**: Opciones del paquete.
- **datos**: Datos del paquete.

### Fragmentación

Si el paquete es muy grande se puede fragmentar en paquetes más pequeños.

Esto se hace en el origen y se reensambla en el destino. El problema es que si un fragmento se pierde se pierde todo el paquete.

Tiene:

- **offset**: Indica la posición del fragmento en el paquete original.
- **identificador**: Identifica a que paquete pertenece.
- **flags**: Indica si hay más fragmentos o no.
  - **DF**: Don't Fragment, indica que no se puede fragmentar.
  - **MF**: More Fragments, indica que hay más fragmentos.

Esto se hace si se excede el MTU (Maximum Transmission Unit) de la red. Normalmente el MTU es de 1500 bytes.

No es una buena idea hacerlo ya que genera más problemas que soluciones. Por lo que normalmente los sistemas operativos intentan determinar el MTU de la red y fragmentar en el origen.

Si de casualidad se pierde un fragmento, se pierde todo el paquete.

Si el paquete es muy grande y NO se puede fragmentar, se envía un mensaje ICMP de tipo 3 código 4 (Destination Unreachable, Fragmentation Needed and Don't Fragment was Set).

La fragmentación se debe hacer en múltiplos de 8 bytes. Ya que el offset se mide en múltiplos de 8 bytes.

## Plano de control

El plano de control se encarga de tomar decisiones sobre la ruta que deben seguir los paquetes. Para esto se utilizan los protocolos de ruteo.

El plano tiene distintas características:

- **Dinámico**: Se actualiza constantemente.
- **Estático**: No se actualiza. Es útil para redes pequeñas como las domésticas ya que todo lo que se recibe desde internet se envía a la red interna y todo lo que se recibe de la red interna se envía a internet.
- **Distribuido**: No necesita un ente centralizado que controle todo. Sino que los routers se comunican entre ellos para actualizar sus tablas de routing. Para ello deben hablar mediante un protocolo especial (normalmente de capa de aplicación) que corre sobre IP.
- **Centralizado**: Existe un ente centralizado que controla y decide por donde irán los paquetes. Es útil para redes pequeñas ya que a medida que crece la red se vuelve y muy frágil.
- **Dependientes del trafico**: Se actualizan en base al tráfico de la red. Esto significa que no solo reaccionan a la topología de la red, sino que también a la congestión de la misma, con el fin de balancear la carga.

Los routers domésticos suelen ser polifuncionales, ya que no solo hacen routing sino que también hacen NAT, firewall, DHCP, etc.. Normalmente se utilizan protocolos de ruteo estáticos ya que no es necesario un protocolo de ruteo dinámico para redes simples.

Para el mismo flujo de datos (misma protocolo de transporte, IP origen y destino y mismo puerto origen y destino) se suele utilizar el mismo camino. Es decir se evita hacer balanceo de carga para el mismo flujo de datos.

No así para distintos flujos de datos, donde 2 caminos de mismo o similar costo se pueden alternar para balancear la carga de los distintos flujos de datos.

### Topología de red

- AS (Autonomous System): Red autónoma que tiene un único protocolo de ruteo. Se identifican con un número de 16 bits.
- ISP (Internet Service Provider): Proveedores de servicios de internet. Son AS.

Jerarquía de AS:

- **Tier 1**: No pagan a nadie por el tráfico que envían. Se conectan a todos los demás Tier 1.
- **Tier 2**: Pagan a los Tier 1 por el tráfico que envían. Se conectan a los Tier 1 y a otros Tier 2.
- **Tier 3**: Pagan a los Tier 2 por el tráfico que envían. Se conectan a los Tier 2 y a otros Tier 3.
- **Stubs**: Se conectan a los Tier 3 y son aquellos que proveen servicios a los usuarios finales.

Los nodos de la red, se conectan a más de un router para mantener la alta disponibilidad. Por lo que se pueden tener múltiples caminos para llegar a un destino.

A su vez, si el trafico es similar entre 2 nodos de la misma jerarquía, se puede hacer una conexión P2P entre ellos para evitar el costo de pasar por nodos de jerarquía superior.

De la misma manera, existen unos nodos de la red llamados IXP (Internet Exchange Point) que son puntos de intercambio de tráfico entre distintos AS mantenidos entre todos los AS que se conectan a él ahorrando costos para subir a jerarquías superiores.

El hecho de subir en la jerarquía de AS implica un costo y se conoce como "uphill" y el hecho de bajar en la jerarquía también implica un costo para el consumidor final y se conoce como "downhill".

Los CDNs también son parte de la topología de red por el tráfico que manejan y se los suele ubicar en los puntos más altos de la jerarquía de AS.

### Algortimos de ruteo

- **Distance Vector**: Se basa en la distancia y la dirección. Se actualiza cada cierto tiempo y se envía a todos los vecinos. Se utiliza el algoritmo de Bellman-Ford. Este es un algoritmo puramente distribuido ya que no necesita conocer la topología de la red para calcular las rutas más cortas. El problema es que no simpre converge y puede generar loops muy grandes ante cambios o desconexiones en la red.
- **Link State**: Se basa en el estado de los enlaces. Se actualiza cada vez que hay un cambio en la red y se envía a todos los routers. Se utiliza el algoritmo de Dijkstra. Este algoritmo es más eficiente que el de distancia vector ya que converge siempre y no genera loops. El problema es que necesita conocer la topología de la red para calcular las rutas más cortas y esto muchas veces implica un alto costo en envío de mensajes y por ende en la congestión de la red. Este algoritmo si bien es disribuido ya que se ejecuta en cada router, necesita centralizar la información para calcular las rutas más cortas. Además ante un pequño cambio en la red, se deben recalcular las rutas para volver a llegar a un estado óptimo.

### Protocolos de ruteo

- **RIP (Routing Information Protocol)**: Protocolo de ruteo de distancia vector. Se utiliza el algoritmo de Bellman-Ford. Se actualiza cada 30 segundos y se envía a todos los vecinos. Se utiliza el puerto 520. Se utiliza en redes pequeñas ya que no escala tan bien. Cuenta con autenticación.
- **OSPF (Open Shortest Path First)**: Protocolo de ruteo de estado de enlaces. Se utiliza el algoritmo de Dijkstra. Se actualiza cada vez que hay un cambio en la red y se envía a todos los routers. Se utiliza el puerto 89. Se utiliza en redes grandes ya que escala muy bien. Lo que se suele hacer para que el $N$ siendo este el número de routers no sea tán grande a la hora de calcular las rutas es dividir la red en áreas y calcular las rutas por áreas. Esto se llama OSPF jerárquico. Cuenta con autenticación.
