# Rasa Demo bot 
Ejemplo mostrado en la reunion de innovación.

### Entrenamiento Rasa NLU 
```
make bot=restaurante train-nlu
```
### Entrenamiento Rasa Core 
```
make bot=restaurante train-core
```
### Iniciar el servidor para las acciones de rasa
```
make run-actions
```
### Iniciar el servidor de rasa 
```
make bot=restaurante port=5005 run
```
### Interfaz Web
Luego de levantados los dos servidores podemos ir a la carpeta */ui/index.html* y simplemente hacerle doble click.
