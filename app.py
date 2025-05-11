# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Cadena de conexión para SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://sa:AMPUERO20%23@localhost/ReservasCabana?driver=ODBC+Driver+17+for+SQL+Server'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Cliente
class Cliente(db.Model):
    __tablename__ = 'Clientes'  # Nombre exacto de la tabla en SQL Server
    ID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Correo = db.Column(db.String(100), nullable=False)
    Telefono = db.Column(db.String(15))
    Identificacion = db.Column(db.String(20))

    def __repr__(self):
        return f'<Cliente {self.Nombre}>'

# Ruta para crear un nuevo cliente
@app.route('/crear_cliente', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        # Capturamos los datos del formulario
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        identificacion = request.form['identificacion']

        # Validación en el backend para duplicados
        cliente_existente = Cliente.query.filter(
            (Cliente.Correo == correo) | (Cliente.Identificacion == identificacion)
        ).first()

        if cliente_existente:
            # Si existe un cliente con el mismo correo o identificación
            mensaje = " Error: El correo o la identificación ya están registrados."
            print("Cliente duplicado encontrado.")
            return render_template('crear_cliente.html', error=mensaje)

        # Si no existe, se guarda el nuevo cliente
        nuevo_cliente = Cliente(
            Nombre=nombre,
            Correo=correo,
            Telefono=telefono,
            Identificacion=identificacion
        )

        db.session.add(nuevo_cliente)
        db.session.commit()
        print(" Cliente creado exitosamente.")
        
        # Redirigir al listado de clientes
        return redirect(url_for('leer_clientes'))

    # Si es un GET, se muestra el formulario
    return render_template('crear_cliente.html')

#Ruta para leer clientes
@app.route('/clientes', methods=['GET'])
def leer_clientes():
    print(">>>> Entrando a la ruta /clientes")
    clientes = Cliente.query.all()  # Trae todos los clientes de la BD
    print(f">>>> Clientes encontrados: {clientes}")
    if not clientes:
        print(">>> No se encontraron clientes en la base de datos.")
    return render_template('clientes.html', clientes=clientes)

# Ruta para editar un cliente
@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get(id)
    
    # Verificación de existencia
    if not cliente:
        return render_template('error.html', mensaje="El cliente que intentas editar no existe.")

    if request.method == 'POST':
        cliente.Nombre = request.form['nombre']
        cliente.Correo = request.form['correo']
        cliente.Telefono = request.form['telefono']
        cliente.Identificacion = request.form['identificacion']

        # Validación del formulario
        if not cliente.Telefono.isdigit() or len(cliente.Telefono) < 8:
            return render_template('error.html', mensaje="El teléfono debe ser numérico y contener al menos 8 dígitos.")
        
        try:
            db.session.commit()
            return redirect('/clientes')
        except:
            return render_template('error.html', mensaje="Hubo un problema al actualizar el cliente.")
    
    return render_template('editar_cliente.html', cliente=cliente)

# Ruta para eliminar un cliente
@app.route('/eliminar_cliente/<int:id>', methods=['GET'])
def eliminar_cliente(id):
    cliente = Cliente.query.get(id)
    
    # Verificación de existencia
    if not cliente:
        return render_template('error.html', mensaje="El cliente que intentas eliminar no existe.")

    try:
        db.session.delete(cliente)
        db.session.commit()
        return redirect('/clientes')
    except:
        return render_template('error.html', mensaje="Hubo un problema al eliminar el cliente.")

# Iniciar la aplicación
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


