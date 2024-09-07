# Preguntas parcial

## ¿Cual es la diferencia entre control de flujo y de congestión?

- Congenstion: está relacionado con el tamaño de la ventana de
- Flujo: está relacionado con el tamaño del buffer del emisor

## ¿Que se le informa al emisor cuando puede enviar más paquetes?

A través del header de los paquetes que le envía el receptor al emisor.

## ¿De que manera sabe el sender que el receiver recibió el paquete?

Con los ACKs

## Como manjamos el control de congestión en TCP?

- Hay un flag que te informa si hay reducción de la ventana de congestión
- Mucho mejor analizarlo vía timeouts

## De que depende la ventana de congestión?

Depende de ambos del sender y del receiver. Tomamos el mínimo de ambos.

## Como diferenciamos una perdida de paquete de una congestión?

No se puede diferenciar. Una congestión puede desembocar en una perdida de paquete.

## Me afectan los otros clientes TCP en la transferencia de mis paquetes?

En el flujo no, ya que la ventana se establece entre el sender y el receiver.

En la congestión si, ya que la ventana de congestión se establece entre el sender y el receiver.

## Como defenderte de UDP

- Podemos hacer un limite de conexiones UDP simultaneas
- Son peligrosas las conexiones UDP ya que no tienen control de flujo ni de congestión por defecto
