from flask import Flask, render_template, request, jsonify
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

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id='1768024',
    key='25ef14f3e9a47c712e61',
    secret='31c5ddebc75a9419e7d2',
    cluster='us2',
    ssl=True
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

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

    # Emitir un evento de Pusher
    pusher_client.trigger('reservas-channel', 'nueva-reserva', {
        'nombre_apellido': nombre_apellido,
        'telefono': telefono,
        'fecha': fecha.strftime("%Y-%m-%d %H:%M:%S")
    })

    con.close()

    return f"Reserva guardada: {nombre_apellido}, Teléfono: {telefono}, Fecha: {fecha}"

@app.route("/reservas/buscar")
def reservasBuscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_reservas ORDER BY Id_Reserva DESC")
    registros = cursor.fetchall()

    con.close()

    return jsonify(registros)

@app.route("/reservas/actualizar", methods=["POST"])
def reservasActualizar():
    id_reserva = request.form["txtIdReserva"]
    nombre_apellido = request.form["txtNombreApellido"]
    telefono = request.form["txtTelefono"]

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "UPDATE tst0_reservas SET Nombre_Apellido = %s, Telefono = %s WHERE Id_Reserva = %s"
    val = (nombre_apellido, telefono, id_reserva)
    cursor.execute(sql, val)
    con.commit()

    con.close()

    return f"Reserva actualizada: {nombre_apellido}, Teléfono: {telefono}"

@app.route("/reservas/eliminar", methods=["POST"])
def reservasEliminar():
    id_reserva = request.form["id_reserva"]

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "DELETE FROM tst0_reservas WHERE Id_Reserva = %s"
    val = (id_reserva,)
    cursor.execute(sql, val)
    con.commit()

    con.close()

    return "Reserva eliminada correctamente"

if __name__ == "__main__":
    app.run(debug=True)
