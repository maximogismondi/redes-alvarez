# Capa de Transporte

La red de internet se define como "best effort" Lo que significa que no garantiza la entrega de los paquetes aunque se intenta. La capa de transporte es la encargada de garantizar la entrega de los paquetes.

Lo que hace la capa de transporte es **multiplexar** y **demultiplexar** los paquetes de información. Es decir, se encarga de armar los paquetes de información que se van a enviar y de separar los paquetes de información que se reciben.

Un protocolo es un algoritmo, un conjunto de reglas ordenadas que se deben seguir para realizar una tarea. En la capa de transporte se encuentran dos protocolos: **TCP** y **UDP**.

## Provee

- **Confiabilidad**: Garantiza la entrega de los paquetes.
- **Control de flujo**: Evita que un emisor sature a un receptor.
- **Seguridad**: Encriptación de los datos ??

## Comando para ver las conexiones activas

```bash
netstat -na # Muestra todas las conexiones activas
```

## Sockets

Se identifican con:

- Protocolo
- IP de origen
- Puerto de origen
- IP de destino
- Puerto de destino

Esto nos permite tener múltiples conexiones entre dos dispositivos. Es decir que gestiona el control de flujo.

Los puertos más comunes llamados "well known ports" se exitenden desde el 0 al 1023. Los puertos del 1024 al 49151 son llamados "registered ports" y los puertos del 49152 al 65535 son llamados "dynamic ports". Estos puertos especiales necesitan permisos de administrador para ser utilizados.

## Comunicaciones fiables

Para que una comunicación sea fiable se necesita:

- **Paquetes en orden**: Los paquetes deben llegar en el orden correcto.
- **Sin duplicados**: No se deben recibir paquetes duplicados.
- **Sin pérdidas**: No se deben perder paquetes.
- **Sin errores**: No se deben recibir paquetes con errores.

Podemos agregar más cosas como:

- **Performance**: Que sea rápido.
- **Seguridad**: Que los datos estén encriptados.
- **Control de flujo**: Que no se sature al receptor.
- **Fairness**: Que todos los usuarios tengan la misma prioridad.
- **Control de congestión**: Que no se sature la red.

Estas son distintas cosas (menos prioritarías) que se pueden agregar a una comunicación fiable.

TCP es un protocolo que cumple con todas las características principales de una comunicación fiable, e intenta cumplir con las características secundarias.

## Protocolos

### TSL

Un protocolo que está entre la capa de aplicación y la capa de transporte. Se encarga de la encriptación de los datos y corre sobre TCP.

### UDP

Este protocolo no está conectado, es decir que no garantiza la entrega de los paquetes. Es un protocolo muy rápido y se utiliza para enviar paquetes pequeños. Se utiliza para enviar paquetes de voz, video, etc. donde existe una tolerancia a la pérdida de paquetes.

Para ello introduce muy poco overhead. Tan solo 8 bytes:

- 2 bytes para el puerto de origen
- 2 bytes para el puerto de destino
- 2 bytes para la longitud del paquete
- 2 bytes para el checksum

Cuando la rta ocupa más de 512 bytes se manda si o si por TCP para que no se pierda ya que sería muy costoso volver a enviarlo en caso de pérdida y es preferible que se envíe por TCP sacrificando la velocidad y un poco de tiempo al establecer la conexión pero garantizando la entrega.

### TCP

Es un protocolo muy complejo que se encarga de garantizar la entrega de los paquetes. Se encarga de la confiabilidad, control de flujo y seguridad.

### Estableciento una conexión

Para enviar los paquetes debe establecer una conexión. Para ello se utiliza el "three way handshake":

1. El cliente envía un paquete con el flag SYN = 1, el Rs, el MSS y el RWIN
2. El servidor responde con un paquete con el flag SYN = 1, ACK = 1, el Rs, el Nr, el MSS y el RWIN
3. El cliente responde con un paquete con el flag ACK = 1, el Rs, Nr el MSS y el RWIN nuevamente

Mientras se establece la conexión, se debe establecer el tamaño máximo de los segmentos (MSS) que se pueden enviar. El MSS es el tamaño máximo de los datos que se pueden enviar en un segmento. Tanto el cliente como el servidor deben acordar el MSS. Entre otros datos que se deben acordar están el tamaño de la ventana de recepción (RWIN) y el número de secuencia.

Puede pasar que 2 servidores traten de establecer una conexión al mismo tiempo entre si mismo. En este caso no es necesaria que se haga un "three way handshake" ya que ambos servidores están esperando una conexión. En este caso se puede hacer un "two way handshake". Puede pasar en servidores que están en la nube y que se conectan entre si o muy tipicamente en un servidor de correo SMTP.

### Comunicación

Cada enpoint tiene un numero de secuencia que indica el numero de bytes que se han enviado. Cuando se envían los segmentos, se los envía con el número de secuencia enviado y el número de secuencia que se espera recibir, es decir el siguiente byte al último byte que se recibió.

### Cabeza del paquete TCP

Estos se define en la cabecera del paquete TCP:

- **Puerto de origen**: 2 bytes
- **Puerto de destino**: 2 bytes
- **Número de secuencia**: 4 bytes
- **Número de ACK / Recepción**: 4 bytes
- **Offset**: 4 bits, indica el tamaño de la cabecera
- **Reservado**: 6 bits, reservados para futuras implementaciones
- **Flags**: 6 bits
  - **URG**: 1 bit, indica que el campo de urgencia es válido
  - **ACK**: 1 bit, indica que el campo de ACK es válido
  - **PSH**: 1 bit, indica que el receptor debe pasar los datos a la capa de aplicación
  - **RST**: 1 bit, indica que la conexión se debe reiniciar
  - **SYN**: 1 bit, indica que se está iniciando una conexión
  - **FIN**: 1 bit, indica que se está cerrando la conexión
