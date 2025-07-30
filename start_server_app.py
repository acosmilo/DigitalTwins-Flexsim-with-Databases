from flask import Flask, request
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/cafetera", methods=["POST"]) # Aqui siempre poner el url de Ngrok
def recibir_datos():
    data = request.get_json()
    estado = data.get("estado")
    temperatura = data.get("temperatura")

    if estado is None or temperatura is None:
        return {"status": "error", "message": "Datos incompletos"}, 400

    try:
        conexion = pymysql.connect(
            host="localhost",
            user="root",          # Cambia si usas otro usuario
            password="dragonesXsiempre",      # Usa tu contraseña real
            database="cafetera_db"
        )
        cursor = conexion.cursor()
        sql = "INSERT INTO datos_cafetera (estado, temperatura) VALUES (%s, %s)"
        cursor.execute(sql, (estado, temperatura))
        conexion.commit()
        conexion.close()

        return {"status": "ok"}, 200
    except Exception as e:
        print("ERROR FLASK:", e)   # <--- Agrega esto
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
