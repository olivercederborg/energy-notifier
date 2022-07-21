import os
from twilio.rest import Client
from dotenv import load_dotenv
from scrape import main

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
from_number = os.environ["TWILIO_FROM_NUMBER"]
receivers = os.environ["SMS_RECEIVERS"].split(",")


def send_sms(number):
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=main(), from_=from_number, to=number)
    print(f"SID {message.sid} sent")


for receiver in receivers:
    send_sms(receiver)
