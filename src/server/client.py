import socket
import threading
import wx
import time

clients = dict()
my_seq = 0
end_string = "&&&&&&"
last_heartbeat = time.time()


def connect_to_server(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    return client_socket


def join_server(chat_display, client_socket, client_list, status_indicator):
    client_socket.sendall((f"assign/?/?" + end_string).encode("utf-8"))
    while not my_seq:
        execute_command(client_socket.recv(1024).decode("utf-8"), chat_display)

    def receive_messages():
        global last_heartbeat
        last_heartbeat = time.time()
        while last_heartbeat + 5 > time.time():
            try:
                command = client_socket.recv(1024).decode("utf-8")
                if not command:
                    break
                execute_command(command, chat_display)
                client_list.Set(list(clients.values()))
            except Exception as e:
                print(e)
                break
        chat_display.AppendText("Connection lost\n")
        status_indicator.Hide()

    threading.Thread(target=receive_messages, daemon=False).start()


def execute_command(commands: str, chat_display: wx.TextCtrl) -> str:
    global my_seq, last_heartbeat
    for command in commands.split(end_string):
        if len(command.split("/")) != 3:
            continue
        cmd, seq, data = command.split("/")
        if cmd == "assign":
            my_seq = seq
            clients[my_seq] = f"User{my_seq} (You)"
            for client in map(lambda x: x.strip(), data.split(",")):
                if client != my_seq:
                    clients[client] = f"User{client}"
        elif cmd == "new_client":
            if seq != my_seq:
                clients[seq] = f"User{seq}"
            wx.CallAfter(
                chat_display.AppendText, f"{clients[seq]} has joined the chat\n"
            )
        elif cmd == "message":
            wx.CallAfter(chat_display.AppendText, f"{clients[seq]}: {data}\n")
        elif cmd == "client_left":
            wx.CallAfter(chat_display.AppendText, f"{clients[seq]} has left the chat\n")
            clients.pop(seq)
        else:
            last_heartbeat = time.time()


def send_message(client_socket, message):
    client_socket.sendall(f"message/{my_seq}/{message}{end_string}".encode("utf-8"))


def send_left_message(client_socket):
    print("Sending left message")
    client_socket.sendall(f"client_left/{my_seq}/?{end_string}".encode("utf-8"))
