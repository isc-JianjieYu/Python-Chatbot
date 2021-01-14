import requests
import sys
import json
import oauthlib

#credentials
USER = '_system'
PASS = 'SYS'



userip = input ("Enter patient with id")

ltxt = userip.split(" ")

print(f"first input :  {ltxt[0]}")

print(f"first input :  {ltxt[1]}")
if ltxt[0] == "patient":
    #URL for GET request
    url = "http://localhost:52777/rest/persons/" + ltxt[1]

    #Run GET
    response = requests.get(url, auth=(USER, PASS) )#, headers = headers, verify =False)
    print(response.text)


"""print(type(response.text))

#r_dict = json.dumps(r_list)
r_dict = json.loads(response.text)
print(type(r_dict))

sr = 1

for p in r_dict:
    print(f'{sr} : {p["Name"]}')
    sr+=1

print (response.text)"""