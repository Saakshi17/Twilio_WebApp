# Twilio_WebApp

The Twilio WebApp, allows the user to receive calls to a Twilio phone number. THe user can ask general FAQs to openAI's chatbot, GPT3.5 using the AI assisted voice chatbot. The conversation is logged and stored in Google Cloud Storage. 

FastAPI is used to create the Twilio Application. 
# Steps to Run 
Create an environment using requirements.txt

Configure the Twilio account and Auth Token to receive calls on personal number from Twilio phone number, to check if the account is authenticated in the makecall.py

You will need to configure your Twilio phone number to send a webhook to a specific endpoint when a call comes in. It could be something as  "https://123.ngrok-free.app/answer_call" .This can be done in the Twilio console where you set the voice URL configurations for your phone number.

Refer https://www.twilio.com/docs/voice/quickstart/python for initial setup for receving calls. 

In main.py fill in the GCP bucketname, path_to_json for GCP etc to run the main file. 

Use "uvicorn main:app --reload" in terminal to start the app. 
Use "ngrok http YourPortNumber" in terminal to start ngrok 

