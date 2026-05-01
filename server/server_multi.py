import socket
import threading
import os
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server Multi Thread Running...")

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    try:
        header = conn.recv(1024).decode()

        # ================= FILE =================
        if "|" in header:
            filename, filesize = header.split("|")
            filesize = int(filesize)

            # 🔥 pastikan folder ada
            os.makedirs("files/received", exist_ok=True)

            # 🔥 buat nama file unik (timestamp + port)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{timestamp}_{addr[1]}_{filename}"

            filepath = os.path.join("files/received", unique_filename)

            # 🔥 kasih sinyal siap
            conn.send(b"READY")

            with open(filepath, "wb") as f:
                received = 0
                while received < filesize:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            print(f"[SUCCESS] {unique_filename} diterima ({filesize} bytes)")

            conn.send(b"DONE")

        # ================= TEXT =================
        else:
            print(f"[TEXT] {addr}: {header}")

    except Exception as e:
        print("[ERROR]", e)

    finally:
        conn.close()


while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()