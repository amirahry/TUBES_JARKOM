import os

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
        os.system("python server/server_single.py")
    elif choice == "2":
        os.system("python server/server_multi.py")
    elif choice == "3":
        os.system("python client/client_text.py")
    elif choice == "4":
        os.system("python client/client_file.py")
    elif choice == "5":
        os.system("python multicast/sender.py")
    elif choice == "6":
        os.system("python multicast/receiver.py")
    elif choice == "7":
        os.system("python broadcast/sender.py")
    elif choice == "8":
        os.system("python broadcast/receiver.py")
    elif choice == "9":
        break
    else:
        print("Pilihan salah")