import socket

HOST = "127.0.0.1"
PORT = 5000


def run():
    client = socket.socket()

    try:
        client.connect((HOST, PORT))

        print("1. Kata")
        print("2. Kalimat")
        print("3. Paragraf")

        choice = input("Pilih: ")

        if choice == "1":
            msg = input("Masukkan kata: ")
        elif choice == "2":
            msg = input("Masukkan kalimat: ")
        elif choice == "3":
            print("Masukkan paragraf, tekan Enter kosong untuk selesai:")
            lines = []

            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            msg = "\n".join(lines)
        else:
            print("Salah pilihan")
            return

        client.send(msg.encode())
        print("Pesan berhasil dikirim.")

    except ConnectionRefusedError:
        print("Gagal connect. Jalankan server dulu.")

    finally:
        client.close()
        input("Tekan Enter untuk kembali ke menu...")