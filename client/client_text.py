import socket

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket()
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
    print("Masukkan paragraf:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    msg = "\n".join(lines)
else:
    print("Salah pilihan")
    exit()

client.send(msg.encode())
client.close()