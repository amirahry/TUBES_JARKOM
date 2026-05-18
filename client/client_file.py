import socket
import os

HOST = "127.0.0.1"
PORT = 5000


def run():
    filepath = input("Masukkan path file: ")

    if not os.path.exists(filepath):
        print("File tidak ditemukan!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    client = socket.socket()

    try:
        client.connect((HOST, PORT))

        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)

        client.send(f"{filename}|{filesize}".encode())

        ready = client.recv(1024).decode()

        if ready != "READY":
            print("Server tidak siap")
            return

        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                client.sendall(chunk)

        print(client.recv(1024).decode())

    except ConnectionRefusedError:
        print("Gagal connect. Jalankan server dulu.")

    finally:
        client.close()
        input("Tekan Enter untuk kembali ke menu...")