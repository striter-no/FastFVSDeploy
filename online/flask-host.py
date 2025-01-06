from flask import Flask, request
from requests import get
import sys
import logging
import subprocess

def do(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"

def getLocalIP(interface="eth0"):
    raw = do(f"ip addr show {interface}" + " | grep 'inet ' | awk '{print $2}' | cut -d/ -f1")
    return raw.strip()

log = logging.getLogger('werkzeug')
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
log.disabled = True

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(f"POST request from {request.remote_addr} data: {request.json}")
        return f"POST request from {request.remote_addr} data: {request.json}", 200
    elif request.method == 'GET':
        print(f"GET request from {request.remote_addr}")
        return f"GET request from {request.remote_addr}", 200
    else:
        return "Invalid request method", 405

if __name__ == '__main__':

    myip = get('https://api.ipify.org').text
    globalport = 9000

    localip   = getLocalIP("wlxccb25504052f")
    localport = 9000

    print(f"Your local IP address is: {localip}")
    print(f"Your IP address is: {myip}")
    print(f"\nServer running on http://{localip}:{localport}")
    print(f"You can also access it via http://{myip}:{globalport}\n{'-'*15}\n")

    app.run(
        host=localip,
        port=localport
    )
