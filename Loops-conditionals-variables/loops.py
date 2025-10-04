age = int(input("Please, insert your age: "))

if 0<= age < 12:
    print("You are a child")
elif 12<= age < 18:
    print("You are a teenager")
elif 18 <= age < 60:
    print("You are an adult")
elif 60 <= age < 120:
    print("You are an elderly")
else: 
    print("Please, insert a valid age, just numbers")
