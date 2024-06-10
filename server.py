import socket
import threading
import json


HOST = '127.0.0.1'
PORT = 5000
ADDR = (HOST, PORT)
BUFFER_SIZE = 1024


clients = []
rooms = {}

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if message:
                handle_message(client_socket, message)
            else:
                remove_client(client_socket)
                break
        except:
            continue

def handle_message(client_socket, message):
    try:
        data = json.loads(message)
        action = data['action']
        
        if action == 'join':
            room = data['room']
            if room not in rooms:
                rooms[room] = []
            rooms[room].append(client_socket)
            broadcast(room, f"{data['username']} joined the room.", client_socket)
        elif action == 'message':
            room = data['room']
            broadcast(room, f"{data['username']}: {data['message']}", client_socket)
    except json.JSONDecodeError:
        pass

def broadcast(room, message, client_socket):
    for client in rooms.get(room, []):
        try:
            client.send(message.encode('utf-8'))
        except:
            remove_client(client)

def remove_client(client_socket):
    for room, clients in rooms.items():
        if client_socket in clients:
            clients.remove(client_socket)
            if not clients:
                del rooms[room]
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen()

    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
