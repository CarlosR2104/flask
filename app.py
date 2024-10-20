from flask import Flask, render_template, request, jsonify, make_response
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

# Ruta para mostrar la página principal
@app.route("/")
def index():
    return render_template("alumnos.html")

# Ruta para buscar alumnos
@app.route("/alumnos/buscar")
def buscar_alumnos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumnos ORDER BY matricula DESC")
    alumnos = cursor.fetchall()

    con.close()
    return make_response(jsonify(alumnos))

# Ruta para guardar un nuevo alumno o actualizar uno existente
@app.route("/alumnos/guardar", methods=["POST"])
def guardar_alumno():
    if not con.is_connected():
        con.reconnect()

    matricula = request.form["matricula"]
    nombreapellido = request.form["nombreapellido"]

    cursor = con.cursor()

    if matricula:  # Si existe la matrícula, actualizamos
        sql = """
        UPDATE alumnos SET NombreApellido = %s WHERE matricula = %s
        """
        val = (nombreapellido, matricula)
    else:  # Si no, creamos un nuevo registro
        sql = """
        INSERT INTO alumnos (matricula, NombreApellido) VALUES (%s, %s)
        """
        val = (matricula, nombreapellido)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({"status": "success"}))

# Ruta para eliminar un alumno
@app.route("/alumnos/eliminar", methods=["POST"])
def eliminar_alumno():
    if not con.is_connected():
        con.reconnect()

    matricula = request.form["matricula"]
    cursor = con.cursor()
    sql = "DELETE FROM alumnos WHERE matricula = %s"
    cursor.execute(sql, (matricula,))
    con.commit()
    con.close()

    return make_response(jsonify({"status": "deleted"}))

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)

