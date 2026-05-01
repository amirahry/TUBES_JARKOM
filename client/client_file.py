import socket
import os

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket()
client.connect((HOST, PORT))

filepath = input("Masukkan path file: ")

filename = os.path.basename(filepath)
filesize = os.path.getsize(filepath)

# kirim header
client.send(f"{filename}|{filesize}".encode())

# tunggu READY
ready = client.recv(1024).decode()

if ready != "READY":
    print("Server tidak siap")
    exit()

# kirim file
with open(filepath, "rb") as f:
    while True:
        chunk = f.read(4096)
        if not chunk:
            break
        client.sendall(chunk)

# tunggu DONE
print(client.recv(1024).decode())

client.close()