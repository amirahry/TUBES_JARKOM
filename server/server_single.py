import socket
import os

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server Single Thread Running...")

conn, addr = server.accept()
print(f"[CONNECTED] {addr}")

try:
    header = conn.recv(1024).decode()

    # ================= FILE =================
    if "|" in header:
        filename, filesize = header.split("|")
        filesize = int(filesize)

        os.makedirs("files/received", exist_ok=True)
        filepath = os.path.join("files/received", filename)

        # 🔥 kirim READY
        conn.send(b"READY")

        with open(filepath, "wb") as f:
            received = 0
            while received < filesize:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)

        print(f"[SUCCESS] File {filename} diterima!")

        # 🔥 kirim DONE
        conn.send(b"DONE")

    # ================= TEXT =================
    else:
        print("[TEXT]", header)

finally:
    conn.close()
    server.close()