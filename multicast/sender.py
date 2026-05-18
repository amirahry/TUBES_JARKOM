import socket

MCAST_GRP = "224.1.1.1"
PORT = 5007


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        msg = input("Masukkan pesan multicast: ")
        sock.sendto(msg.encode(), (MCAST_GRP, PORT))
        print("[MULTICAST] Pesan terkirim.")

    finally:
        sock.close()
        input("Tekan Enter untuk kembali ke menu...")