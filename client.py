import socket
import json
import threading


HOST = '127.0.0.1'
PORT = 5000
ADDR = (HOST, PORT)
BUFFER_SIZE = 1024

class Client:
    def __init__(self, username):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(ADDR)
        self.username = username

    def join_room(self, room):
        message = json.dumps({"action": "join", "room": room, "username": self.username})
        self.client_socket.send(message.encode('utf-8'))

    def send_message(self, room, message):
        data = {"action": "message", "room": room, "username": self.username, "message": message}
        self.client_socket.send(json.dumps(data).encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
                if message:
                    print(message)
            except:
                break

if __name__ == "__main__":
    username = input("Enter your username: ")
    client = Client(username)

    room = input("Enter the room to join: ")
    client.join_room(room)

    threading.Thread(target=client.receive_messages).start()

    while True:
        message = input()
        client.send_message(room, message)
