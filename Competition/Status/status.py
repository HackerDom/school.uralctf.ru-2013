#!/usr/bin/python
__author__ = 'Maxim Muzafarov'
from flask import Flask
from flup.server.fcgi import WSGIServer
import requests
import os
import paramiko
import poplib


app = Flask(__name__)


@app.route('/status/')
def index():
    host = "school.uralctf.ru"
    services = ['QServer', 'MEM', 'DISK', 'CPU',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                'Promo']

    def status(service):
        try:
            if service == "QServer":
                r = requests.get("http://{0}/qserver/".format(host))
                if r.status_code == 200:
                    return 0
                return 1
            elif service == "Promo":
                r = requests.get("http://{0}/".format(host))
                if r.status_code == 200:
                    return 0
                return 1
            elif service == "A":
                client = paramiko.SSHClient()
                try:
                    user = "labirint"
                    password = "welcomE"
                    port = 22

                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(hostname=host, username=user, password=password, port=port)
                    stdin, stdout, stderr = client.exec_command('ls enter')
                    data = stdout.read() + stderr.read()
                    if "forward" in data:
                        retval = 0
                    else:
                        retval = 2
                except:
                    retval = 1
                client.close()
                return retval
            elif service == "B":
                link = "http://school.uralctf.ru/static/quest/task2"
                r = requests.head(link)
                if r.status_code == 200:
                    return 0
                elif r.status_code == 404:
                    return 1
                return 2
            elif service == "C":
                r = requests.get("http://pop-server.tk/".format(host), auth=('C','Pfrhsnj'))
                if r.status_code == 200:
                    return 0
                elif r.status_code == 502:
                    return 1
                elif r.status_code == 401:
                    return 3
                return 2
            elif service == "D":
                link = "http://{}/static/quest/floppy.img".format(host)
                r = requests.head(link)
                if r.status_code == 200:
                    return 0
                elif r.status_code == 404:
                    return 1
                return 2
            elif service == "E":
                link = "http://school.uralctf.ru/static/quest/wallpaper.bmp"
                r = requests.head(link)
                if r.status_code == 200:
                    return 0
                elif r.status_code == 404:
                    return 1
                return 2
            elif service == "F":
                link1 = "http://school.uralctf.ru/static/quest/whosaidthat.zip"
                link2 = "http://school.uralctf.ru/static/quest/Question.jpg"
                r1 = requests.head(link1)
                r2 = requests.head(link2)
                if r1.status_code == 200 and r2.status_code == 200:
                    return 0
                elif r1.status_code == 404 or r2.status_code == 404:
                    return 1
                return 2
            elif service == "G":
                link = "http://school.uralctf.ru/static/quest/bro.jpg"
                r = requests.head(link)
                if r.status_code == 200:
                    return 0
                elif r.status_code == 404:
                    return 1
                return 2
            elif service == "H":
                user = "abuse"
                password = "5315725"
                try:
                    Mailbox = poplib.POP3('school.uralctf.ru', '110', 5)
                except:
                    return 1
                try:
                    Mailbox.user(user)
                    Mailbox.pass_(password)
                    if Mailbox.stat():
                        retval = 0
                    else:
                        retval = 2
                except:
                    retval = 2
                Mailbox.quit()
                return retval
            elif service == "I":
                client = paramiko.SSHClient()
                try:
                    user = "anomaly"
                    password = "whatsthehell"
                    port = 22

                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(hostname=host, username=user, password=password, port=port)
                    stdin, stdout, stderr = client.exec_command('ls')
                    data = stdout.read() + stderr.read()
                    if "secure.log" in data:
                        retval = 0
                    else:
                        retval = 2
                except:
                    retval = 1
                client.close()
                return retval
            elif service == "J":
                link = "http://school.uralctf.ru/static/quest/passwords.docx"
                r = requests.head(link)
                if r.status_code == 200:
                    return 0
                elif r.status_code == 404:
                    return 1
                return 2
            elif service == "MEM":
                freeMemory = int(os.popen("free -m").readlines()[1].split()[3])
                if freeMemory > 700:
                    return 0
                elif freeMemory > 400:
                    return 2
                else:
                    return 1
            elif service == "DISK":
                freeDisk = int(os.popen("df").readlines()[1].split()[3]) / 1024
                if freeDisk > 5000:
                    return 0
                elif freeDisk > 3000:
                    return 2
                else:
                    return 1
            elif service == "CPU":
                cpuUse = float(str(os.popen("top -b -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip().split('%')[0]))
                if cpuUse > 80:
                    return 1
                elif cpuUse > 50:
                    return 2
                return 0
        except:
            return 255

    def cell(flag):
        if flag == 0:
            return '<td style="background: #44ff44;" title=0>OK</td>'
        elif flag == 1:
            return '<td style="background: #ff4444;" title=1>FAIL</td>'
        else:
            return '<td style="background: orange;" title={}>WRONG</td>'.format(flag)

    response = '''
            <!DOCTYPE HTML>
            <html><head>
            <META HTTP-EQUIV="refresh" CONTENT="300">
            <title>Status of services</title>
            <style type="text/css">
                TABLE,TD,TH {
                    margin-bottom: 10px;
                    border: 1px solid black;
                    border-collapse: collapse;
                    font-family: arial;
                    font-size: 16pt;
                }
                TD,TH {
                    padding: 5px;
                }
            </style>
            </head>
            <body>
            <h1>Status of services</h1>
            <table><tr>
            '''

    for service in services:
        response += "<th>{}</th>".format(service)
    response += "</tr>\n<tr>"
    for service in services:
        response += "{}".format(cell(status(service)))
    response += "</tr>\n</table></body>"
    return response


if __name__ == '__main__':
    WSGIServer(app).run()
