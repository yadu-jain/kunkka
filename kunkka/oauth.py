import httplib2

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

# List the scopes your app requires:
flow=None
auth_uri=None
CLIENT_ID=None #"839932794527-178uqshpfnc7al8ecc5gdml5gopffb8q.apps.googleusercontent.com"
CLIENT_SECRET=None #"Fiw6f5q_5ZxHC3rvd0HQ4ao7"
REDIRECT_URI=None#"http://localhost:8080/login/"
SCOPES = None#['https://www.googleapis.com/auth/plus.me','email']
def init_oauth():
  global flow
  global auth_uri
  

  # The following redirect URI causes Google to return a code to the user's
  # browser that they then manually provide to your app to complete the
  # OAuth flow.
  #REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

  # For a breakdown of OAuth for Python, see
  # https://developers.google.com/api-client-library/python/guide/aaa_oauth
  # CLIENT_ID and CLIENT_SECRET come from your APIs Console project
  
  flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                             client_secret=CLIENT_SECRET,
                             scope=SCOPES,
                             redirect_uri=REDIRECT_URI,
                             access_type='online')

  auth_uri = flow.step1_get_authorize_url()

  # This command-line server-side flow example requires the user to open the
  # authentication URL in their browser to complete the process. In most
  # cases, your app will use a browser-based server-side flow and your
  # user will not need to copy and paste the authorization code. In this
  # type of app, you would be able to skip the next 3 lines.
  # You can also look at the client-side and one-time-code flows for other
  # options at https://developers.google.com/+/web/signin/
  print 'OAuth'  
  auth_uri+='&hd=travelyaari.com'
  print auth_uri
def get_service(code):
  try:    
    # Set authorized credentials
    global flow
    credentials = flow.step2_exchange(code)
    print "started"
    # Create a new authorized API client.
    http = httplib2.Http()
    http.disable_ssl_certificate_validation = True
    credentials = flow.step2_exchange(code, http)
    print credentials
    http = credentials.authorize(http)
    print http
    service = build('plusDomains', 'v1', http=http)  
    print service
    print "Done"
    return service
  except Exception as e:
    print e
    return None