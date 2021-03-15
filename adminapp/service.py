from google.oauth2 import service_account
import googleapiclient.discovery

SCOPES = ['https://www.googleapis.com/auth/cloud-identity.groups']
SERVICE_ACCOUNT_FILE = 'adminapp/serviceaccountkey.json'

def create_service():
  credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  delegated_credentials = credentials.with_subject('cognizance.amrita@gmail.com')

  service_name = 'cloudidentity.googleapis.com'
  api_version = 'v1'
  discovery_url = (
    'https://%s/$discovery/rest?version=%s' % (service_name, api_version))
  service = googleapiclient.discovery.build(
    service_name,
    api_version,
    discoveryServiceUrl=discovery_url,
    credentials=credentials)

  return service