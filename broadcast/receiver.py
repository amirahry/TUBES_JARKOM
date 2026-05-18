import socket
import msvcrt

PORT = 5008


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", PORT))
    sock.settimeout(1)

    print("[RECEIVER] Menunggu broadcast...")
    print("Tekan Q untuk kembali ke menu.")

    try:
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode().lower()
                if key == "q":
                    print("\nReceiver dihentikan.")
                    break

            try:
                data, addr = sock.recvfrom(4096)
                message = data.decode()

                if "[FILE BROADCAST]" in message:
                    print(f"[FILE INFO] dari {addr}: {message}")
                else:
                    print(f"[TEXT] dari {addr}: {message}")

            except socket.timeout:
                continue

    finally:
        sock.close()
        input("Tekan Enter untuk kembali ke menu...")