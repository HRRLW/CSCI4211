import socket
import threading

# Global dictionary to manage topics, subscribers, and stored messages
subscriptions = {
    "WEATHER": {"clients": [], "messages": []},
    "NEWS": {"clients": [], "messages": []}
}

# Function to handle each connected client
def handle_client(client_socket, client_address):
    print(f"[INFO] Connected to {client_address}")
    try:
        while True:
            # Receive a message from the client
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            
            print(f"[MESSAGE from {client_address}]: {message}")
            
            # Parse the message format
            parts = message.strip("<>").split(", ")
            if len(parts) < 2:
                client_socket.sendall(b"<ERROR: Invalid Message Format>")
                continue
            
            command = parts[1]
            
            # Handle CONNECT
            if command == "CONN":
                client_socket.sendall(b"<CONN_ACK>")

            # Handle SUBSCRIBE
            elif command == "SUB":
                if len(parts) < 3:
                    client_socket.sendall(b"<ERROR: Missing Subject>")
                    continue
                subject = parts[2]
                if subject not in subscriptions:
                    client_socket.sendall(b"<ERROR: Subscription Failed - Subject Not Found>")
                else:
                    subscriptions[subject]["clients"].append(client_socket)
                    client_socket.sendall(b"<SUB_ACK>")
                    print(f"[INFO] {client_address} subscribed to {subject}")
                    # Deliver stored messages to the subscriber
                    if subscriptions[subject]["messages"]:
                        for stored_message in subscriptions[subject]["messages"]:
                            formatted_message = f"Topic: {subject}, Message: {stored_message}"
                            try:
                                client_socket.sendall(formatted_message.encode("utf-8"))
                            except Exception as e:
                                print(f"[ERROR] Failed to send stored message: {e}")
            
            # Handle PUBLISH
            elif command == "PUB":
                if len(parts) < 4:
                    client_socket.sendall(b"<ERROR: Missing Message>")
                    continue
                subject = parts[2]
                msg_content = parts[3]
                if subject not in subscriptions:
                    client_socket.sendall(b"<ERROR: Subject Not Found>")
                else:
                    # Store the message and forward it to online subscribers
                    subscriptions[subject]["messages"].append(msg_content)
                    for subscriber in subscriptions[subject]["clients"]:
                        try:
                            subscriber.sendall(f"Topic: {subject}, Message: {msg_content}".encode("utf-8"))
                        except Exception as e:
                            print(f"[ERROR] Failed to send to a subscriber: {e}")
                    client_socket.sendall(b"<PUB_ACK>")
            
            # Handle DISCONNECT
            elif command == "DISC":
                client_socket.sendall(b"<DISC_ACK>")
                # Remove the client from all topic subscription lists
                for subject in subscriptions:
                    if client_socket in subscriptions[subject]["clients"]:
                        subscriptions[subject]["clients"].remove(client_socket)
                break
            
            else:
                client_socket.sendall(b"<ERROR: Unknown Command>")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        # Close the client connection
        client_socket.close()
        print(f"[INFO] Connection closed {client_address}")

# Function to start the server
def start_server():
    # Create a socket and bind it to a port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)
    print("[INFO] Server listening on port 12345")

    while True:
        # Accept incoming client connections
        client_socket, client_address = server_socket.accept()
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        print(f"[INFO] Started thread for {client_address}")

if __name__ == "__main__":
    start_server()
