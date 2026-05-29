def check_pass(password):
    if len(password)<8:
        raise Exception("Password must be at least 8 characters long")
    print("password is strong")
try:
    password=input("enter the password ")
    check_pass(password)
except Exception as e:
    print(e)

