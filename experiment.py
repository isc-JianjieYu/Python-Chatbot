import requests
from requests_oauthlib import OAuth2Session
"""
client_id = "6A605kYem9GmG38Vo6TTzh8IFnjWHZWtRn46K1hoxQY"
client_secret = "POrisHrcdMvUKmaR6Cea0b8jtx-z4ewVWrnaIXASO-H3tB3g5MgPV7Vqty7OP8aEbSGENWRMkeVuJJKZDdG7Pw"
redirect_uri = 'https://x-argonaut-app://HealthProviderLogin/'

#authori = "https://tcfhirsandbox.intersystems.com.au/oauth2/authorize"
#ACCESS_TOKEN_URL = "https://tcfhirsandbox.intersystems.com.au/oauth2/token"


#requests.get('{}?response_type=code&client_id={}&redirect_uri={}'.format(AUTHORIZE_URL, CLIENT_ID, REDIRECT_URI))
scope = ["patient/*.read launch/patient"]

oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

authorization_url, state = oauth.authorization_url(
        'https://tcfhirsandbox.intersystems.com.au/oauth2/authorize',
        # access_type and prompt are Google specific extra
        # parameters.
        grant_type="Authorization code", state="asdasdasdasdasdasasd")

print ('Please go to %s and authorize access.' % authorization_url)

authorization_response = raw_input('x-argonaut-app://HealthProviderLogin/')

token = oauth.fetch_token('https://tcfhirsandbox.intersystems.com.au/oauth2/token', authorization_response=authorization_response, client_secret=client_secret)

token = {
            'token_name' : 'sandbox',
            'access_token': 'reCvr6spwj8YNkIll-sPJH--eadHOaT0hBMBhVRvnRHdiG3E_zdankL89cc5lv1U-fo-jSnw9l1CkXCHfbQxZw',
            'refresh_token': '8nlWpdDv4cvmjLoIrw1XHzAScYZDI9WBtAnvFqwnVSc',
            'token_type': 'Bearer',
            'expires_in': '3600',
            'scope' : 'launch/patient patient/*.read',
            'patient' : '97'
        }"""

token = "reCvr6spwj8YNkIll-sPJH--eadHOaT0hBMBhVRvnRHdiG3E_zdankL89cc5lv1U-fo-jSnw9l1CkXCHfbQxZw"

#url = 'https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Practitioner/648'
response = requests.get('https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Practitioner/648', headers = {'Authorization':'Bearer' + token} )

print(response)