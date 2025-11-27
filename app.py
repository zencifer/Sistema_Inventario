from flask import Flask, request, session, render_template, redirect, url_for
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave segura

# Función de verificación de usuario
def verificar_usuario(nombre, password):
    conn = sqlite3.connect('instance/InventarioDB.db')
    cursor = conn.cursor()

    password_encriptada = hashlib.md5(password.encode()).hexdigest()

    cursor.execute('''
        SELECT * FROM usuarios 
        WHERE nombre = ? AND password = ?
    ''', (nombre, password_encriptada))

    usuario = cursor.fetchone()

    if usuario:
        cursor.execute('''
            UPDATE usuarios 
            SET fecha_hora_ultimo_inicio = ? 
            WHERE nombre = ?
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nombre))
        conn.commit()

    conn.close()
    return usuario

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        usuario = verificar_usuario(nombre, password)

        if usuario:
            session['usuario'] = nombre
            session['rol'] = usuario[4]  # El rol está en la columna 4
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')

    return render_template('login.html')

@app.route('/')
def home():
    if 'usuario' in session:
        return f"Bienvenido {session['usuario']} - Rol: {session['rol']}"
    return redirect(url_for('login'))

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')



if __name__ == '__main__':
    app.run(debug=True)