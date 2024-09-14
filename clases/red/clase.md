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
