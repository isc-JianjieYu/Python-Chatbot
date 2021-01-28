import requests, json
import webbrowser
from requests_oauthlib import OAuth2Session

authorize_url = "https://tcfhirsandbox.intersystems.com.au/oauth2/authorize"
token_url = "https://tcfhirsandbox.intersystems.com.au/oauth2/token"
state = 'asdasdasdasdasdasasd'
scope = 'patient%2F*.read%20launch%2Fpatient'#patient/*.read launch/patient'
callback_uri = "x-argonaut-app://HealthProviderLogin/"
test_api_url = "https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient?identifier=RN000000200"
client_id = '6A605kYem9GmG38Vo6TTzh8IFnjWHZWtRn46K1hoxQY'
client_secret = 'POrisHrcdMvUKmaR6Cea0b8jtx-z4ewVWrnaIXASO-H3tB3g5MgPV7Vqty7OP8aEbSGENWRMkeVuJJKZDdG7Pw'
#username = 'superuser'
#password = 'SYS'
OAuth_url = authorize_url + '?response_type=code&state=' + state + '&client_id=' + client_id + '&scope='+scope+'&redirect_uri=' + callback_uri

#fullcallback = requests.get(OAuth_url)
#print(fullcallback.url)
webbrowser.open(OAuth_url)
authorization_code = input("Enter the auth code: ")
 
data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
access_token_response = requests.post(token_url, data=data, verify=True, allow_redirects=True, auth=(client_id, client_secret))
print(access_token_response.status_code)
tokens = json.loads(access_token_response.text)
access_token = tokens['access_token']
refresh_token = tokens['refresh_token']
print(tokens)

# token = {
#     'access_token': tokens['access_token'],
#     'refresh_token': tokens['refresh_token'],
#     'token_type': 'Bearer',
#     'expires_in': tokens['expires_in'],     
#     }
# refresh_url = 'https://tcfhirsandbox.intersystems.com.au/oauth2/token'
# protected_url = 'https://tcfhirsandbox.intersystems.com.au/oauth2/secret'

# # most providers will ask you for extra credentials to be passed along
# # when refreshing tokens, usually for authentication purposes.
# extra = {
#     'client_id': client_id,
#     'client_secret': client_secret,
# }

# def token_saver(tok):
#     print("refreshed: " + tok)

# client = OAuth2Session(client_id, token=token, auto_refresh_url=refresh_url, auto_refresh_kwargs=extra, token_updater=token_saver)
# r = client.get(protected_url)