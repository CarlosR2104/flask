from flask import Flask, render_template, request
import mysql.connector
import datetime
import pytz
import pusher

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

# Ejemplo de ruta GET usando templates para mostrar una vista
@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

# Ejemplo de ruta POST para guardar información en la tabla tst0_reservas
@app.route("/reservas/guardar", methods=["POST"])
def reservasGuardar():
    nombre_apellido = request.form["txtNombreApellido"]
    telefono = request.form["txtTelefono"]

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha) VALUES (%s, %s, %s)"
    fecha = datetime.datetime.now(pytz.timezone("America/Matamoros"))
    val = (nombre_apellido, telefono, fecha)
    cursor.execute(sql, val)
    con.commit()
    
    con.close()

    return f"Reserva guardada: Nombre y Apellido {nombre_apellido}, Teléfono {telefono}, Fecha {fecha}"

# Código usado en las prácticas para buscar reservas
@app.route("/reservas/buscar")
def reservasBuscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_reservas ORDER BY Id_Reserva DESC")
    registros = cursor.fetchall()

    con.close()

    return registros

if __name__ == "__main__":
    app.run(debug=True)
