# App-de-control-de-inventario-con-python
App de control de inventario con API REST y CRUD usando ORM (curso avanzado de Python)​
**Descripción del programa:** El programa consta de un sistema que almacena en una base de datos cinco parámetros (id, código del producto, tipo de componentes, nombre del usuario y el sector de la empresa al cual pertenecen). Donde el código del producto, es el número de id pasado al código binario.

En consecuencia, el programa almacena estos parámetros a partir de los datos ingresados en la interfaz gráfica de Tkinter y puede realizar 3 rutinas:

Añadir un componente
Modificar un componente
Eliminar un registro
Donde cada función tiene asociado un decorador el cual se encarga de llevar un registro de las operaciones realizadas a través la terminal. En este sentido, la función ‘nuevo’ tiene el decorador que registra la operación realizada y además tiene otro , el cuál se encarga de verificar si el componente asociado a ese usuario ya existe; para así evitar duplicados en la de datos.
