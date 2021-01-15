import requests
import subprocess
import sys
import json
 
token = 'h5VzZTu3AXByxveZ1NKY1xiZTSkZ-1IKxtqMKed_rXfAuG2-CjmTJ_kotvygXoQmzAOmze2--KOQOwrRrgGoow'
 
call_header = {'accept':'application/json','Authorization': 'Bearer ' + token}
 
url = 'https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/132/AllergyIntolerance'
 
response = requests.get(url, headers=call_header, verify=True)
allergies = json.loads(response.text)

for entry in allergies["entry"]:
    #print(entry)
    display = entry["resource"]["substance"]["text"]
    print(display)
    print("\n")
        
#add = "Name: " + patient["name"][0]["text"]  + "\n\nGender: " + patient["gender"]  + "\n\nDOB: " + patient["birthDate"] + "\n\nPhone: " + patient["telecom"][0]["value"] + "\n\nAddress: " + patient["address"][0]["line"][0] + ", " + patient["address"][0]["city"] + ", " + patient["address"][0]["postalCode"] + "\n\n" + "Care provider: " + patient["careProvider"][0]["reference"] + "\n\n" 

#print(patient["name"][0]["text"])
#print(patient["gender"])
#print(patient["birthDate"])
#print(patient["telecom"][0]["value"])
#print(patient["address"][0]["line"][0])

#print(add)
