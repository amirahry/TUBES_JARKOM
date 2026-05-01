import socket
import os

PORT = 5008

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    print("\n1. Kirim kata/kalimat/paragraf")
    print("2. Kirim file (simulasi broadcast)")
    print("3. Exit")

    choice = input("Pilih: ")

    # ================= TEXT =================
    if choice == "1":
        message = input("Masukkan pesan: ")
        sock.sendto(message.encode(), ('127.0.0.1', PORT))
        print("[SENDER] Pesan broadcast terkirim!")

    # ================= FILE =================
    elif choice == "2":
        filepath = input("Masukkan path file: ")

        if not os.path.exists(filepath):
            print("File tidak ditemukan!")
            continue

        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)

        # 🔥 kirim info file (bukan isi file)
        message = f"[FILE BROADCAST] {filename} ({filesize} bytes)"
        sock.sendto(message.encode(), ('127.0.0.1', PORT))

        print("[SENDER] Info file dibroadcast!")

    elif choice == "3":
        break

    else:
        print("Pilihan salah")