from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import datetime
import pytz
import pusher

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Ruta para la página principal
@app.route("/")
def index():
    con.close()
    return render_template("app.html")

# Ruta para la página de alumnos
@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

# Ruta para guardar alumnos (puedes ajustar esta función si no es necesaria)
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Código modificado para usar la tabla tst0_reservas
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Reserva, Nombre_Apellido, Telefono, DATE_FORMAT(Fecha, '%d/%m/%Y') AS Fecha 
    FROM tst0_reservas
    ORDER BY Id_Reserva DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()

    con.close()
    return make_response(jsonify(registros))

# Ruta para editar un registro en tst0_reservas
@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT Id_Reserva, Nombre_Apellido, Telefono, Fecha FROM tst0_reservas
    WHERE Id_Reserva = %s
    """
    val = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

# Ruta para guardar o actualizar un registro en tst0_reservas
@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id = request.form.get("id")
    nombre_apellido = request.form["nombre_apellido"]
    telefono = request.form["telefono"]
    fecha = request.form.get("fecha", datetime.datetime.now(pytz.timezone("America/Matamoros")).strftime('%Y-%m-%d'))

    cursor = con.cursor()

    if id:
        # Si el ID existe, actualizamos el registro
        sql = """
        UPDATE tst0_reservas SET
        Nombre_Apellido = %s,
        Telefono = %s,
        Fecha = %s
        WHERE Id_Reserva = %s
        """
        val = (nombre_apellido, telefono, fecha, id)
    else:
        # Si no hay ID, insertamos un nuevo registro
        sql = """
        INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha)
                        VALUES (%s,             %s,      %s)
        """
        val = (nombre_apellido, telefono, fecha)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    # Notificación con Pusher
    pusher_client = pusher.Pusher(
        app_id="1714541",
        key="3ce64b716f42fee14c9b",
        secret="dfe422af8d19a7130710",
        cluster="us2",
        ssl=True
    )

    pusher_client.trigger("canalReservas", "registroReserva", {})

    return jsonify({})
