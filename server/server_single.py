import socket
import os
import msvcrt

HOST = "127.0.0.1"
PORT = 5000


def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1)

    print("Server Single Thread Running...")
    print("Tekan Q untuk kembali ke menu.")

    try:
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode().lower()
                if key == "q":
                    print("\nServer dihentikan.")
                    break

            try:
                conn, addr = server.accept()
            except socket.timeout:
                continue

            print(f"[CONNECTED] {addr}")

            try:
                header = conn.recv(1024).decode()

                if "|" in header:
                    filename, filesize = header.split("|")
                    filesize = int(filesize)

                    os.makedirs("files/received", exist_ok=True)
                    filepath = os.path.join("files/received", filename)

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
                    conn.send(b"DONE")

                else:
                    print("[TEXT]", header)

            finally:
                conn.close()

    finally:
        server.close()
        input("Tekan Enter untuk kembali ke menu...")