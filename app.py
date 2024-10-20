from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import datetime
import pytz

# Configuración de la conexión a la base de datos
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

# Ruta para insertar o actualizar reservas
@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id_reserva     = request.form["id_reserva"]  # Campo ID de la reserva
    nombre_apellido = request.form["nombre_apellido"]  # Campo Nombre y Apellido
    telefono        = request.form["telefono"]  # Campo Teléfono
    fecha           = request.form["fecha"]  # Campo Fecha (debería ser formato YYYY-MM-DD)
    
    cursor = con.cursor()

    if id_reserva:  # Si el ID existe, actualiza la reserva
        sql = """
        UPDATE tst0_reservas SET
        Nombre_Apellido = %s,
        Telefono = %s,
        Fecha = %s
        WHERE Id_Reserva = %s
        """
        val = (nombre_apellido, telefono, fecha, id_reserva)
    else:  # Si el ID no existe, inserta una nueva reserva
        sql = """
        INSERT INTO tst0_reservas (Nombre_Apellido, Telefono, Fecha)
        VALUES (%s, %s, %s)
        """
        val = (nombre_apellido, telefono, fecha)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({"success": True}))

# Ruta para buscar reservas recientes
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

# Ruta para editar una reserva existente
@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id_reserva = request.args["id_reserva"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Reserva, Nombre_Apellido, Telefono, Fecha 
    FROM tst0_reservas
    WHERE Id_Reserva = %s
    """
    val    = (id_reserva,)

    cursor.execute(sql, val)
    registro = cursor.fetchone()
    con.close()

    return make_response(jsonify(registro))

# Ruta para eliminar una reserva
@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not con.is_connected():
        con.reconnect()

    id_reserva = request.form["id_reserva"]

    cursor = con.cursor()
    sql    = """
    DELETE FROM tst0_reservas
    WHERE Id_Reserva = %s
    """
    val    = (id_reserva,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({"success": True}))

if __name__ == "__main__":
    app.run(debug=True)

