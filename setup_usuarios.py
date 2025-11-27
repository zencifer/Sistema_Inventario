import sqlite3
import hashlib
from datetime import datetime

#
#
#
#   EJECUTAR SCRIPT SI ES PRIMERA VEZ QUE SE CORRE EL PROGRAMA
#       Abrir terminal. "python setup_usuarios.py"
#
#

# Conectar a la base de datos
conn = sqlite3.connect('instance/InventarioBD.db')
cursor = conn.cursor()

# Crear la tabla usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    fecha_hora_ultimo_inicio TEXT,
    rol TEXT NOT NULL CHECK(rol IN ('ADMIN', 'PRODUCTOS', 'ALMACENES'))
)
''')

# Función para encriptar contraseñas con MD5
def encriptar_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Insertar los usuarios base
usuarios_base = [
    ('ADMIN', 'admin23', 'ADMIN'),
    ('PRODUCTOS', 'productos19', 'PRODUCTOS'),
    ('ALMACENES', 'almacenes11', 'ALMACENES')
]

for nombre, password, rol in usuarios_base:
    password_encriptada = encriptar_password(password)
    try:
        cursor.execute('''
            INSERT INTO usuarios (nombre, password, fecha_hora_ultimo_inicio, rol)
            VALUES (?, ?, NULL, ?)
        ''', (nombre, password_encriptada, rol))
        print(f"Usuario '{nombre}' creado exitosamente")
    except sqlite3.IntegrityError:
        print(f"Usuario '{nombre}' ya existe en la base de datos")

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("\n¡Tabla 'usuarios' creada e inicializada correctamente!")
print("\nContraseñas encriptadas con MD5:")
for nombre, password, rol in usuarios_base:
    print(f"  {nombre}: {encriptar_password(password)}")