import serial
import time

PORT = 'COM9'
BAUDRATE = 9600
CMD_OPEN = b'\x55\xAA\x01\x00\x01\x00\x00\x00\x01\x00\x02\x00'

with serial.Serial(PORT, BAUDRATE, timeout=2) as ser:
    print("🔌 Enviando comando OPEN...")
    ser.write(CMD_OPEN)
    time.sleep(0.5)
    response = ser.read(12)
    print("📥 Respuesta cruda:", response.hex())
