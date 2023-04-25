import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import os
import pandas as pd
DIR = os.getcwd()



stats = {}

def write_to_file(stats):
    # stats = json.loads(str(stats))
    data = pd.DataFrame.from_dict(stats,orient="index")
    data = data.transpose()    
    column_sums = data.sum()
    data.loc['total'] = column_sums
    # data.to_excel('stats.xlsx')
    data = data.fillna('')
    # Convert the DataFrame to a formatted string
    data_string = data.to_string(index=True, header=True)

    # Write the string to a file
    with open('stats.txt', 'w') as f:
        f.write(data_string)
    

def proccess_log():
    log_file = f"{DIR}/log/server.log"
    with open(log_file, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("b"):
            client_id = line.strip()
           # print(client_id, lines[i + 1].strip()[1:27])
            # try:
            timestamp_str = lines[i+1].strip()[1:27]
            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            timestamp = str(timestamp)[0:10]
            # print(timestamp)
            try:
                stats[client_id][str(timestamp)] += 1
            except:
                try:
                    stats[client_id][str(timestamp)] = 1
                except:
                    stats[client_id] = {}
                    stats[client_id][str(timestamp)] = 1
    write_to_file(stats)

proccess_log()
