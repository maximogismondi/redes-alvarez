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

## Protocolos

### TSL

Un protocolo que está entre la capa de aplicación y la capa de transporte. Se encarga de la encriptación de los datos.

### UDP

### TCP

Cuando la rta ocupa más de 512 bytes se manda si o si por TCP para que no se pierda
