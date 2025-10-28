import socket
import threading
import sys
import os

SERVER_HOST = "127.0.0.1"  # Change if server is on another machine
SERVER_PORT = 5000         # Must match chat_server.py


def receive_messages(sock):
    """Background thread that continuously receives and prints messages."""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("Disconnected from server.")
                break
            print(data.decode("utf-8"), end="")
    except Exception as e:
        print(f"[ERROR receiving] {e}")
    finally:
        try:
            sock.close()
        except:
            pass
        os._exit(0)  # hard-exit entire client if receiver dies


def main():
    # 1. Create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Connect to server
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
    except Exception as e:
        print(f"Could not connect to server: {e}")
        sys.exit(1)

    # 3. Receive and show the server’s welcome banner before anything else
    try:
        initial_banner = sock.recv(1024).decode("utf-8")
        print(initial_banner, end="")
    except Exception as e:
        print(f"Error receiving welcome message: {e}")
        sock.close()
        sys.exit(1)

    # 4. Start the background receiver after showing the welcome banner
    recv_thread = threading.Thread(
        target=receive_messages,
        args=(sock,),
        daemon=True
    )
    recv_thread.start()

    # 5. Main send loop
    try:
        while True:
            user_input = input()
            if user_input.strip().lower() == "/quit":
                sock.sendall(user_input.encode("utf-8"))
                break
            sock.sendall(user_input.encode("utf-8"))
    except KeyboardInterrupt:
        try:
            sock.sendall("/quit".encode("utf-8"))
        except:
            pass
    finally:
        try:
            sock.close()
        except:
            pass
        sys.exit(0)


if __name__ == "__main__":
    main()
