# SupportVectorMachine

Modulo SVM en Python para clasificar documentos web.
Clasificacion en Relevantes y No relevantes

Se lee archivo csv con el siguiente formato para entrenar:
| Query        | Url           | Clase  |
| ------------- |:-------------:| -----:|
| Turismo Misiones | http://www.argentinaviajera.com.ar/misiones.html | 1 |
| Turismo Misiones | http://www.turismoushuaia.com/ |   0 |
| Turismo Misiones | http://www.ushuaia.gob.ar/turismo |    0 |

Clase = 0 (No relevante) | 1 (Relevante)
## Dependencias
------
[Pony ORM](https://ponyorm.com/)<br>
[Pattern CliPS](http://www.clips.ua.ac.be/pattern)<br>
