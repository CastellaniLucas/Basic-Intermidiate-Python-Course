import hashlib
import getpass
import random
import time
import math

# --- Funciones ---
def generar_hash(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()


def verificar_contraseña(hash_correcto):
    intentos = 0
    while intentos < 3:
        contraseña_ingresada = getpass.getpass("Ingrese contraseña: ")
        hash_ingresada = generar_hash(contraseña_ingresada)

        if hash_ingresada == hash_correcto:
            print(" Contraseña correcta. Bienvenido!")
            return True
        else:
            intentos += 1
            print(f"Contraseña incorrecta. Intento {intentos} de 3.")
            time.sleep(1)
    print("Acceso denegado.")
    return False


def opcion1():
    print("\n--- Opción 1: Número aleatorio ---")
    print("Número generado:", random.randint(1, 1000))


def opcion2():
    print("\n--- Opción 2: Calcular raíz cuadrada ---")
    num = float(input("Ingresá un número: "))
    print("La raíz cuadrada es:", math.sqrt(num))


def opcion4():
    print("\n--- Opción 4: Mostrar hora actual ---")
    print("HORA ACTUAL", time.strftime("%H:%M:%S"))


def opcion3():
    print("\n--- Opción 3 : Sumar")
    a = int(input("Escriba el primer operando: "))
    b = int(input("Escriba el segundo operando: "))
    print(f"La suma es: {a+b}")


def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Generar número aleatorio")
    print("2. Calcular raíz cuadrada")
    print("3. Sumar")
    print("4. Mostrar hora actual")
    print("5. Juego de reflejos")
    print("6. Cambiar contraseña")
    print("7. Cerrar sesión")


def cambiar_contraseña(hash_contraseña_actual):
    print("\n--- CAMBIAR CONTRASEÑA ---")
    contraseña_vieja = getpass.getpass("Ingrese contraseña actual: ")
    hash_ingresado = generar_hash(contraseña_vieja)

    if hash_ingresado != hash_contraseña_actual:
        print("Contraseña incorrecta.")
        time.sleep(1)
        return hash_contraseña_actual

    contraseña_nueva = getpass.getpass("Ingrese contraseña nueva: ")
    contraseña_nueva_repetida = getpass.getpass("Repita contraseña nueva: ")

    if contraseña_nueva != contraseña_nueva_repetida:
        print("Las contraseñas no coinciden.")
        time.sleep(1)
        return hash_contraseña_actual
    else:
        print("Contraseña cambiada exitosamente.")
        time.sleep(1)
        return generar_hash(contraseña_nueva)

def juego_reflejos():
    print("\n--- JUEGO DE REFLEJOS ---")
    print("¿Cómo jugar?")
    print("Cuando el contador llegue a 0 deberá escribir el número que aparece en pantalla lo más rápido posible")
    print("¿Empezamos?")
    print("1. Empezar")
    print("2. Salir")
    opcion = input("Elegí una opción: ")
    if opcion == "1":
      juego_ref()
    else:
      print("Saliendo del juego...")
      time.sleep(1)
      return False

def juego_ref():
    print("¡Empezamos!")
    for i in range(5):
      print(f"Empezamos en {5-int(i)}")
      time.sleep(1)

    num = random.randint(1, 1000)
    print(f"El número es: {num}")
    inicio = time.time()
    numero_escrito = int(input("Escribí el número que aparece en pantalla: "))
    fin = time.time()
    tiempo_transcurrido = fin - inicio

    if num != numero_escrito:
      print("Perdiste!")
    else:
      print(f"Ganaste en {tiempo_transcurrido:.4f} segundos")


def opciones_mayor(opcion):
    global hash_correcto_usuario_mayor

    if opcion == "1":
        opcion1()
    elif opcion == "2":
        opcion2()
    elif opcion == "3":
        opcion3()
    elif opcion == "4":
        opcion4()
    elif opcion == "5":
        juego_reflejos()
    elif opcion == "6":
        hash_correcto_usuario_mayor = cambiar_contraseña(hash_correcto_usuario_mayor)
    elif opcion == "7":
        print(" Saliendo de la sesión...")
        time.sleep(1)
        return False
    else:
        print("Opción inválida, intentá de nuevo.")
    return True


def opciones_menor(opcion):
    global hash_correcto_usuario_menor

    if opcion == "1":
        opcion1()
    elif opcion == "2":
        opcion2()
    elif opcion == "3":
        opcion3()
    elif opcion == "4":
        opcion4()
    elif opcion == "5":
        juego_reflejos()
    elif opcion == "6":
        hash_correcto_usuario_menor = cambiar_contraseña(hash_correcto_usuario_menor)
    elif opcion == "7":
        print(" Saliendo de la sesión...")
        time.sleep(1)
        return False
    else:
        print("Opción inválida, intentá de nuevo.")
    return True




# --------------------------------------------------- Programa principal -------------------------------------------------------- #
usuario_mayor = "Lucas"
usuario_menor = "Luquitas"
hash_correcto_usuario_mayor = generar_hash("Python123!")  # contraseña por defecto
hash_correcto_usuario_menor = generar_hash("Python123")   # contraseña por defecto

while True:
    print("\n--- INICIO DE SESIÓN ---")
    print("1. Iniciar sesión")
    print("2. Salir del programa")

    opcion = input("Elegí una opción: ")

    if opcion == "1":
        print("Iniciando sesión...")
        time.sleep(1)
        usuario = input("Ingrese usuario: ")

        if usuario == usuario_mayor:
            if verificar_contraseña(hash_correcto_usuario_mayor):
                print(f"\nBienvenido {usuario}!")
                while True:
                    mostrar_menu()
                    if not opciones_mayor(input("Elegí una opción: ")):
                        break
            else:
                print("Contraseña incorrecta.")
                time.sleep(1)

        elif usuario == usuario_menor:
            if verificar_contraseña(hash_correcto_usuario_menor):
                print(f"\nBienvenido {usuario}!")
                while True:
                    mostrar_menu()
                    if not opciones_menor(input("Elegí una opción: ")):
                        break
            else:
                print("Contraseña incorrecta.")
                time.sleep(1)
        else:
            print("Usuario no encontrado.")
            time.sleep(1)

    elif opcion == "2":
        print("Saliendo del programa...")
        time.sleep(1)
        break

    else:
        print("Opción inválida, intentá de nuevo.")
        time.sleep(1)
