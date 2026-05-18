import socket
import struct
import msvcrt

MCAST_GRP = "224.1.1.1"
PORT = 5007


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    sock.settimeout(1)

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("[MULTICAST RECEIVER] Menunggu pesan...")
    print("Tekan Q untuk kembali ke menu.")

    try:
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode().lower()
                if key == "q":
                    print("\nReceiver dihentikan.")
                    break

            try:
                data, addr = sock.recvfrom(1024)
                print(f"[MULTICAST] dari {addr}: {data.decode()}")

            except socket.timeout:
                continue

    finally:
        sock.close()
        input("Tekan Enter untuk kembali ke menu...")