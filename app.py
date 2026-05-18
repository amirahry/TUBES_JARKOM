from flask import Flask, render_template, request, redirect, url_for
import socket
import threading
import os
import struct
from datetime import datetime

app = Flask(__name__)

TCP_HOST = "127.0.0.1"
TCP_PORT = 5000

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5007

BCAST_PORT = 5008

UPLOAD_FOLDER = "files/send"
RECEIVED_FOLDER = "files/received"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RECEIVED_FOLDER, exist_ok=True)

logs = []

tcp_server_running = False
tcp_stop_event = threading.Event()

broadcast_receiver_running = False
broadcast_stop_event = threading.Event()

multicast_receiver_running = False
multicast_stop_event = threading.Event()


def add_log(message):
    time = datetime.now().strftime("%H:%M:%S")
    logs.insert(0, f"[{time}] {message}")
    if len(logs) > 50:
        logs.pop()


def handle_tcp_client(conn, addr):
    try:
        header = conn.recv(1024).decode()

        if "|" in header:
            filename, filesize = header.split("|")
            filesize = int(filesize)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(RECEIVED_FOLDER, unique_filename)

            conn.send(b"READY")

            with open(filepath, "wb") as f:
                received = 0
                while received < filesize:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            conn.send(b"DONE")
            add_log(f"TCP file diterima dari {addr}: {unique_filename}")

        else:
            add_log(f"TCP text dari {addr}: {header}")

    except Exception as e:
        add_log(f"TCP error: {e}")

    finally:
        conn.close()


def tcp_server_loop():
    global tcp_server_running

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((TCP_HOST, TCP_PORT))
        server.listen()
        server.settimeout(1)

        tcp_server_running = True
        add_log("TCP Server started")

        while not tcp_stop_event.is_set():
            try:
                conn, addr = server.accept()
                thread = threading.Thread(target=handle_tcp_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except socket.timeout:
                continue

    except Exception as e:
        add_log(f"TCP Server error: {e}")

    finally:
        tcp_server_running = False
        server.close()
        add_log("TCP Server stopped")


def broadcast_receiver_loop():
    global broadcast_receiver_running

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind(("", BCAST_PORT))
        sock.settimeout(1)

        broadcast_receiver_running = True
        add_log("Broadcast Receiver started")

        while not broadcast_stop_event.is_set():
            try:
                data, addr = sock.recvfrom(4096)
                add_log(f"Broadcast dari {addr}: {data.decode()}")
            except socket.timeout:
                continue

    except Exception as e:
        add_log(f"Broadcast Receiver error: {e}")

    finally:
        broadcast_receiver_running = False
        sock.close()
        add_log("Broadcast Receiver stopped")


def multicast_receiver_loop():
    global multicast_receiver_running

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.bind(("", MCAST_PORT))
        sock.settimeout(1)

        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        multicast_receiver_running = True
        add_log("Multicast Receiver started")

        while not multicast_stop_event.is_set():
            try:
                data, addr = sock.recvfrom(4096)
                add_log(f"Multicast dari {addr}: {data.decode()}")
            except socket.timeout:
                continue

    except Exception as e:
        add_log(f"Multicast Receiver error: {e}")

    finally:
        multicast_receiver_running = False
        sock.close()
        add_log("Multicast Receiver stopped")


@app.route("/")
def index():
    return render_template(
        "index.html",
        logs=logs,
        tcp_server_running=tcp_server_running,
        broadcast_receiver_running=broadcast_receiver_running,
        multicast_receiver_running=multicast_receiver_running
    )


@app.route("/start-tcp-server", methods=["POST"])
def start_tcp_server():
    if not tcp_server_running:
        tcp_stop_event.clear()
        thread = threading.Thread(target=tcp_server_loop)
        thread.daemon = True
        thread.start()
    else:
        add_log("TCP Server sudah berjalan")

    return redirect(url_for("index"))


@app.route("/stop-tcp-server", methods=["POST"])
def stop_tcp_server():
    tcp_stop_event.set()
    return redirect(url_for("index"))


@app.route("/send-tcp-text", methods=["POST"])
def send_tcp_text():
    message = request.form["message"]

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((TCP_HOST, TCP_PORT))
        client.send(message.encode())
        client.close()

        add_log(f"TCP text dikirim: {message}")

    except Exception as e:
        add_log(f"Gagal kirim TCP text: {e}")

    return redirect(url_for("index"))


@app.route("/send-tcp-file", methods=["POST"])
def send_tcp_file():
    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        add_log("File belum dipilih")
        return redirect(url_for("index"))

    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(filepath)

    try:
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((TCP_HOST, TCP_PORT))

        client.send(f"{filename}|{filesize}".encode())

        ready = client.recv(1024).decode()

        if ready == "READY":
            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    client.sendall(chunk)

            response = client.recv(1024).decode()
            add_log(f"TCP file dikirim: {filename} - {response}")
        else:
            add_log("Server tidak siap menerima file")

        client.close()

    except Exception as e:
        add_log(f"Gagal kirim TCP file: {e}")

    return redirect(url_for("index"))


@app.route("/start-broadcast-receiver", methods=["POST"])
def start_broadcast_receiver():
    if not broadcast_receiver_running:
        broadcast_stop_event.clear()
        thread = threading.Thread(target=broadcast_receiver_loop)
        thread.daemon = True
        thread.start()
    else:
        add_log("Broadcast Receiver sudah berjalan")

    return redirect(url_for("index"))


@app.route("/stop-broadcast-receiver", methods=["POST"])
def stop_broadcast_receiver():
    broadcast_stop_event.set()
    return redirect(url_for("index"))


@app.route("/send-broadcast", methods=["POST"])
def send_broadcast():
    message = request.form["message"]

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(message.encode(), ("127.0.0.1", BCAST_PORT))
        sock.close()

        add_log(f"Broadcast dikirim: {message}")

    except Exception as e:
        add_log(f"Gagal kirim broadcast: {e}")

    return redirect(url_for("index"))


@app.route("/start-multicast-receiver", methods=["POST"])
def start_multicast_receiver():
    if not multicast_receiver_running:
        multicast_stop_event.clear()
        thread = threading.Thread(target=multicast_receiver_loop)
        thread.daemon = True
        thread.start()
    else:
        add_log("Multicast Receiver sudah berjalan")

    return redirect(url_for("index"))


@app.route("/stop-multicast-receiver", methods=["POST"])
def stop_multicast_receiver():
    multicast_stop_event.set()
    return redirect(url_for("index"))


@app.route("/send-multicast", methods=["POST"])
def send_multicast():
    message = request.form["message"]

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))
        sock.close()

        add_log(f"Multicast dikirim: {message}")

    except Exception as e:
        add_log(f"Gagal kirim multicast: {e}")

    return redirect(url_for("index"))


@app.route("/clear-logs", methods=["POST"])
def clear_logs():
    logs.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)