import requests 

url = input("Enter URL: ")

r = requests.get(url)

headers = ["x-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security"]

for h in headers:
    if h in r.headers:
        print(h, " : Present")
    else:
        print(h, " : Missing(potential risk)")