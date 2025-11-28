from flask import Flask, request, session, render_template, redirect, url_for, flash
import sqlite3
import hashlib
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_muy_segura_2024'  # Cambia esto por una clave segura en producción


# Decorador para proteger rutas que requieren autenticación A
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash('Debe iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Función para obtener conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('instance/InventarioBD.db')
    conn.row_factory = sqlite3.Row
    return conn

# Función de verificación de usuario
def verificar_usuario(nombre, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Encriptar la contraseña con MD5 (igual que en tu DB)
        password_encriptada = hashlib.md5(password.encode()).hexdigest()

        # Buscar usuario en la base de datos
        cursor.execute('''
            SELECT * FROM usuarios 
            WHERE nombre = ? AND password = ?
        ''', (nombre, password_encriptada))

        usuario = cursor.fetchone()

        if usuario:
            # Actualizar fecha y hora del último inicio de sesión
            cursor.execute('''
                UPDATE usuarios 
                SET fecha_hora_ultimo_inicio = ? 
                WHERE nombre = ?
            ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nombre))
            conn.commit()

        conn.close()
        return usuario
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return None

# Ruta principal - redirige según estado de sesión
@app.route('/')
def index():
    session.clear()
    if 'usuario' in session:
        return redirect(url_for('inicio'))
    return redirect(url_for('login'))

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya hay sesión activa, redirigir a inicio
    if 'usuario' in session:
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        password = request.form.get('password', '')

        # Validar que los campos no estén vacíos
        if not nombre or not password:
            flash('Por favor, complete todos los campos', 'error')
            return render_template('login.html')

        # Verificar credenciales
        usuario = verificar_usuario(nombre, password)

        if usuario:
            # Guardar información en la sesión
            session['usuario'] = usuario['nombre']
            session['usuario_id'] = usuario['id']
            session['rol'] = usuario['rol']
            session['nombre_completo'] = usuario['nombre']

            flash(f'¡Bienvenido {usuario["nombre"]}!', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            return render_template('login.html')

    return render_template('login.html')

# Ruta de inicio (protegida)
@app.route('/inicio')
@login_requerido
def inicio():
    return render_template('inicio.html',
                           usuario=session.get('usuario'),
                           rol=session.get('rol'),
                           nombre_completo=session.get('nombre_completo'))

# Ruta de productos (protegida)
@app.route('/productos')
@login_requerido
def productos():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()

    conn.close()

    return render_template('productos.html',
                           productos=productos,
                           usuario=session.get('usuario'),
                           rol=session.get('rol'))

# Ruta de almacenes (protegida)
@app.route('/almacenes')
@login_requerido
def almacenes():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM almacenes')
    almacenes = cursor.fetchall()

    conn.close()

    return render_template('almacenes.html',
                           almacenes=almacenes,
                           usuario=session.get('usuario'),
                           rol=session.get('rol'))


# Ruta de logout
@app.route('/logout')
def logout():
    usuario = session.get('usuario', 'Usuario')
    session.clear()
    flash(f'Sesión cerrada correctamente. ¡Hasta pronto {usuario}!', 'info')
    return redirect(url_for('login'))

# Manejo de errores 404
@app.errorhandler(404)
def page_not_found(e):
    return f"<h1>404 - Página no encontrada</h1><a href='{url_for('login')}'>Volver al inicio</a>", 404

# Manejo de errores 500
@app.errorhandler(500)
def internal_error(e):
    return f"<h1>500 - Error interno del servidor</h1><a href='{url_for('login')}'>Volver al inicio</a>", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
