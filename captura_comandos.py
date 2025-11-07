from fplib import fplib
import time

# Inicializa el sensor
fp = fplib(port='COM9', baud=9600, timeout=3)

# Modifica fplib para imprimir los comandos enviados
# Ya debes tener esto en fpmain.py dentro de _send_packet():
# print(f"[DEBUG] Comando enviado ({cmd}):", [hex(b) for b in packet])

# Ejecuta cada comando para capturar su paquete UART
comandos = [
    ("Open", None),
    ("CmosLed", 1),
    ("Identify1_N", None),
    ("GetEnrollCount", None),
    ("IsPressFinger", None),
    ("EnrollStart", 3),
    ("Enroll1", None),
    ("Enroll2", None),
    ("Enroll3", None),
    ("DeleteID", 3),
    ("DeleteAll", None),
    ("CaptureFinger", None),
    ("MakeTemplate", None)
]

for nombre, parametro in comandos:
    print(f"\n📦 Enviando comando: {nombre}")
    fp._send_packet(nombre, parametro if parametro is not None else 0)
    time.sleep(0.5)
    