# Trabajo práctico teórico - Onix

Onix: A Distributed Control Platform for Large-scale Production Networks

[Link al paper](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Koponen.pdf)

## Introducción

En resumen, ONIX es una capa que facilita la escalabilidad, la integridad de la información que corre por encima de todos los elementos de red, probablemente en un cluster de servidores. Estos se comunican con los dispositivos de red (switches, routers, etc) para poder administrarlos de manera centralizada.

Onix es un SDN como otros vistos, pero es el primero en enfocarse en la implementarción y en la generalidad en su máxima expresión.

## Objetivos

La idea de ONIX es solventar los siguientes problemas:

- Generalidad: ONIX es general y puede manejar cualquier tipo de red. No está atado a un tipo de red en particular.
- Simplificar: La API de ONIX es simple y permite a los desarrolladores escribir aplicaciones de red sin tener que preocuparse por la complejidad de la red subyacente.
- Escalabilidad: ONIX es escalable y puede manejar una gran cantidad de dispositivos de red. No tiene dificultades de escalabilidad más allá de las propias de tener una gran cantidad de dispositivos.
- Robustez: ONIX es robusto y tolerante a fallas. Debe poder manejar las fallas de los dispositivos de red y de los servidores que corren ONIX de manera `graceful`. Para esto los servidores de ONIX se encuentran replicados y no existe un único punto de falla, aunque sabemos que esto no es gratis y requiere de una sincronización de estado entre los servidores.
- Performance: Si bien el objetivo de ONIX NO es que los paquetes de datos se procesen más rápido, porque eso sería el plano de datos, sí se centra en mantener la velocidad del plano de control para poder implementar cambios de manera veloz y responder a las necesidades de la red en un tiempo razonable. Sin embargo a diferencia de los sistemas tradicionales, ONIX se centra en la generalidad y hay un trade-off entre velocidad y generalidad.

## Contexto de implementación

El contexto en el que si implementa Onix es el siguiente:

- Infraestructura física: Se tiene una serie de elementos de red (switches, routers, balanceadores, etc) que se cominican entre sí y tienen una interfaz que le permite hablar con los servidores de ONIX. Estos son los encargados finales de routear los paquetes de datos y de ejecutar las políticas de la red.
- Infraestructura de conectividad: La infraestructura que conecta a la infraestructura física con los servidores de ONIX. Puede ser `in-band` (embebida en la propia red) o `out-of-band` (una red dedicada para la comunicación con los servidores de ONIX). Debe soportar una comunicacción bidireccional. Se pueden usar protocolos convencionales de control para esto como OSPF.
- Onix: Es un sistema distribuido que se implementa en uno o varios servidores. Mantienen un estado global de la red y proveen una API para que permite a las aplicaciones de red interactuar con la misma y modificar su estado (tablas de ruteo por ejemplo) de manera centralizada. Estas instancias de ONIX son las encargadas de mantener la consistencia del estado de la red y de comunicarse con los elementos de red para que estos apliquen los cambios necesarios. También deben comunicarse de forma bidireccional para notificar cambios en la red y recibir las nuevas políticas a aplicar.
- Logica de control: Son las aplicaciones que corren sobre ONIX y que interactúan con la API de ONIX para modificar el estado de la red. Estas aplicaciones pueden ser de cualquier tipo, desde aplicaciones de monitoreo, hasta aplicaciones de balanceo de carga, firewalls, etc. En definitiva cualqueir aplicación que se pueda construir en base a las primitives que provee ONIX.

## NIBs

La información en ONIX se almacena como una base de datos de clave-valor donde cada unidad de información se conoce como Network Information Base (NIB). Estas NIBs se organizan en forma de grafos para modelar la topology de la red. Estos NIBs son el corazón de ONIX y son la información que se debe mantener consistente en todos los servidores de ONIX.

Estos NIBS como dijimos son clave valor y pueden modelar, nodos de la red, puertos, enlaces, rutas, politicas, flujos, etc. Cada uno de estos elementos tiene un identificador único. Un nodo puede tener varios puertos y un link conecta dos puertos. Un link puede tener varios flujos y un flujo puede tener varias rutas, etc.

## API

Las funcionalidades básicas de la API de Onix son las siguientes:

