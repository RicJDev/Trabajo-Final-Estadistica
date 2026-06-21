import os
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from dotenv import load_dotenv

load_dotenv()

STUDENTS_FORM = os.getenv("STUDENTS_FORM", "")
GRADUATES_FORM = os.getenv("GRADUATES_FORM", "")

SCOPES = [
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/forms.body.readonly"
]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(
        "credentials.json", SCOPES, redirect_uri="http://localhost:8080/"
    )
    creds = tools.run_flow(flow, store)

service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)
