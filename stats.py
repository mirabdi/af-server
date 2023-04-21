import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

stats = []
def proccess_stats(curr):
    log_file = "stats/stats.txt"
    with open(log_file, "r") as f:
        lines = f.readlines()

        
    for i, line in enumerate(lines):
        if line.startswith("b"):
            parts = line.strip()
            computer_id = parts[0]
            new_day = curr[computer_id]
            parts.append(new_day)
            new_line = ''.join(parts)+'\n'
            lines[i] = new_line


def proccess_log():
    log_file = "log/server.log"
    with open(log_file, "r") as f:
        lines = f.readlines()


        
    for i, line in enumerate(lines):
        if line.startswith("b"):
            parts = line.strip()
            computer_id = parts[0]
            log_file = "log/server.log"
    with open(log_file, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines[-1000:]):
        if line.startswith("b"):
            computer_id = line.strip()
            
            try:
                timestamp_str = lines[i+1].strip()[1:27]
                timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                if datetime.datetime.now() - timestamp <= datetime.timedelta(hours=1):
                    found[computer_id] = 1
                    # print(computer_id)
            except:
                pass
            new_day = curr[computer_id]
            parts.append(new_day)
            new_line = ''.join(parts)+'\n'
            lines[i] = new_line
            try:
                timestamp_str = lines[i+1].strip()[1:27]
                timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                if datetime.datetime.now() - timestamp <= datetime.timedelta(days=1):
                    days[computer_id] = 1
                    # print(computer_id)
            except:
                pass
    for computer_id in computer_ids:
        try:
            found[computer_id]
        except:
            no_request.append(computer_id)
    
    if len(no_request) != 0:
        notify_users()
        # print(no_request)
        # pass

proccess_log()