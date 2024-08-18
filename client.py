import socketio
import sys
import threading
import time

# Create a Socket.IO client
sio = socketio.Client()

# Global variable to keep track of the current input
current_input = ""

# Function to handle incoming messages
@sio.on('message')
def on_message(data):
    global current_input

    # Clear the current input line
    sys.stdout.write("\033[K")
    
    # Print the incoming message
    print(f"\r{data}")
    
    # Reprint the input prompt and the current input
    sys.stdout.write(f"Enter your message: {current_input}")
    sys.stdout.flush()

# Function to handle sending messages
def send_message(username):
    global current_input

    while True:
        # Read the input from the user
        current_input = input("Enter your message: ")
        
        # Send the message to the server
        sio.send({'username': username, 'message': current_input})
        
        # Reset the current input after sending the message
        current_input = ""

# Connect to the server
def connect_to_server(server_address):
    try:
        # Check if the URL scheme is provided, if not, add http://
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

    # Keep the client alive to receive messages
    while True:
        time.sleep(1)
