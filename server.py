from flask import Flask, render_template
from flask_socketio import SocketIO, send
from datetime import datetime
import socket

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('experiments.html')

@socketio.on('message')
@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    raw_data = {'username': username, 'message': message, 'timestamp': timestamp}

    print(f"Received message from {username} at {timestamp}: {message}")

    # Send the raw data to all clients
    send(raw_data, broadcast=True)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        local_ip = 'Unable to determine local IP'
    finally:
        s.close()
    return local_ip

if __name__ == '__main__':
    local_ip = get_local_ip()
    print(f"Server is running on: {local_ip}:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
