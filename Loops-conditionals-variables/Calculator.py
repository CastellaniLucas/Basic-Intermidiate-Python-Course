password = "1234"
passw = input("Enter your password: ")

exit = 0
while(not(exit)):
    if (passw == password):
        print("Welcome Back to the best calculator of the world")
        print("What do you want to calculate?")
        print("1. Sum")
        print("2. Substraction")
        print("3. Multiplication")
        print("4. Divition")
        print("5. Exit")
        selection = int(input())
        if (selection == 5):
            exit = 1
            print("Goodbye My Lord Commander")
        elif(selection == 1):
            a = int(input("Enter the first operand: "))
            b = int(input("Enter the second operand: "))
            c = a + b           
            print(f"The sum of {a} + {b} is equal to {c}")
            input()

        elif(selection == 2):
            a = int(input("Enter the first operand: "))
            b = int(input("Enter the second operand: "))
            c = a - b           
            print(f"The substraction of {a} - {b} is equal to {c}")
            input()

        elif(selection == 3):
            a = int(input("Enter the first operand: "))
            b = int(input("Enter the second operand: "))
            c = a * b           
            print(f"The multiplication of {a} * {b} is equal to {c}")
            input()
        
        elif(selection == 4):
            a = int(input("Enter the first operand: "))
            b = int(input("Enter the second operand: "))
            if (b != 0):
                c = a / b           
                print(f"The divition of {a} / {b} is equal to {c}")
                input()
            else:
                print("Indeterminated. Divition by 0")
                input()

        else:
            print("Invalid access. Try Again")
    else:
        print("Invalid password, try again, or quit(1)")
        if(int(input()) == 1):
            exit = 1
            print("Goodbye My Lord Commander")
        else:
            continue
    

