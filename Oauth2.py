import requests
import subprocess
import sys
import json

token = 'QlBZMmXe3bo6rMw9a3f9wO1rVeg7jFnqgv5Q-tISbXUtZPemt_2H_4slcMb3aeizavaRGksg0IsRlF6vomv6pA'

call_header = {'accept':'application/json','Authorization': 'Bearer ' + token}

url = 'https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Practitioner/648'

response = requests.get(url, headers=call_header, verify=True)

print(response.text)
