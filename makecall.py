import os
from twilio.rest import Client

os.environ["TWILIO_AUTH_TOKEN"]=""
os.environ["TWILIO_ACCOUNT_SID"]=""
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to="",
    from_=""
)
print(call.sid)