- **Ventana**: 2 bytes, indica el tamaño de la ventana de recepción
- **Checksum**: 2 bytes, para verificar la integridad del paquete
- **Urgent Pointer**: 2 bytes, indica el offset del campo de urgencia
- **Opciones**: Variable, se pueden agregar opciones al paquete, como el MSS y el RWIN cuando se establece la conexión

### Cantidad de bytes inflight

CHEQUEAR: AL mismo tiempo TCP solo puede tener "inflight" un número limitado de paquetes, el límite teórico es de 2GB, pero en la práctica es mucho menor. Este limite teórico se debe a que el número de secuencia es de 4 bytes, por lo que el número de secuencia máximo es de 2^32 = 4GB.

### Pérdida de paquetes

Normalmente los paquetes que se pierden son los paquetes y no los de datos ya que son menos propensos a corromperse y a ser descartados por un router con poco espacio en la cola.

Si se pierde uno de los paquetes de datos, el receptor no puede seguir recibiendo los paquetes siguientes ya que debe garantizar que los paquetes lleguen en orden. En ese momento el receptor al recibir un paquete que no es el que espera, envía un paquete de ACK con el número de secuencia del último paquete que recibió correctamente.

El emisor al recibir un paquete duplicado, puede reenviar el paquete que se perdió. Pero esto puede generar muchos falsos negativos, ya que puede ser que el paquete perdido haya llegado más tarde. Por eso, el emisor debe esperar un tiempo antes de reenviar el paquete. Este tiempo se llama "retransmisión timeout" y lo calcularemos más adelante. Por otro lado, el receptor usar la técnica de "Fast retransmission" para detectar si un paquete se perdió. Si el receptor recibe 3 paquetes de ACK duplicados, puede asumir que el paquete se perdió con un alto grado de confianza y reenviar el paquete.

### Retransmisión timeout

El tiempo de retransmisión debe ser más grande que el tiempo de ida y vuelta (RTT) de la conexión.

La fórmula para calcular el tiempo de retransmisión es:

```text
T(i) = (1 - α) * T(i-1) + α * RTT
D(i) = (1 - β) * D(i-1) + β * |RTT - T(i)|

Donde:
- T(i) es el tiempo de retransmisión del paquete i
- D(i) es la desviación del tiempo de retransmisión del paquete i
- RTT es el tiempo de ida y vuelta
- α y β son constantes, normalmente α = 0.125 y β = 0.25
```

Por último el tiempo de retransmisión se calcula como:

```text
Timeout = T(i) + 4 * D(i)
```

La distribución del tiempo no tiene un modelo poissoniano, sino que es más aplanada.

### Tamaño de la ventana

La ventana es la cantidad de bytes que puede haber en vuelo. Lo ideal que el tamaño de la ventana

El tamaño de la ventana de envío se calcula a partir del RTT, el throughput, el MSS y el tamaño de la ventana de recepción (RWND).

```text
w = min(cwnd, rwnd)

Donde:
- cwnd es el tamaño de la ventana de congestión
- rwnd es el tamaño de la ventana de recepción
- w es el tamaño de la ventana de envío
```

El tamaño de la ventana de congestión si bien depende de la capa de red, se puede inferir a partir del throughput, los paquetes perdidos y el RTT en la capa de transporte con TCP.

Se inicializa de la siguiente manera:

```text
cwin(0) = 1 MSS
sstresh = 65535 bytes (numero mágico)

Donde:
- cwin es el tamaño de la ventana de congestión
- sstresh es el umbral de la ventana de congestión
- MSS es el tamaño máximo de los segmentos
```

```text
Si:

- cwin < sstresh => slow start
  cwin >= sstresh => congestion avoidance
```

En slow start, se inicia lento pero se crece muy rápidamente, de manera exponencial. Por cada segmento que se recibe correctamente, se incrementa la ventana en 1 MSS.

Si perdemos paquetes dependeiendo del algoritmo que usemos, se reduce el cwin y el sshtresh:

- TCP Reno:

```text
cwin(i) = cwin(i-1) / 2
sstresh = cwin(i) / 2
```

- TCP Tahoe:

```text
cwin(i) = 1 MSS
sstresh = cwin(i) / 2
```

- TCP Cubic:

Tiene una curva distinta, a priori funciona como TCP Reno pero cuando se pierde un paquete, tiene un creciemiento más logaritmico hasta el máximo anterior y luego de superar este máximo, vuelve a crecer de manera exponencial.

En congestion avoidance, se incrementa de manera lineal. Por cada segmento que se recibe correctamente, se incrementa la ventana en 1 MSS / cwin.

```text
cwin(i) = cwin(i-1) + MSS / cwin
```

Ahora debemos tener en cuenta que el tamaño de la ventana, el cwin

No lo dice en los libros, pero el sshtresh puede bajar hasta 2 MSS. Y aunque tenga un slow start por 1 paquete, el crecimiento será lineal porque automaticamente pasa a congestion avoidance.

### Cierre de la conexión

Para cerrar la conexión se utiliza el "four way handshake":

1. El cliente envía un paquete con el flag FIN = 1
2. El servidor responde con un paquete con el flag ACK = 1
3. El servidor envía un paquete con el flag FIN = 1
4. El cliente responde con un paquete con el flag ACK = 1

Con estos 4 paquetes, se puede cerrar la conexión. De todas formas el servidor puede seguir enviando paquetes hasta que el cliente envíe un paquete con el flag FIN = 1.
