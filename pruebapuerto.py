import serial

try:
    ser = serial.Serial('COM9', 9600, timeout=2)
    print("✅ Puerto COM9 abierto correctamente")
    ser.close()
except Exception as e:
    print("❌ Error al abrir COM9:", e)