- `Query`: Entontrar entidades
- `Create/Destrory`: Crear o remover entidades de la red
- `Access attributes`: Leer y/o modificar atributos de las entidades
- `Notifications`: Recibir notificaciones de cambios en la red
- `Synchronize`: Espera a que las actualizaciones se exporten a la red o a los controladores
- `Configuration`: Configurar la importación y exportación de los NIBs con la red (ejemplo la frecuencia de actualización)
- `Pull`: Forzar la actualización (a demanda) de las importaciones (de nuevos cambios en la red) de modo que se peudan actualizar los NIBs y aplicar las politicas correspondinetes.

## Scalability

Para lograr la escalabilidad onix implementa una serie de técnicas que permiten distibuir el trabajo entre varios nodos sin necesitar de un nodo central ni de replicación en muchos casos. También trata de simplificar ciertas cuestiones para que la escalabilidad no sea complicada. Como por ejemplo en un cluster de nodos de ONIX, si bien cada nodo trabaja por separado, estos podrán ser representados como un único nodo para el resto de la red y para otros cluster de nodos. De modo que agregar un nuevo nodo a un cluster sea totalmente transparente para el resto de la red.

Más en detalle:

    - Particionamiento: No necesariamente todos los NIBs se encuentran en todos los nodos de ONIX. Se pude establecer un particionamiento de la red con algún criterio (ejemplo por región geográfica) y que cada nodo de ONIX se encargue de un subconjunto de la red por lo que tan solo será necesario replicar los NIBs que se encuentran en la frontera de las particiones. Además no deberá registrar todos los eventos de la red, sino solo los que afectan a los NIBs que maneja.

- Agregación: Onix permite la agregación de un subconjunto de los dispositivos de red en un único nodo de ONIX. De modo que se puede simplificar la red y no tener que manejar cada dispositivo por separado.
- Consistencia y durabilidad: ONIX implementa una serie de algoritmos distribuidos de replicación, lockeo, consistencia, etc. Que permitan mantener la consistencia de los NIBs en todos los nodos de ONIX. Sin embargo ONIX ofrece 2 alternativas de BDD, una basada en transacciones enfocada en la consistencia y durabilidad y otra para entrornos más volatiles que se enfoca más en la disponibilidad y no ofrece ciertas garantías de consistencia (DHT, Distributed Hash Table).

### Etapas de escalabilidad

Si pensamos en una implementación práctica. Podemos diferenciar 4 etapas de escalabilidad:

- Particionamiento: Divide la red entre varias instancias de ONIX. Cada instancia maneja un subconjunto de la red de modo sea más fácil de manejar y consuma menos recursos.
- Agregación: Se puede agrupar varios dispositivos de red en un único nodo lógico de ONIX de modo que no solo simplifique la red para una instancia de ONIX terceiara, sino que también permite comportartir tan solo un resumen de las estadisticas (trafico por ejemplo) y guardarse los detalles en la propia instancia de ONIX.
- Further partitioning: Se puede particionar la red de modo que se particione la base de datos de ONIX. Esto permite una escalabilidad mayor y fuerza que para hacer consultas a otras instancias se tenga que usar la base de datos compartida para hacer requests y responses a las mismas.
- Inter-domain aggregation: Se puede agrupar una AS en un nodo lógico de red de modo que guardemos la privacidad de la red exponiendo solo los datos que sean estrictamente necesarios para otras AS.

## Reliability

Hay 4 tipos de fallas las cuales ONIX debe ser tolerante:

### Network elements and link failures

Fallas en dispositivos de forwarding y en los enlaces de la red.

Esto ya lo pueden tratar los planos de control tradicionales. Se debe difundir la falla y recalcular las tablas de routeo y esto define un tiempo mínimo de reacción para redigir el tráfico. Es por esto y por los requisitos de tiempo cada vez más estrictos que se agiliza el proceso con caminos de backup precalculados.

### ONIX failures

Si una instancia de ONIX falla, tenemos bien dos opciones, que sea detectada y relevada por otra en su totalidad o que muchas instancias de ONIX se encargen de manejar los elementos de red de forma simultanea. La primera tiene el problema que puede sobrecargar la instancia que releva a aquella que falló y la segunda tiene el problema de que se deben sincronizar los estados de las instancias de ONIX. Es por esto que ONIX provee en su API un mecanismo que permite a las aplicaciones tomar deciones sobre las colisiones de estados. Una solución simple podría ser que las distintas instancias de ONIX implementen los mismos algoritmos de control y siempre y cuando sean deterministcos, deberían converger a un mismo estado aunque puede transitoriamente estar en un estado inconsistente.

