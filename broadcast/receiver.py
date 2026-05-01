import socket

PORT = 5008

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('', PORT))

print("[RECEIVER] Menunggu broadcast...")

while True:
    data, addr = sock.recvfrom(4096)
    message = data.decode()

    if "[FILE BROADCAST]" in message:
        print(f"[FILE INFO] dari {addr}: {message}")
    else:
        print(f"[TEXT] dari {addr}: {message}")