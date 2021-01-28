from requests_oauthlib import OAuth2Session

client_id = "6A605kYem9GmG38Vo6TTzh8IFnjWHZWtRn46K1hoxQY"
client_secret = "POrisHrcdMvUKmaR6Cea0b8jtx-z4ewVWrnaIXASO-H3tB3g5MgPV7Vqty7OP8aEbSGENWRMkeVuJJKZDdG7Pw"
redirect_uri = 'x-argonaut-app://HealthProviderLogin/'

authorization_base_url = "https://tcfhirsandbox.intersystems.com.au/oauth2/authorize"
token_url = "https://tcfhirsandbox.intersystems.com.au/oauth2/token"
refresh_url = token_url # True for Google but not all providers.
scope = [
    'patient/*.read',
    'launch/patient',
]
trak = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
authorization_url, state = trak.authorization_url(authorization_base_url, state='asdasdasdasdasdasasd')
print(f'Please go to {authorization_url} and authorize access.')
authorization_response = input('Enter the whole callback url: ')

token = trak.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=authorization_response)


print(token)