### Conectiviy infraestructure failures

El último caso de falla es entre los elementos de la red y los servidores de ONIX o entre los sevidores de ONIX en sí.

Acá tenemos 2 situaciones a analizar:

- Si hay una red separada para la administración: Entonces el problema es menor ya que la red de administración será la que falle y la red de datos seguirá funcionando con el último estado conocido o en última instancia usando protocolos de control tradicionales hasta que se recupere la red de administración como OSPF.
- Si la red de administración es la misma que la de datos: Entonces en este caso asumiremos que no se cayo toda la red sino aquellos enlaces que conectan a los servidores de ONIX con los elementos de red. En este caso y como ONIX conoce normalmente la topología de red de antemano, el mismo podrá actualizar las rutas de enrutamiento de modo que usen caminos alternativos para llegar a los elementos de red. O una solución más eficaz sería tener configurado de antemano estos múltiples paths y que tras caerse un enlace, los elementos de red automáticamente cambien a otro path maximizando la disponibilidad de la red.

## NIB distribution

Para distribuir los NIBs entre los distintos nodos de ONIX y los elementos de red se deben tener en cuenta 2 factores para elegir la metodología más adecuada:

- La frecuencia de actualización de los NIBs y la durabilidad de los datos. No es lo mismo una politica de red que se establece una vez y dura meses que a un dato como el trafico de la red que cambia constantemente y en poco tiempo se vuelve obsoleto.
- La consistencia de datos requerida. Como en la caso anterior, frente a una politica que entre en conflicto ya que no es consistente, normalemente necesitaremos a un humano que tome la decisión final de cual aplicar. Ahora si hablamos de cosas más simples como el trafico de la red o el estado de un link, podemos permitirnos una inconsistencia temporal y consitencia eventual ya que o bien ONIX o las aplicaciones, consultarán nuevamente por el estado y se podrá sobre-escribir el estado inconsistente.

Es por esto que ONIX no decide automáticamente de que forma se almacenarán y replicarán los NIBs, sinó que deja que las aplicaciones tomen esta decisión. Provee 2 tipos de bases de datos:

- Una base de datos transaccional SQL: Que ofrece y garantiza la consistencia y durabilidad del dato. Sin embargo esto tiene un costo en términos de performance y esto empeora exponencialmente a medida que se agregan más nodos a la red.
- Una base de datos DHT: Que ofrece una altisima disponibilidad y performance, pero no garantiza la consintencia de los datos sino que ofrece una consistencia eventual, en la que eventualmente se llegará a un estado consistente. Esto es ideal para datos que cambian constantemente y no necesitan ser consistentes en todo momento. Sin embargo frente a inconsistencias, las aplicaciones serán las responsables de resolverlas y ONIX provera ciertas herramientas para que esto sea más sencillo.

Si bien las opciones son diametralmente opuestas, ONIX ofrece una solución mixta en la que ambos tipos de bases de datos pueden coexistir y ser usadas por las aplicaciones de la red, donde cada una tenga un propósito distinto.

Para hacer estos cambios debemos tener en cuenta que los procolos north bound y south bound son distintos y son completamente transparentes el uno para el otro. Por ejemplo ONIX puede comunicarse con los elemenos de red vía OpenFlow o con Open vSwitch para hacer cambios en las tablas de ruteo y en las configuraciones de los switches. Sin embargo con las aplicaciones de red puede usar un protocolo totalmente distinto como REST o gRPC. Esto permite por ejemplo que una aplicación haga un cambio en la NIB de ONIX, por ejemplo un cambio de ruta para un router en particular y ONIX refleje este cambio actualizando las NIBs de maneara distribuido y enviando un comando OpenFlow al router corresponiente notificando el cambio propuesto por la aplicación.

La importación y exportación de los NIBs se realiza mediante unos módulos de sincronización los cuales pueden ser configurados por las aplicaciones al igual que las entidades de los NIBS, las cuales pueden ser extendidas para el propósito de la aplicación. Tanto los módulos como las entidades pueden ser configuradas para resolver conflictos. Por ejemplo si se produce un conflicto en una estadística de tráfico, se puede configurar para tomar la más reciente o un promedio de ambas.

