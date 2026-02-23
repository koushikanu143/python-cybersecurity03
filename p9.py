import requests 

domain = input("Enter email ").split("@")[-1]

#public disposeable email list
url = "https://raw.githubusercontent.com/7c/fakefilter/main/txt/data.txt" 

data = requests.get(url).text.splitlines()

if domain in data:
    print("disposable email detected")
else:
    print(" likely real email")
