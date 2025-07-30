import serial
import time
import subprocess
import re

# ========== CONFIGURA TUS DATOS ==========
PUERTO_SERIAL = 'COM3'  # Cambia esto al COM real
BAUDIOS = 9600
URL_NGROK = 'https://6c5871d7ef05.ngrok-free.app/cafetera'  # Asegúrate que termina en /cafetera
# =========================================

# Intenta abrir el puerto
try:
    ser = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=2)
    time.sleep(2)  # Estabiliza la conexión
    print(f"[OK] Puerto {PUERTO_SERIAL} abierto correctamente.\n")
except Exception as e:
    print(f"[ERROR] No se pudo abrir {PUERTO_SERIAL}: {e}")
    exit()

# Bucle principal de lectura y envío
try:
    while True:
        # Leer línea del puerto
        linea = ser.readline().decode('utf-8', errors='ignore').strip()
        if not linea:
            continue

        print(f"[SERIAL] Línea recibida: {linea}")

        # Buscar temperatura entre signos de $
        match = re.search(r'\$(\d+(\.\d+)?)\$', linea)
        if not match:
            print("[WARN] No se encontró temperatura válida en la línea.\n")
            continue

        # Extraer temperatura y determinar estado
        temperatura = float(match.group(1))
        estado = "true" if temperatura > 35 else "false"

        print(f"[INFO] Temperatura: {temperatura}°C | Estado: {estado}")

        # Armar comando curl
        comando_curl = [
            "curl", "-X", "POST", URL_NGROK,
            "-H", "Content-Type: application/json",
            "-d", f'{{"estado": {estado}, "temperatura": {temperatura}}}'
        ]

        print("[CURL] Ejecutando comando:")
        print(" ".join(comando_curl))

        # Ejecutar el comando
        try:
            resultado = subprocess.run(comando_curl, capture_output=True, text=True)
            if resultado.stdout:
                print(f"[SERVER] Respuesta: {resultado.stdout.strip()}")
            if resultado.stderr:
                print(f"[CURL ERROR] {resultado.stderr.strip()}")
        except Exception as e:
            print(f"[ERROR] No se pudo ejecutar curl: {e}")

        print("-" * 50)
        time.sleep(5)

except KeyboardInterrupt:
    print("\n[STOP] Programa detenido por el usuario.")
    ser.close()
