import requests
import subprocess
import sys
import json
 
token = 'A043EiWn_o_G5QzgMQRbfouFsk68-8TI8Sc_xAcWsqQNFY8Kg83nMv8Vv32kEOUMbj-O_k4xyNgIumDjpwdd1A'
 
call_header = {'accept':'application/json','Authorization': 'Bearer ' + token}
 
url = 'https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient'
 
response = requests.get(url, headers=call_header, verify=True)
patients = json.loads(response.text)["entry"]

search = input("Please enter the MRN: ")
find = False
for patient in patients:
    if "identifier" in patient["resource"]:
        if patient["resource"]["identifier"][1]["value"] == search:
            find = True
            print(patient["resource"]["name"][0]["family"][0] + " " + patient["resource"]["name"][0]["given"][0])
            break
if find == False:
    print("Patient not found!")
