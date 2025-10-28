# 💫 Inventario de Computadoras y Periféricos
## Descripción

Este programa es una aplicación de escritorio desarrollada en Python para gestionar un inventario de computadoras y periféricos. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los ítems del inventario, con validaciones de entrada, búsqueda avanzada y manejo robusto de errores. Está diseñado para entornos empresariales, como departamentos de informática, donde se necesita rastrear equipos asignados a usuarios y sectores específicos.

El programa utiliza una interfaz gráfica intuitiva con Tkinter, una base de datos SQLite para persistencia de datos, y técnicas de programación orientada a objetos (POO) para modularidad y mantenibilidad.

## Funcionalidades Principales

1. Gestión de Inventario (CRUD)

    Nuevo Ítem: Permite agregar un nuevo componente (e.g., CPU, MOUSE) asignado a un usuario y departamento. Incluye validación para evitar duplicados (mismo componente y usuario).
    Eliminar Ítem: Elimina un ítem seleccionado del inventario, actualizando tanto la interfaz como la base de datos.
    Modificar Ítem: Edita los detalles de un ítem existente (componente, usuario, departamento).
    Cada operación se registra en un archivo de log (inventario.log) para auditoría.

2. Validaciones y Seguridad

    Validación de Componentes: Solo acepta tipos predefinidos (CPU, NOTEBOOK, MOUSE, TECLADO, MONITOR, IMPRESORA), convirtiéndolos a mayúsculas.
    Validación de Usuarios: Usa expresiones regulares (regex) para asegurar formato "Nombre Apellido" con mayúsculas iniciales.
    Validación de Departamentos: Selección obligatoria de sectores empresariales (Recursos Humanos, Contabilidad, etc.).
    Prevención de Duplicados: Decorador que verifica si un ítem ya existe antes de insertar.

3. Búsqueda y Filtros

    Campo de búsqueda con filtro por campo (componente, usuario o departamento).
    Búsqueda parcial y case-insensitive usando LIKE en SQL.
    Botón "Mostrar Todos" para resetear la vista completa del inventario.

4. Interfaz de Usuario

    Ventana principal con campos de entrada, botones de acción y una tabla (Treeview) para visualizar datos.
    Mensajes informativos y de error con messagebox.
    Diseño fijo con colores consistentes (fondo azul acero para botones).

5. Persistencia y Manejo de Datos

    Base de datos SQLite con tabla Inventario (campos: id, codigo, componente, usuario, departamento).
    Códigos únicos generados en binario para cada ítem.
    Manejo de errores en operaciones de DB (e.g., conexiones fallidas).

## Conceptos y Tecnologías de Programación Utilizados:

### Lenguaje y Paradigmas

Python: Lenguaje principal, versión 3.x. Se utiliza por su simplicidad, librerías integradas y soporte para POO.
Programación Orientada a Objetos (POO): Clases como Metodos (lógica de negocio y DB) y GUI (interfaz). Encapsula datos y métodos para modularidad.
Decoradores: Funciones como @verificar_duplicados, @registrar_operacion y @registrar_eliminacion para agregar lógica transversal (e.g., logging y validaciones) sin modificar el código principal.

### Librerías y Módulos

Tkinter: Para la interfaz gráfica. Incluye widgets como Button, Entry, Treeview, Combobox y Radiobutton. Maneja eventos con command=lambda.
SQLite3: Base de datos embebida para persistencia. Usa consultas SQL raw con placeholders (?) para evitar inyecciones. Manejo de conexiones y cursores con try-finally para cierre seguro.
Logging: Módulo estándar para registrar operaciones en un archivo (inventario.log). Reemplaza print para auditoría persistente.
Re (Regex): Para validaciones de patrones (e.g., formato de usuario con r'^[A-Z][a-z]+ [A-Z][a-z]+$').

### Técnicas Avanzadas

Manejo de Errores: try-except-finally para capturar excepciones en DB (e.g., sqlite3.Error) y mostrar mensajes al usuario.
Context Managers (Simulados): Aunque SQLite no soporta with nativo para cursores, se usa try-finally para asegurar cierre de recursos.
Validaciones y Sanitización: Entradas se validan antes de procesar para prevenir datos inválidos.
Separación de Concerns: Código dividido en módulos (modelo.py para lógica, vista.py para UI, main.py para ejecución), facilitando mantenimiento y pruebas.
Búsqueda Dinámica: Consultas SQL dinámicas con LIKE para filtros flexibles.

### Arquitectura

MVC (Model-View-Controller): Implícito – Metodos es el Modelo (datos/DB), GUI es la Vista (UI), y los botones actúan como Controlador (conecta acciones).
Persistencia Ligera: SQLite es ideal para prototipos sin servidor, pero escalable a MySQL/PostgreSQL con cambios mínimos.

### Instalación y Requisitos

Requisitos: Python 3.x instalado. No requiere librerías externas (todo es estándar).
Ejecución: Corre python3 main.py (o el archivo principal). La DB se crea automáticamente.

### Uso

Ejecuta el programa.
Ingresa datos en los campos y selecciona un departamento.
Usa "Nuevo" para agregar, selecciona un ítem y usa "Eliminar" o "Modificar".
Busca con el campo de búsqueda y filtra por campo.
Revisa inventario.log para operaciones registradas.

### Proximas mejoras
migrar a SQLAlchemy, agregar autenticación o exportar a CSV.

### Licencia

Este proyecto es de código abierto bajo la licencia MIT.
