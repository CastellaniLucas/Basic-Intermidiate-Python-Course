import hashlib
import getpass
import random
import time
import math

diccionario = [
    "agua", "sol", "luna", "tierra", "fuego", "aire", "bosque", "río", "mar", "montaña",
    "valle", "nube", "viento", "roca", "arena", "cielo", "estrella", "planeta", "universo", "galaxia",
    "animal", "planta", "flor", "hoja", "fruta", "semilla", "tronco", "raíz", "lago", "océano",
    "barco", "puerto", "ciudad", "pueblo", "campo", "camino", "carretera", "auto", "bicicleta", "tren",
    "avión", "puente", "casa", "edificio", "ventana", "puerta", "techo", "piso", "pared", "habitación",
    "cama", "silla", "mesa", "escritorio", "lámpara", "reloj", "cuadro", "libro", "cuaderno", "lapicera",
    "lápiz", "goma", "regla", "computadora", "pantalla", "teclado", "ratón", "cable", "teléfono", "televisor",
    "radio", "música", "canción", "guitarra", "piano", "violín", "batería", "voz", "nota", "melodía",
    "ritmo", "baile", "arte", "pintura", "escultura", "fotografía", "cine", "teatro", "poesía", "libreto",
    "historia", "cuento", "novela", "palabra", "letra", "frase", "oración", "párrafo", "texto", "idioma",
    "lengua", "voz", "oído", "ojo", "nariz", "boca", "mano", "brazo", "pierna", "pie",
    "cabeza", "cara", "cabello", "piel", "corazón", "pulmón", "cerebro", "hueso", "músculo", "sangre",
    "vida", "muerte", "amor", "odio", "alegría", "tristeza", "miedo", "valentía", "esperanza", "paz",
    "guerra", "conflicto", "familia", "amigo", "enemigo", "niño", "niña", "hombre", "mujer", "persona",
    "gente", "sociedad", "comunidad", "escuela", "facultad", "universidad", "profesor", "alumno", "clase", "examen",
    "nota", "tarea", "trabajo", "oficina", "empresa", "fábrica", "tienda", "mercado", "dinero", "precio",
    "valor", "billete", "moneda", "banco", "tarjeta", "cuenta", "ahorro", "deuda", "impuesto", "sueldo",
    "economía", "política", "gobierno", "presidente", "ministro", "ley", "justicia", "derecho", "policía", "ejército",
    "país", "nación", "frontera", "bandera", "himno", "cultura", "tradición", "costumbre", "idioma", "religión",
    "fiesta", "comida", "bebida", "pan", "carne", "pescado", "pollo", "huevo", "leche", "queso",
    "fruta", "verdura", "arroz", "pasta", "azúcar", "sal", "aceite", "vinagre", "agua", "vino",
    "cerveza", "café", "té", "jugo", "postre", "helado", "torta", "galleta", "chocolate", "caramelo",
    "tiempo", "hora", "minuto", "segundo", "día", "semana", "mes", "año", "siglo", "mañana",
    "tarde", "noche", "ayer", "hoy", "mañana", "pasado", "futuro", "presente", "pasado", "eternidad",
    "energía", "luz", "sombra", "color", "rojo", "azul", "verde", "amarillo", "negro", "blanco",
    "gris", "naranja", "violeta", "rosa", "marrón", "dorado", "plateado", "transparente", "oscuro", "claro",
    "forma", "línea", "punto", "círculo", "cuadro", "triángulo", "rectángulo", "figura", "dimensión", "volumen",
    "peso", "masa", "tamaño", "altura", "ancho", "profundidad", "distancia", "velocidad", "aceleración", "fuerza",
    "presión", "temperatura", "calor", "frío", "energía", "potencia", "resistencia", "corriente", "voltaje", "campo",
    "imán", "metal", "hierro", "cobre", "oro", "plata", "plomo", "acero", "plástico", "madera",
    "vidrio", "papel", "cartón", "cuero", "algodón", "lana", "seda", "piedra", "cerámica", "cemento",
    "arena", "polvo", "gas", "vapor", "líquido", "sólido", "átomo", "molécula", "química", "física",
    "matemática", "geometría", "álgebra", "estadística", "número", "suma", "resta", "multiplicación", "división", "ecuación",
    "fórmula", "gráfico", "vector", "matriz", "función", "derivada", "integral", "límite", "teorema", "prueba",
    "sistema", "control", "sensor", "actuador", "motor", "robot", "programa", "código", "algoritmo", "variable",
    "constante", "bucle", "condición", "lista", "diccionario", "conjunto", "tupla", "archivo", "dato", "bit",
    "byte", "memoria", "procesador", "chip", "circuito", "transistor", "resistor", "capacitor", "diodo", "led",
    "pantalla", "display", "sensor", "arduino", "raspberry", "microcontrolador", "oscilador", "frecuencia", "amplitud", "fase",
    "onda", "seno", "coseno", "tangente", "impulso", "respuesta", "retroalimentación", "error", "controlador", "modelo",
    "planta", "estado", "salida", "entrada", "referencia", "ruido", "disturbio", "estabilidad", "polo", "cero",
    "banda", "ancho", "frecuencia", "resonancia", "ganancia", "fase", "retardo", "tiempo", "respuesta", "constante",
    "transitorio", "permanente", "amplitud", "armónico", "senal", "analógico", "digital", "muestreo", "cuantización", "filtro",
    "pasabajo", "pasaalto", "pasabanda", "notch", "fft", "espectro", "frecuencia", "dominio", "transformada", "laplace",
    "zeta", "discreto", "continuo", "controlador", "PID", "observador", "modelo", "espacio", "estados", "realimentación", "aceptar", "acceso", "acido", "activo", "actor", "actividad", "agenda", "agencia",
    "agricultura", "alcance", "alegoria", "alianza", "almacen", "alto", "ambiente",
    "ambiguo", "analisis", "anterior", "apetito", "aplicacion", "apoyo", "arreglo",
    "articulo", "asiento", "asegurar", "asignatura", "asistencia", "asociacion",
    "aspecto", "audio", "avanzar", "barrera", "basico", "beneficio", "biblioteca",
    "bloque", "bomba", "botella", "brillo", "brisa", "brote", "bruto", "buscar",
    "cabina", "calidad", "calendario", "calle", "calma", "camara", "cambio", "camisa",
    "campana", "cantante", "capacidad", "capitulo", "captura", "cartel", "carta",
    "casco", "caza"
]

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
    print("Cuando el contador llegue a 0 deberá escribir la palabra que aparece en pantalla lo más rápido posible")
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

    num = random.randint(1, 500)
    print(f"La palabra es: {diccionario[num]}")
    inicio = time.time()
    palabra_escrita = input("Escribí la palabra que aparece en pantalla: ")
    fin = time.time()
    tiempo_transcurrido = fin - inicio

    if diccionario[num] != palabra_escrita:
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
