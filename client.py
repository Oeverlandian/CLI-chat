import socketio
import sys
import threading
import time

sio = socketio.Client()

current_input = ""

@sio.on('message')
def on_message(data):
    global current_input

    full_message = f"--------------------------------\n{data['username']} | {data['timestamp']}\n{data['message']}\n--------------------------------"

    sys.stdout.write("\033[K")
    print(f"\r{full_message}")
    sys.stdout.write(f"Enter your message: {current_input}")
    sys.stdout.flush()

def send_message(username):
    global current_input

    while True:
        current_input = input("Enter your message: ")
        
        sio.send({'username': username, 'message': current_input})
        
        current_input = ""

def connect_to_server(server_address):
    try:
        if not server_address.startswith(('http://', 'https://')):
            server_address = 'http://' + server_address

        sio.connect(server_address)
        print("Connected to server!")
    except Exception as e:
        print(f"Failed to connect to server: {e}")

if __name__ == '__main__':
    server_address = input("Enter the server address (e.g., http://203.0.113.1:5000 or http://yourdomain.com:5000): ")
    connect_to_server(server_address)

    username = input("Enter your username: ")
    threading.Thread(target=send_message, args=(username,)).start()

    while True:
        time.sleep(1)
