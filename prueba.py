from fplib import fplib
import time
import webbrowser

fp = fplib(port='COM9', baud=9600, timeout=3)

if not fp.init():
    print("❌ No se pudo inicializar el sensor.")
    exit()

fp.set_led(True)
print("🖐️ Coloca tu dedo para identificar...")

user_id = -1
timeout_segundos = 10
inicio = time.time()

while time.time() - inicio < timeout_segundos:
    user_id = fp.identify()
    if user_id != -1 and user_id is not None:
        break
    time.sleep(0.5)  # Espera medio segundo antes de volver a intentar

fp.set_led(False)

if user_id != -1 and user_id is not None:
    print(f"✅ Huella reconocida como ID {user_id}")
    url = f"http://localhost:8000/login_sensor/{user_id}"
    webbrowser.open(url)
else:
    print("⏱️ Tiempo agotado. No se detectó ninguna huella.")
    print("👥 Total de huellas registradas:", fp.get_enrolled_cnt())
    print("🤏 ¿Dedo detectado?", fp.is_finger_pressed())
fp.set_led(True)  # Enciende LED antes de buscar
print("🖐️ Coloca el mismo dedo con el que te registraste...")

id_detectado = fp.identify()
fp.set_led(False)

if id_detectado != -1:
    print("✅ Huella reconocida como ID:", id_detectado)
else:
    print("❌ No se pudo reconocer ninguna huella.")
