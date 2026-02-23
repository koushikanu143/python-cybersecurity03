#python regex library for password strength checker 
import re 
password = input("Enter password: ") 
if (len(password)>=8 and 
    re.search("[A-Z]", password) and 
    re.search("[a-z]", password) and 
    re.search("[0-9]", password) and 
    re.search("[@#$%^&*]", password)): 
    print("Strong password") 
else: 
    print("Weak password")