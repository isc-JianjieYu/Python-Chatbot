from rauth.service import OAuth2Service

# Get a real consumer key & secret from:
# https://github.com/settings/applications/new
sandbox = OAuth2Service(
    client_id='6A605kYem9GmG38Vo6TTzh8IFnjWHZWtRn46K1hoxQY',
    client_secret='POrisHrcdMvUKmaR6Cea0b8jtx-z4ewVWrnaIXASO-H3tB3g5MgPV7Vqty7OP8aEbSGENWRMkeVuJJKZDdG7Pw',
    name='sandbox',
    authorize_url='https://tcfhirsandbox.intersystems.com.au/oauth2/authorize',
    access_token_url='https://tcfhirsandbox.intersystems.com.au/oauth2/token',
    base_url='https://tcfhirsandbox.intersystems.com.au/oauth2')

print('Visit this URL in your browser: ' + sandbox.get_authorize_url())

# # This is a bit cumbersome, but you need to copy the code=something (just the
# # `something` part) out of the URL that's redirected to AFTER you login and
# # authorize the demo application
# code = raw_input('Enter code parameter (code=something) from URL: ')

# # create a dictionary for the data we'll post on the get_access_token request
#data = dict(code=code, redirect_uri='x-argonaut-app://HealthProviderLogin/')

# # retrieve the authenticated session
# session = github.get_auth_session(data=data)

# # make a request using the authenticated session
# user = session.get('user').json()

# print('currently logged in as: ' + user['login'])