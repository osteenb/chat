import socket
import threading
import datetime

HOST = "0.0.0.0"   # Listen on all interfaces
PORT = 5000        # Must match the client

# Dictionary to track connected clients: {socket: username}
clients = {}


def timestamp():
    """Return current time formatted like [YYYY-MM-DD HH:MM:SS]."""
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def broadcast(message):
    """
    Send a message to ALL connected clients, including the sender.
    If any client is dead/broken, remove it.
    """
    for client_socket in list(clients.keys()):
        try:
            client_socket.sendall(message.encode("utf-8"))
        except Exception:
            # If sending fails, drop that client so it doesn't break future sends
            try:
                client_socket.close()
            except:
                pass
            # Safely remove from clients dict
            if client_socket in clients:
                del clients[client_socket]


def handle_client(client_socket, addr):
    try:
        # 1. Send welcome banner and ask for username
        welcome_message = (
            "\n----------------------------------------\n"
            "👋 Hello! You've logged into Brooks O'Steen Chat Server.\n"
            "/quit to leave chat.../whosonline to see who is online.\n"
            "Please provide a username to join the chat:\n"
            "----------------------------------------\n> "
        )
        client_socket.sendall(welcome_message.encode("utf-8"))

        username = client_socket.recv(1024).decode("utf-8").strip()

        # Fallback username if they just hit Enter
        if not username:
            username = f"{addr[0]}:{addr[1]}"

        # Store this client
        clients[client_socket] = username

        # Announce join to everyone (including this user)
        join_msg = f"{timestamp()} {username} has joined the chat.\n"
        print(join_msg.strip())
        broadcast(join_msg)

        # 2. Chat receive loop for this client
        while True:
            data = client_socket.recv(1024)

            # If no data, client disconnected (closed socket)
            if not data:
                break

            text = data.decode("utf-8").strip()

            # Allow client to leave with /quit
            if text.lower() == "/quit":
                break
          
          #CODE added to list online users 
            if text.lower() == "/whosonline":
                online = ", ".join(clients.values())
                client_socket.sendall(f"Online users: {online}\n".encode("utf-8"))
                continue
        #CODE added to list online users-delete above line if error occurs

            # Format outgoing message with timestamp + username
            out_msg = f"{timestamp()} {username}: {text}\n"
            print(out_msg.strip())  # show in server console
            broadcast(out_msg)

    except Exception as e:
        print(f"Error with client {addr}: {e}")

    finally:
        # Handle cleanup when the client leaves
        if client_socket in clients:
            left_username = clients[client_socket]
            leave_msg = f"{timestamp()} {left_username} has left the chat.\n"
            print(leave_msg.strip())

            # Remove from active list
            del clients[client_socket]

            # Tell everyone they left
            broadcast(leave_msg)

        # Close socket safely
        try:
            client_socket.close()
        except:
            pass


def main():
    print(f"Starting chat server on {HOST}:{PORT} ...")

    # Create server TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow quick restart without "Address already in use"
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind and listen
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server is running. Waiting for connections...")

    # Accept loop
    while True:
        client_socket, addr = server_socket.accept()
        print(f"{timestamp()} Connection from {addr}")

        # Spin up a thread for this new client
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, addr),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    main()
