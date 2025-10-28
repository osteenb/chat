# Python Multi-Client Chat Application

**Author:** Brooks O'Steen  
**Files:** chat_server.py and chat_client.py  
**Language:** Python 3

**Purpose:** Demonstrate a threaded TCP chat server and client capable of handling multiple users concurrently, complete with timestamps, usernames, and join/leave notifications.

## Overview
This project implements a multi-client chat system using Python sockets and threads.
It allows multiple clients to connect to a central server, exchange messages in real-time, and see who's online.
Each message is timestamped and labeled with the sender's username for clarity.

## Key Features
- Multi-user concurrent chat using threads.
- Timestamps on all messages.
- Usernames displayed with each message.
- Join/Leave notifications for all participants.
- Broadcast messaging to all connected clients (except the sender).
- Custom commands:
  - `/quit` — safely disconnect from the chat.
  - `/whosonline` — see a live list of connected users.

## How It Works
Open separate Terminals and run python scripts in same folder as files.
**Example:** `PS C:\Users\brook\GitHubChatSRVR\chatserver> python chat_server.py`

### 1. chat_server.py
The server:
- Listens on all network interfaces (0.0.0.0) at port 5000.
- Accepts incoming TCP client connections.
- Spawns a dedicated thread (handle_client) for each connected client.
- Tracks connected clients in a shared dictionary:
  ```python
  clients = {socket: username}
  ```
- Each message is prefixed with:
  ```
  [YYYY-MM-DD HH:MM:SS] username: message
  ```
- Broadcasts messages to all other users.
- Handles disconnects gracefully and notifies others when a user leaves.

### 2. chat_client.py
The client:
- Connects to the server's IP and port.
- Prompts for a username upon connection.
- Launches a background thread (receive_messages) to continuously listen for new messages.
- Runs a main send loop allowing the user to type and send messages.
- Displays all messages from other users, complete with timestamps and usernames.
- Supports `/quit` to exit cleanly.

## Example Usage

### Start the Server
```bash
python chat_server.py
```
Console output:
```
Starting chat server on 0.0.0.0:5000 ...
Server is running. Waiting for connections...
```

### Start Clients
```bash
python chat_client.py
```
Each user will see:
```
👋 Hello! You've logged into Brooks O'Steen Chat Server.
Please provide a username to join the chat:
----------------------------------------
> Brooks
[2025-10-27 21:45:03] Brooks has joined the chat.
```
Send messages directly:
```
Hello everyone!
/whosonline
/quit
```

## Data Flow Summary
```
[Client1] ----\
[Client2] -----\               ┌───────────────────────────┐
[Client3] -------> (Server) --->│ handle_client(threaded)  │
[Client4] -----/                │ broadcast() → all clients │
[Client5] ----/                 └───────────────────────────┘
```
Each client both sends and receives simultaneously through threads:
- The main loop handles sending user input.
- The background thread handles receiving and displaying messages.

## Possible Enhancements
- Add private messaging (`/pm username message`).
- Add message history.
- Implement GUI.
- Add encryption (SSL/TLS or Fernet) for secure chat.
- Display user join/leave notifications in a different color (with ANSI codes).

## Requirements
- Python 3.8+
- Works cross-platform (Windows, macOS, Linux)
- No external libraries required — uses standard socket, threading, datetime, and sys.
