#open redirect checker
import requests

site = input("site: ")
payload = "?redirect=http://evil.com"

r = requests.get(site+payload)

if "evil.com" in r.url:
    print("open redirect possible")
else:
    print("no redirect detected")
