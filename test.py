import json

arryj = '[{"Name":"Jianjie Yu","Title":"Intern","Company":"InterSystems","Phone":"1321-123-5554","DOB":"1992-02-04"},{"Name":"Sachin Malik","Title":"Intern","Company":"InterSystems","Phone":"123-123-5554","DOB":"1995-06-14"},{"Name":"Harshitha Acha","Title":"Intern","Company":"InterSystems","Phone":"1343-123-5554","DOB":"1996-09-09"},{"Name":"Yuanhao Zheng","Title":"Intern","Company":"InterSystems","Phone":"123-123-5554","DOB":"2000-01-07"}]'
listPatient = json.loads(arryj)
printing = ""
for patient in listPatient:
    add = "Name: " + patient["Name"] + "\nTitle: " + patient["Title"] + "\nCompany: " + patient["Company"] + "\nPhone: " + patient["Phone"] + "\nDOB: " + patient["DOB"] + "\n\n"
    printing += add
print(printing)