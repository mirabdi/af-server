import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import os

DIR = os.getcwd()

def update_variables(data):
    with open(f"{DIR}/variables.json", 'w') as f:
    # Write the JSON data to the file
        json.dump(data, f)


def get_variables():
    with open(f'{DIR}/variables.json', 'r') as f:
        json_data = json.load(f)
    return json_data


# Computer lists should be updated whenever new client is added (Client should also get new ID)
vars = get_variables()
client_ids = vars['client_ids']
# Computers that didn't connect in the last 1 hour
no_request = []

found = {}



def notify_users():
    vars = get_variables()
    last_email = vars['last_email']
    last_email = datetime.datetime.strptime(last_email, "%Y-%m-%d %H:%M:%S.%f")
    if datetime.datetime.now() - last_email < datetime.timedelta(days=1):
        return
    sender_email = "abdirasulov.main@gmail.com"
    # receiver_emails = ["kerekemesterge@gmail.com", "jmmcbride@protonmail.com"]
    receiver_emails = ["kerekemesterge@gmail.com"]
    password = "password_comes_here"

    subject = "Alphafold ERROR MESSAGES"
    
    body = f"Hi, \n \n The computers {no_request} didn't ask for new sequence in the last hour. You might want to check it. If the problem persists, I will send a new email in 24 hours. \n Not sincerely (cause I am just a script),\n AFserver bot "


    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)

    server.starttls()
    server.login(sender_email, password)
    for receiver_email in receiver_emails:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
    server.quit()
    
    vars['last_email'] = str(datetime.datetime.now())
    update_variables(vars)



def proccess_log():
    log_file = f"{DIR}/log/server.log"
    with open(log_file, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("b"):
            client_id = line.strip()
           # print(client_id, lines[i + 1].strip()[1:27])
            try:
                timestamp_str = lines[i+1].strip()[1:27]
                timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                if datetime.datetime.now() - timestamp <= datetime.timedelta(hours=1):
                    found[client_id] = str(timestamp)
                   # print(client_id)
            except:
                pass
    for client_id in client_ids:
        try:
            found[client_id]
        except:
            no_request.append(client_id)
    print(no_request)
    if len(no_request) != 0:
        notify_users()
        # print(no_request)
        # pas

proccess_log()
