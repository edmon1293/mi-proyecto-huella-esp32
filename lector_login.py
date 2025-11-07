import serial
import time
import webbrowser

PORT = 'COM9'        # Cambia esto según tu sistema
BAUDRATE = 9600

# Comando binario Identify1_N (buscar coincidencia en todas las plantillas)
CMD_IDENTIFY_1_N = b'\x55\xAA\x01\x00\x01\x00\x00\x00\x11\x01\x12\x00'  # ID 0x11

def iniciar_sesion_por_huella():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=2)
        print("🔌 Conectado al sensor...")
        ser.write(CMD_IDENTIFY_1_N)
        print("🖐️ Esperando huella...")

        time.sleep(1)  # Pequeña espera

        response = ser.read(12)  # Esperar 12 bytes de respuesta (paquete corto)
        if len(response) == 12 and response[9] == 0x00:
            id_detectado = response[10]
            print(f"✅ Huella reconocida. ID = {id_detectado}")
            url = f"http://localhost:8000/login_sensor/{id_detectado}/"
            webbrowser.open(url)
        else:
            print("❌ No se detectó coincidencia.")

        ser.close()

    except Exception as e:
        print("⚠️ Error al comunicarse con el lector:", e)

if __name__ == "__main__":
    iniciar_sesion_por_huella()
