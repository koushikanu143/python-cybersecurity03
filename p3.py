name = input("Name: ") 
year = input("Birth year: ") 
 
common = ["123", "1234", "@123", "2004", "admin", "qwerty"] 
chars = "!@#$%^&*()" 
 
for c in common: 
    print(name + year + c) 
    print(name + chars[2] + year) 
    print(name.capitalize() + c) 