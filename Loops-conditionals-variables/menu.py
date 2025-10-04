# INTRODCUCCIÓN A INPUT + MENÚ

print("🍽️ Bienvenidos al Restaurante ChatGourmet")
print("Menú:")
print("1. Ver entradas")
print("2. Ver platos principales")
print("3. Ver vinos")
print("4. Ver postres")

opcion = int(input('Elija para ver el menú: 1, 2 , 3 ,4'))

if opcion == 1:
    print("\n🥗 Entradas:")
    print("- Bruschettas: $1200")
    print("- Ensalada caprese: $1500")

elif opcion == 2:
    print("\n🍝 Platos principales:")
    print("- Ñoquis con pesto: $2500")
    print("- Milanesa con papas: $2800")
    print("- Risotto de hongos: $3100")
elif opcion == 3:
    print("\n🍷 Vinos:")
    print("- Malbec reserva: $4500")
    print("- Chardonnay joven: $3800")

elif opcion == 4:
    print("\n🍰 Postres:")
    print("- Tiramisú: $1800")
    print("- Flan con dulce de leche: $1600")
    print("- Helado artesanal: $1500")

else:
    print("\n❌ Opción no válida.")


