import requests
import json

token = 'X1HV8NsHkGToowIULU6UUQGxSHr3UEaVmEEmVXzTBhgjTfZNH3E7yQcO2z85xy3QfYfehfmSr9JRt6AkqGcwlA'

call_header = {'accept':'application/json','Authorization': 'Bearer ' + token}

url = 'https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient/137'

response = requests.get(url, headers=call_header, verify=True)


r_dict = json.loads(response.text)

trakurl = (f"https://tcfhirsandbox.intersystems.com.au/t2019grxx/csp/system.Home.cls#/Direct/AW.Direct.EPR?RegistrationNo={str(r_dict['identifier'][1]['value'])}")
trak_name = (f"{r_dict['name'][0]['text']}")
trak_careProvider = (f"{r_dict['careProvider'][0]['display']}")
trak_recordNumber = (f"{r_dict['identifier'][1]['value']}")
trak_dob = (f"{r_dict['birthDate']}")
trak_gender = (f"{r_dict['gender']}")

print (f"Record Number : {trak_recordNumber}\n\t Name : {trak_name}\n\t  Sex : {trak_gender}\n\t  DOB : {trak_dob}\nCare Provider : {trak_careProvider}\n\nClick the button below to go to {trak_name} TrakCare profile")