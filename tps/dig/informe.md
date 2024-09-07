# Trabajo práctico dig

- Fecha de entrega: 7 de septiembre de 2024
- Materia: Redes (TA048)
- Curso: 02 Alvalrez Hamelin
- Nombre completo: Máximo Gismondi
- Padrón: 110119

## Introducción

En este trabajo práctico, nos vamos a centrar en la utilidad `dig` (Domain Information Groper). Esta utilidad permite realizar consultas a servidores DNS, proporcionando a los administradores de redes la capacidad de depurar la resolución de nombres de dominio y analizar el funcionamiento del protocolo DNS en situaciones específicas.

En esta ocasión, utilizaremos `dig` para consultar el servidor DNS asociado a `developer.mozilla.org`, un sitio que ofrece guías, referencias y herramientas principalmente para desarrolladores web. Analizaremos la traza de consultas, los servidores que responden, y otros detalles no solo a través de la línea de comandos, sino también con Wireshark, una aplicación que permite capturar y analizar cualquier tipo de paquete de red. de red. -->

## Comando

Antes de empezar a enviar consultas a través de `dig`, vamos a entender como funciona el comando y la estructura del mismo. `dig` tiene la siguiente estructura:

```bash
dig [@server] [name] [type] [+opciones]
```

Donde:

- `@server`: Especifica el servidor DNS al que se le enviará la consulta. Si no se especifica, se utilizará el servidor DNS configurado en el sistema.
- `name`: Es el nombre de dominio que se desea consultar.
- `type`: Especifica el tipo de registro que se desea consultar. Si no se especifica, se asume que es un registro de tipo `A`.
- `+opciones`: Son opciones adicionales que se pueden utilizar para modificar el comportamiento de la consulta.

### Opciones

Para hacer una consulta iterativa, autorizada y verborrágica debemos utilizar las siguientes opciones:

- `+trace`: Realiza una consulta iterativa, mostrando la traza de consultas desde el servidor raíz hasta el servidor autoritativo.
- `+stats`: Muestra estadísticas de la consulta realizada.
- `+multiline`: Muestra la respuesta en formato de múltiples líneas.

No es necesario utilizar otras opciónes ya que al usar `+trace` siempre se realiza una consulta iterativa y autorizada. Y la información adicional que se puede obtener con `+stats` y `+multiline` es suficiente para analizar la consulta ya que el modo verborrágico está ac

### Servidor DNS

El servidor DNS que vamos a utilizar para realizar la consulta es `8.8.8.8`, el servidor DNS público de Google, que es muy utilizado por su velocidad y disponibilidad.

### Comando completo

Una vez que entendemos la estructura y las opciones que vamos a utilizar, el comando completo para realizar la consulta es el siguiente:

```bash
dig @8.8.8.8 developer.mozilla.org +trace +stats +multiline
```

## Captura

## Análisis

## Conclusión

## Bibliografía

- [IBM dig command](https://www.ibm.com/docs/pl/aix/7.1?topic=d-dig-command)