Por otro lafo para coordinar estos cambios y las distintas entidades existen soluciones como Zookeeper que permiten sincronizar los cambios en los distintos nodos de ONIX como por ejemplo establecimiento de lideres o de algoritmos de consenso.

## Implementation

ONIX se implementa originalmente en C++, y puede correr en múltiples procesadores incluso usando distintos lenguajes de programación en cada uno de ellos (actualmente se encuentran disponibles Python, C++ y Java). No necesita usar TCP/IP para la comunicación sinó que puede usar IPC (Inter Process Communication) para la comunicación entre los distintos nodos de ONIX formando una instancia de ONIX.

## Aplications

Veremos una serie de aplicaciones que se pueden construir sobre ONIX:

### Ethane

Enfuerza políticas de seguridad en una red administrada. El objetivo es reconocer los flujos de la red, validar si cumplen las políticas y en caso de cumplirlas aprobar los flujos y establecer las reglas de ruteo necesarias. Onix permite distribuir el procesamiento de estos flujos de manera que varias instancias de ONIX resuelvan cada uno de los flujos y se distribuyan la carga de trabajo en función de la topología de la red. En esta caso usaremos una base de datos DHT para almacenar los flujos de la red ya que estos cambian constantemente y no necesitan ser consistentes en todo momento.

### DVS (Distributed Virtual Switch)

La idea es dado redes virtuales, compuestas de decenas de VMs que viven en un mismo servidor, crear una serie de switch virtuales que permitan una comunicación entre las VMs de una misma red virtual. Si bien pueden las VMs pueden ser agregadas y removidas, este proceso no será algo que ocurra constantemente y por lo tanto se puede usar una base de datos SQL para almacenar las politicas a aplicar en la red. Además podemos particionar la red según las pools de VMs de un mismo servidor y dedicar una instancia específica de ONIX para cada una de ellas. En caso de fallas, la red puede levantar otra instancia de ONIX como si de levantar una VM se tratase y mientras tanto manter la red funcionando con el último estado conocido.

### Multi-tenant Virtualized Data Centers

En un data center podemos tener varias redes virtuales alojadas de distintos tenants que queremos que esten isolados el uno del otro. Como varios tenants pueden tener direcciones IP o MAC iguales, se debe agregar una capa de encapsulamiento que aisle las redes de los distintos tenants. Las VMs de los tenants se pueden comunicar entre sí y para ello se deben crear tuneles que permitan la comunicación esto crece de forma cuadrática con la cantidad de VMs por tenant ya que una VM se puede conectar a todas las demás del mismo tenant. Es por ello que para manejar esta complejidad se puede usar una base de datos DHT para almacenar las políticas de ruteo y de encapsulamiento de la red. Además se puede distribuir el trabajo usando múltiples intancias de ONIX donde cada hypervisor tenga su propia instancia de ONIX y se encargue de las VMs de su tenant. Esto permitiría abstraer cada uno de los hypervisores como un solo nodo lógico y bajar significativamente la cantidad de tuneles necesarios.

## Evaluation

TODO

## Trabajos relacionados

ONIX no es la primer plataforma de control distribuido, pero si es la primera en enfocarse en la generalidad y en atacar muy fuertemente problemas de escalabilidad y de reliability.

Existen desarollos totalmente opuestos a ONIX que en vez de enfocarse en una generalidad en el plano de control, buscan hacerlo en el forwarding mucho más cercano al plano de datos. Si bien son totalmente ortogonales, los desarollos de ONIX piensan que pueden ser complementarios y que se pueden usar en conjunto.

## Conclusiones

ONIX es una implementación real de una plataforma de control. Busca aplicar el paradigma de SDN y permite que las aplicaciones hagan la mayoría del trabajo, enfocandose en proveer una API transparente y general y simplificar problemas de escalabilidad y consistencia pero NO haciendolos desaparecer. Es por esto que el target principal de ONIX son las grandes redes de producción como los datacenter y las redes de proveedores de servicios que tienen una gran complejidad de redes y proveer una solución de control que escale horizontalmente y que sea tolerante a fallas puede simplificar mucho el trabajo permitiendo que esta escalabilidad no se detenga por problemas que no son inherentes a la red en sí.
