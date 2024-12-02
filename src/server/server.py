import socket
import threading
import time

# List to keep track of all connected clients
clients = dict()
next_seq = 1
end_string = "&&&&&&"


def handle_client(client_socket, port):
    global next_seq
    print(f"New connection from {port}: User{next_seq}")
    clients[client_socket] = next_seq
    threading.Thread(target=send_heartbeat_command, args=(client_socket,)).start()
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8").strip()
            if not message:
                break
            dispatch_command(message, client_socket)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client_socket.close()
        print("Client disconnected")
        broadcast_command(f"client_left/{clients[client_socket]}/?")
        clients.pop(client_socket)
        print(f"Connection closed: {port}")


def broadcast_command(message):
    for client in clients.keys():
        try:
            print("Sending message: ", message)
            client.sendall(f"{message}{end_string}".encode("utf-8"))
        except:
            pass


def dispatch_command(messages: str, client_socket) -> str:
    global next_seq
    for message in messages.split(end_string):
        if len(message.split("/")) != 3:
            continue
        cmd, client_seq, data = message.split("/")
        if cmd == "assign":
            assign_seq_command(client_socket)
            new_client_command()
            next_seq += 1
        elif cmd == "client_left":
            broadcast_command(message)
        else:
            chat_command(client_seq, data)


def assign_seq_command(client_socket) -> int:
    tmp = str(list(clients.values()))
    client_socket.sendall(
        (f"assign/{next_seq}/{tmp[1:-1]}" + end_string).encode("utf-8")
    )


def new_client_command() -> str:
    broadcast_command(f"new_client/{next_seq}/?")


def chat_command(client_seq: int, data: str) -> str:
    broadcast_command(f"message/{client_seq}/{data}")


def send_heartbeat_command(client_socket):
    while client_socket in clients:
        time.sleep(2)
        try:
            client_socket.sendall(("heartbeat/?/?" + end_string).encode("utf-8"))
        except:
            break


def create_server(port: int) -> tuple[str, int]:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))  # Use specfied port instead
    server_socket.listen(5)

    ip, port = server_socket.getsockname()
    print(f"Server created at {ip}:{port}")

    def accept_clients():
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(
                target=handle_client, args=(client_socket, addr[1])
            ).start()

    threading.Thread(target=accept_clients, daemon=True).start()
    return ip, port


if __name__ == "__main__":
    ip, port = create_server()
    print(f"Chat server running on {ip}:{port}")
    while True:
        pass
