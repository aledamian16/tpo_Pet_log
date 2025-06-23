PetLog

Gestor de bitácora de mascotas desarrollado en Python para la materia Programación 1.

🔍 Descripción

PetLog es una aplicación de consola que permite llevar un registro completo de mascotas y sus dueñxs, incluyendo:

Alta, baja y modificación de mascotas y dueñxs

Registro de visitas médicas con historial

Asociación entre mascotas y dueñxs

Control de sesiones de usuario (login / registro)

Persistencia de datos en archivos JSON (mascotas.json, duenios.json) y texto (usuariosRegistrados.txt)

🚀 Características principales

Autenticación: Inicio de sesión y registro de usuarios.

Gestión de dueñxs: Agregar, eliminar, modificar y listar dueñxs.

Gestión de mascotas: Agregar, eliminar, modificar y listar mascotas.

Asociaciones: Vincular mascotas a dueñxs y viceversa.

Historial médico: Registrar visitas médicas con fecha, motivo, diagnóstico, tratamiento y veterinario responsable.

Menús interactivos en consola con validación de entradas.

📂 Estructura de archivos

PetLog/
├── Archivos/
│   ├── Usuarios/
│   │   └── usuariosRegistrados.txt
│   ├── Mascotas/
│   │   └── mascotas.json
│   └── Duenios/
│       └── duenios.json
├── PetLog_G.py            # Código principal
├── README.md             # Documentación del proyecto
└── .gitignore

⚙️ Instalación y uso

Clonar el repositorio

git clone https://github.com/tu-usuario/PetLog.git
cd PetLog

Crear entorno virtual (opcional pero recomendado)

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate    # Windows

Instalar dependencias

Este proyecto solo usa la librería estándar de Python (no hay dependencias externas).

Ejecutar la aplicación

python PetLog_G.py

Primer arranque

Si no existen los archivos en Archivos/, se crearán vacíos.

Crear un usuario para iniciar sesión.

Comenzar a gestionar mascotas y dueñxs.

📋 Funcionalidades detalladas

Menú principal: Navegación por opciones numeradas.

Validaciones: Verificación de IDs, formatos de email, campos no vacíos.

Persistencia: Lectura/escritura atómica de archivos con json.dump y bloques with open(...).

Historial: Cada visita médica es una lista de cadenas con etiquetas y nombre del veterinario.

📝 Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

Haz un fork de este repositorio.

Crea una rama (git checkout -b feature/nombre-de-la-rama).

Realiza tus cambios y haz commit (git commit -m 'Añade nueva funcionalidad').

Envía un push a tu rama (git push origin feature/nombre-de-la-rama).

Abre un Pull Request.

📜 Licencia

Este proyecto es de código abierto bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

