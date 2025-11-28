from flask import Flask, request, session, render_template, redirect, url_for, flash
import sqlite3
import hashlib
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_muy_segura_2024'

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash('Debe iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# en este apartado se encarga de defininir que puede hacer y que no cada rol
def rol_requerido(rol_permitido):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # el admin siempre tiene acceso y los demas solo si se los permite su rol
            if session.get('rol') != rol_permitido and session.get('rol') != 'ADMIN':
                flash('Acceso denegado. Solo el rol de ADMIN o el rol específico pueden realizar esta acción.',
                      'danger')

                # redirige al index si no tiene acceso a hacer algo
                return redirect(url_for('inicio'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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

        # Encripta la contraseña con MD5 (igual que en la BD)
        password_encriptada = hashlib.md5(password.encode()).hexdigest()

        # Busca al usuario en la base de datos
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

# Ruta principal
@app.route('/')
def index():
    session.clear()
    if 'usuario' in session:
        return redirect(url_for('inicio'))
    return redirect(url_for('login'))

# Ruta del login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya hay una sesión activa redirige al inicio
    if 'usuario' in session:
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        password = request.form.get('password', '')

        # Valida que los campos no estén vacíos en la app
        if not nombre or not password:
            flash('Por favor, complete todos los campos', 'error')
            return render_template('login.html')

        # Verifica las credenciales
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

# Ruta de inicio protegida con el login
@app.route('/inicio')
@login_requerido
def inicio():
    return render_template('inicio.html',
                           usuario=session.get('usuario'),
                           rol=session.get('rol'),
                           nombre_completo=session.get('nombre_completo'))

# Ruta de productos
@app.route('/productos')
@login_requerido
def productos():
    conn = get_db_connection()
    cursor = conn.cursor()

    nombre = request.args.get('nombre', '').strip()
    departamento = request.args.get('departamento', '').strip()
    almacen_id = request.args.get('almacen_id', '').strip()

    precio_min = request.args.get('precio_min', '').strip()
    precio_max = request.args.get('precio_max', '').strip()
    cantidad_min = request.args.get('cantidad_min', '').strip()
    cantidad_max = request.args.get('cantidad_max', '').strip()

    query = 'SELECT * FROM productos WHERE 1=1'
    params = []

    if nombre:
        query += ' AND nombre LIKE ?'
        params.append('%' + nombre + '%')

    if departamento:
        query += ' AND departamento LIKE ?'
        params.append('%' + departamento + '%')

    if almacen_id:
        query += ' AND almacen = ?'
        params.append(almacen_id)

    if precio_min and precio_min.replace('.', '', 1).isdigit():
        query += ' AND precio >= ?'
        params.append(float(precio_min))

    if precio_max and precio_max.replace('.', '', 1).isdigit():
        query += ' AND precio <= ?'
        params.append(float(precio_max))

    if cantidad_min and cantidad_min.isdigit():
        query += ' AND cantidad >= ?'
        params.append(int(cantidad_min))

    if cantidad_max and cantidad_max.isdigit():
        query += ' AND cantidad <= ?'
        params.append(int(cantidad_max))

    cursor.execute(query, params)
    productos = cursor.fetchall()

    almacenes_list = conn.execute('SELECT id, nombre FROM almacenes').fetchall()
    conn.close()

    filter_values = {
        'nombre': nombre, 'departamento': departamento, 'almacen_id': almacen_id,
        'precio_min': precio_min, 'precio_max': precio_max,
        'cantidad_min': cantidad_min, 'cantidad_max': cantidad_max
    }

    return render_template('productos.html',
                           productos=productos,
                           almacenes=almacenes_list,
                           usuario=session.get('rol'),
                           rol=session.get('rol'),
                           filter_values=filter_values)


# para crear un producto ya sea un ADMIN o PRODUCTOS
@app.route('/productos/crear', methods=['GET', 'POST'])
@login_requerido
@rol_requerido('PRODUCTOS')  # solo ADMIN o PRODUCTOS pueden crear
def crear_producto():
    conn = get_db_connection()
    almacenes_list = conn.execute('SELECT id, nombre FROM almacenes').fetchall()

    if request.method == 'POST':
        nombre = request.form['nombre']
        departamento = request.form['departamento']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        almacen_id = request.form['almacen_id']

        # Validación básica
        if not nombre or not precio or not cantidad or not almacen_id:
            flash('Error: Los campos Nombre, Precio, Cantidad y Almacén son obligatorios.', 'danger')
        else:
            try:
                conn.execute('''
                    INSERT INTO productos (nombre, departamento, precio, cantidad, almacen)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nombre, departamento, float(precio), int(cantidad), int(almacen_id)))
                conn.commit()
                flash(f'Producto "{nombre}" creado exitosamente.', 'success')
                return redirect(url_for('productos'))
            except ValueError:
                flash('Error: El precio y la cantidad deben ser números válidos.', 'danger')
            except sqlite3.Error as e:
                flash(f'Error al crear el producto: {e}', 'danger')

    conn.close()
    return render_template('producto_form.html',
                           form_title='Crear Nuevo Producto',
                           almacenes=almacenes_list)

# para modificar un producto ya sea un ADMIN o PRODUCTOS
@app.route('/productos/modificar/<int:id>', methods=['GET', 'POST'])
@login_requerido
@rol_requerido('PRODUCTOS')  # solo ADMIN o PRODUCTOS pueden modificar
def modificar_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    almacenes_list = conn.execute('SELECT id, nombre FROM almacenes').fetchall()

    if producto is None:
        conn.close()
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('productos'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        departamento = request.form['departamento']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        almacen_id = request.form['almacen_id']

        if not nombre or not precio or not cantidad or not almacen_id:
            flash('Error: Los campos Nombre, Precio, Cantidad y Almacén son obligatorios.', 'danger')
        else:
            try:
                conn.execute('''
                    UPDATE productos SET 
                        nombre = ?, departamento = ?, precio = ?, 
                        cantidad = ?, almacen = ?
                    WHERE id = ?
                ''', (nombre, departamento, float(precio), int(cantidad), int(almacen_id), id))
                conn.commit()
                flash(f'Producto "{nombre}" actualizado exitosamente.', 'success')
                return redirect(url_for('productos'))
            except ValueError:
                flash('Error: El precio y la cantidad deben ser números válidos.', 'danger')
            except sqlite3.Error as e:
                flash(f'Error al modificar el producto: {e}', 'danger')

    conn.close()
    return render_template('producto_form.html',
                           form_title=f'Modificar Producto: {producto["nombre"]}',
                           producto=producto,
                           almacenes=almacenes_list)

# para eliminar un producto ya sea un ADMIN o PRODUCTOS
@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_requerido
@rol_requerido('PRODUCTOS')  # solo ADMIN o PRODUCTOS pueden eliminar
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    producto = cursor.execute('SELECT nombre FROM productos WHERE id = ?', (id,)).fetchone()

    if producto is None:
        conn.close()
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('productos'))

    try:
        cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash(f'Producto "{producto["nombre"]}" eliminado exitosamente.', 'success')
    except sqlite3.Error as e:
        flash(f'Error al eliminar el producto: {e}', 'danger')

    return redirect(url_for('productos'))

# Ruta de almacenes
@app.route('/almacenes')
@login_requerido
def almacenes():
    conn = get_db_connection()
    cursor = conn.cursor()

    nombre = request.args.get('nombre', '').strip()

    query = 'SELECT * FROM almacenes WHERE 1=1'
    params = []

    if nombre:
        query += ' AND nombre LIKE ?'
        params.append('%' + nombre + '%')

    cursor.execute(query, params)
    almacenes = cursor.fetchall()
    conn.close()

    filter_values = {
        'nombre': nombre
    }

    return render_template('almacenes.html',
                           almacenes=almacenes,
                           usuario=session.get('usuario'),
                           rol=session.get('rol'),
                           filter_values=filter_values)

# para crear un almacen ya sea un ADMIN o ALMACENES
@app.route('/almacenes/crear', methods=['GET', 'POST'])
@login_requerido
@rol_requerido('ALMACENES')  # solo ADMIN o ALMACENES pueden crear
def crear_almacen():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()

        if not nombre:
            flash('Error: Todos los campos son obligatorios', 'danger')
            return render_template('almacen_form.html', form_title='Crear Nuevo Almacén')

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO almacenes (nombre)
            VALUES (?)
        """, (nombre,))
        conn.commit()
        conn.close()

        flash(f'Almacén "{nombre}" creado exitosamente.', 'success')
        return redirect(url_for('almacenes'))

    return render_template('almacen_form.html', form_title='Crear Nuevo Almacén')

# para modificar un almacen ya sea un ADMIN o ALMACENES
@app.route('/almacenes/modificar/<int:id>', methods=['GET', 'POST'])
@login_requerido
@rol_requerido('ALMACENES')  # solo ADMIN o ALMACENES pueden modificar
def modificar_almacen(id):
    conn = get_db_connection()
    almacen = conn.execute('SELECT * FROM almacenes WHERE id = ?', (id,)).fetchone()

    if almacen is None:
        conn.close()
        flash('Almacén no encontrado.', 'danger')
        return redirect(url_for('almacenes'))

    if request.method == 'POST':
        nombre = request.form['nombre']

        if not nombre:
            flash('Error: El nombre es obligatorio.', 'danger')
        else:
            try:
                conn.execute('''
                    UPDATE almacenes SET nombre = ?
                    WHERE id = ?
                ''', (nombre, id,))
                conn.commit()
                conn.close()
                flash(f'Almacén "{nombre}" actualizado exitosamente.', 'success')
                return redirect(url_for('almacenes'))
            except sqlite3.Error as e:
                flash(f'Error al modificar el almacén: {e}', 'danger')
    conn.close()
    return render_template('almacen_form.html', form_title=f'Modificar Almacén: {almacen["nombre"]}', almacen=almacen)

# para eliminar un almacen ya sea un ADMIN o ALMACENES
@app.route('/almacenes/eliminar/<int:id>', methods=['POST'])
@login_requerido
@rol_requerido('ALMACENES')  # solo ADMIN o ALMACENES pueden eliminar
def eliminar_almacen(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    almacen = cursor.execute('SELECT nombre FROM almacenes WHERE id = ?', (id,)).fetchone()

    if almacen is None:
        conn.close()
        flash('Almacén no encontrado.', 'danger')
        return redirect(url_for('almacenes'))

    try:
        cursor.execute('DELETE FROM almacenes WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash(f'Almacén "{almacen["nombre"]}" eliminado exitosamente.', 'success')
    except sqlite3.Error as e:
        flash(f'Error al eliminar el almacén: {e}', 'danger')

    return redirect(url_for('almacenes'))

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

