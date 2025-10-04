pass_admin = "1234"
exit = 0
while (not(exit)):
    usr = input("Enter your username (admin, mod or user): ")
    passw = (input("Enter your password: "))

    if (usr == "admin" and passw == pass_admin):
        print("Welcome Back Admin!")
        print("Correct Password")
        print("1. See Users")
        print("2. Configuration")
        print("3. Exit")
        if (input() == "3"):
            exit = 1
    elif (usr == "admin" and passw != pass_admin):
        print("Usuario o contraseña no válidos")
    elif(usr != "admin" and passw == pass_admin):
        print(f"Welcome Back {usr}!")
        print("Correct Password")
        print("You are not an admin")
        print("1. Check Profile")
        print("2. Change Password")
        print("3. Exit")
        if (input() == "3"):
            exit = 1
    else: 
        print("Usuario o contraseña no válidos")