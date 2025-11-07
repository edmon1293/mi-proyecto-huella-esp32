from fplib import fplib
import time

fp = fplib(port='COM9', baud=9600, timeout=3)

if not fp.init():
    print("❌ No se pudo inicializar el sensor.")
    exit()

def mostrar_menu():
    print("\n----- MENÚ DE PRUEBA BIOMÉTRICA -----")
    print("1. Ver cantidad de huellas registradas")
    print("2. Registrar nueva huella")
    print("3. Identificar huella")
    print("4. Eliminar huella por ID")
    print("5. Eliminar todas las huellas")
    print("6. Salir")

while True:
    mostrar_menu()
    opcion = input("Selecciona una opción (1–6): ")

    if opcion == "1":
        print("👥 Cantidad de huellas:", fp.get_enrolled_cnt())

    elif opcion == "2":
        idx = int(input("🆔 Ingresa el ID donde guardar (por ejemplo 2): "))
        print("🖐️ Coloca tu dedo...")
        fp.set_led(True)
        if fp.is_finger_pressed():
            id, data, stat = fp.enroll()
            if stat:
                print(f"✅ Huella registrada exitosamente como ID {id}")
            else:
                print("❌ Error al registrar huella.")
        else:
            print("⚠️ No detecta dedo. Intenta de nuevo.")
        fp.set_led(False)

    elif opcion == "3":
        print("🧠 Esperando huella para identificar...")
        fp.set_led(True)
        id = fp.identify()
        fp.set_led(False)
        if id != -1:
            print(f"✅ Huella reconocida como ID: {id}")
        else:
            print("❌ No se reconoció ninguna huella.")

    elif opcion == "4":
        idx = int(input("🧽 Ingresa el ID a eliminar: "))
        if fp.delete(idx=idx):
            print(f"🗑️ Huella ID {idx} eliminada correctamente.")
        else:
            print("⚠️ No se pudo eliminar la huella.")

    elif opcion == "5":
        if fp.delete():
            print("🧨 ¡Todas las huellas han sido borradas!")
        else:
            print("⚠️ Error al borrar todas las huellas.")

    elif opcion == "6":
        print("👋 Saliendo del laboratorio biométrico.")
        break

    else:
        print("❌ Opción no válida.")
