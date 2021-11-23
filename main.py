import smtplib, ssl
from pandas import read_csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from markdown import markdown as md

data = read_csv("Participants.csv")
sender_email = input("Enter sender email:\n")
password = input("Type your password and press enter:\n")

receiver_email = data["email"].tolist()
username = data["Participant Name"].tolist()
receiver_count = len(receiver_email)

messages = [MIMEMultipart("alternative")]*receiver_count
subject = input("Please enter the subject of the mail:")
content = open("mail.md", "r").read()
html = md(content)

for i in range(len(messages)):
    messages[i]["Subject"] = subject
    messages[i]["From"] = "IEEE Computer Society, VIT"
    messages[i]["To"] = receiver_email[i%receiver_count]
    part = MIMEText(html.format(receiver=username[i]), "html")
    messages[i].attach(part)

for message in messages:
    print(message.as_string())

# Mailer block

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)

    for i in range(receiver_count):
        server.sendmail(
            sender_email, receiver_email[i], messages[i].as_string()
        )
