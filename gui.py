import tkinter as tk
from tkinter import simpledialog, scrolledtext
import threading
import client

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(padx=20, pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        self.username = simpledialog.askstring("Username", "Enter your username:")
        self.room = simpledialog.askstring("Room", "Enter room name:")

        self.client = client.Client(self.username)
        self.client.join_room(self.room)

        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client.client_socket.recv(client.BUFFER_SIZE).decode('utf-8')
                if message:
                    self.chat_area.config(state=tk.NORMAL)
                    self.chat_area.insert(tk.END, message + "\n")
                    self.chat_area.config(state=tk.DISABLED)
                    self.chat_area.see(tk.END)
            except:
                break

    def send_message(self, event):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.client.send_message(self.room, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
