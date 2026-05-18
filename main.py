from server import server_single, server_multi
from client import client_text, client_file
from multicast import sender as multicast_sender
from multicast import receiver as multicast_receiver
from broadcast import sender as broadcast_sender
from broadcast import receiver as broadcast_receiver  # file kamu namanya reveiver.py

while True:
    print("\n=== MENU UTAMA ===")
    print("1. Jalankan Server Single Thread")
    print("2. Jalankan Server Multi Thread")
    print("3. Client Kirim Text")
    print("4. Client Kirim File")
    print("5. Multicast Sender")
    print("6. Multicast Receiver")
    print("7. Broadcast Sender")
    print("8. Broadcast Receiver")
    print("9. Exit")

    choice = input("Pilih: ")

    if choice == "1":
        server_single.run()
    elif choice == "2":
        server_multi.run()
    elif choice == "3":
        client_text.run()
    elif choice == "4":
        client_file.run()
    elif choice == "5":
        multicast_sender.run()
    elif choice == "6":
        multicast_receiver.run()
    elif choice == "7":
        broadcast_sender.run()
    elif choice == "8":
        broadcast_receiver.run()
    elif choice == "9":
        break
    else:
        print("Pilihan salah")