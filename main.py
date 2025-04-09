from fastapi import FastAPI, Request, Response, HTTPException
from twilio.twiml.voice_response import VoiceResponse
import os
import openai
import datetime
from google.cloud import storage
app = FastAPI()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="path/to/your-service-account-file.json"
openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=openai_api_key)
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.api_route("/answer_call/", methods=["GET", "POST"])
async def answer_call():
    response = VoiceResponse()
    gather = response.gather(input='speech', action='/process_speech/', method='POST')
    gather.say("Hello, The code is working. How can I help you today?", voice='alice')
    # Redirect to the same endpoint if the user does not speak
    response.redirect('/answer_call/')
    return Response(content=str(response), media_type="application/xml")


# @app.post("/process_speech/")
@app.api_route("/process_speech/", methods=["GET", "POST"])
async def process_speech(request: Request):
    try:
        form_data = await request.form()
        speech_result = form_data.get('SpeechResult', '').strip()
        response = VoiceResponse()
        if speech_result:
            ai_text = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                      {"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": f"{speech_result}"},
                    ]
        )

            ai_text = ai_text.choices[0].message.content
            print("Response from openAI:", ai_text)
            with open("conversation_log.txt", "a") as file:
                file.write(f"User said: {speech_result}\nAI responded: {ai_text}\n\n")
            response.say(f"{ai_text}", voice='alice')
            gather = response.gather(input='speech', action='/process_speech/', method='POST')
            gather.say("Do you have another question?", voice='alice')

        else:
            response.say("I didn't catch that. Could you please repeat?", voice='alice')
            response.redirect('/answer_call/')

        return Response(content=str(response), media_type="application/xml")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.api_route("/completed", methods=["GET", "POST"])
async def completed(request: Request):
    form_data = await request.form()
    call_status = form_data.get("CallStatus")
    if call_status == "completed":
        try:
            print("Call completed. Processing the log file.")
            # Assume 'conversation_log.txt' contains the entire conversation to be saved
            current_datetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"TwilioFile_{current_datetime}.txt"
            upload_to_gcs('bucket_name', 'conversation_log.txt', filename)
        except Exception as e:
            print(f"Error during GCS upload: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return Response(status_code=200)
