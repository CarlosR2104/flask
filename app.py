from flask import Flask, render_template, request
import mysql.connector
import datetime
import pytz

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Ruta principal
@app.route("/")
def index():
    con.close()
    return render_template("app.html")

# Ruta para mostrar alumnos (ejemplo de vista usando templates)
@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

# Ruta para guardar los datos de la reserva en la tabla tst0_reservad
@app.route("/reservas/guardar", methods=["POST"])
def reservasGuardar():
    if not con.is_connected():
        con.reconnect()

    # Captura de los datos del formulario
    nombre_apellido = request.form["txtNombreApellido"]
    telefono = request.form["txtTelefono"]
    fecha = datetime.datetime.now(pytz.timezone("America/Matamoros"))  # Fecha actual

    # Inserción en la base de datos
    cursor = con.cursor()
    sql = "INSERT INTO tst0_reservad (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
    val = (nombre_apellido, telefono, fecha)
    cursor.execute(sql, val)
    con.commit()

    # Cierre de conexión
    con.close()

    # Retorno de mensaje de éxito
    return f"Reserva guardada: Nombre y Apellido {nombre_apellido}, Teléfono {telefono}, Fecha {fecha}"

# Ruta para buscar registros de reservas
@app.route("/reservas/buscar")
def reservasBuscar():
    if not con.is_connected():
        con.reconnect()

    # Búsqueda de registros en la tabla tst0_reservad
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_reservad ORDER BY Id_Reserva DESC")
    registros = cursor.fetchall()

    con.close()

    return registros

if __name__ == "__main__":
    app.run(debug=True)
