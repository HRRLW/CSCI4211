import socket
import threading

VALID_TOPICS = ["WEATHER", "NEWS"]  # Allowed topics

# Connect to the server
def connect_to_server(client_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))
    connect_message = f"<{client_name}, CONN>"
    client_socket.sendall(connect_message.encode("utf-8"))
    print(client_socket.recv(1024).decode("utf-8"))
    return client_socket

# Publisher role
def publisher_role(client_name):
    client_socket = connect_to_server(client_name)

    # Ask the publisher to select a fixed topic
    subject = ""
    while subject not in VALID_TOPICS:
        subject = input(f"[{client_name}] Select a topic to publish (WEATHER/NEWS): ").strip().upper()
        if subject not in VALID_TOPICS:
            print(f"<ERROR: Subject Not Found>")
    print(f"[{client_name}] You are now publishing messages for the topic: {subject}")

    try:
        while True:
            # Get the message to publish
            message = input(f"[{client_name}] Enter message to publish for {subject} (or type 'exit' to disconnect): ").strip()
            if not message:
                print("<ERROR: Empty message is not allowed>")
                continue
            if message.lower() == 'exit':
                break

            # Send the publish message
            publish_message = f"<{client_name}, PUB, {subject}, {message}>"
            client_socket.sendall(publish_message.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            if response.startswith("<ERROR"):
                print(f"[Server Response]: {response}")
            else:
                print(f"[Server ACK]: {response}")
    finally:
        client_socket.sendall(b"<DISC>")
        print(client_socket.recv(1024).decode("utf-8"))
        client_socket.close()

# Subscriber role
def subscriber_role(client_name):
    client_socket = connect_to_server(client_name)

    # Allow user to select topics to subscribe to only ONCE
    subscribed = False
    while not subscribed:
        print(f"\n[{client_name}] Subscription options:")
        print("1. WEATHER")
        print("2. NEWS")
        print("3. BOTH")
        choice = input(f"Enter your choice (1-3): ").strip()

        if choice == "1":
            subject = "WEATHER"
            subscribe_message = f"<{client_name}, SUB, {subject}>"
            client_socket.sendall(subscribe_message.encode("utf-8"))
            print(client_socket.recv(1024).decode("utf-8"))
            subscribed = True
        elif choice == "2":
            subject = "NEWS"
            subscribe_message = f"<{client_name}, SUB, {subject}>"
            client_socket.sendall(subscribe_message.encode("utf-8"))
            print(client_socket.recv(1024).decode("utf-8"))
            subscribed = True
        elif choice == "3":
            for topic in VALID_TOPICS:
                subscribe_message = f"<{client_name}, SUB, {topic}>"
                client_socket.sendall(subscribe_message.encode("utf-8"))
                print(client_socket.recv(1024).decode("utf-8"))
            subscribed = True
        else:
            print("<ERROR: Invalid option>")
            continue

    print(f"[{client_name}] Subscribed successfully. You will now receive updates.")

    # Handle user input for exiting
    def handle_user_input():
        while True:
            user_input = input()  # User can type 'exit'
            if user_input.lower() == 'exit':
                try:
                    client_socket.sendall(b"<DISC>")
                    response = client_socket.recv(1024).decode("utf-8")
                    if response == "<DISC_ACK>":
                        print("[INFO] Disconnected successfully.")
                        break
                except Exception as e:
                    print(f"[ERROR] Disconnection failed: {e}")
                finally:
                    client_socket.close()

    # Start user input thread
    input_thread = threading.Thread(target=handle_user_input, daemon=True)
    input_thread.start()

    # Receive messages from the server
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"[{client_name} RECEIVED]: {message}")
                print(f"[{client_name}] Type 'exit' to disconnect: ")
    except Exception as e:
        print(f"[{client_name}] Connection closed: {e}")
    finally:
        client_socket.close()


# Main function for role selection
def main():
    while True:
        print("\nWelcome to the Messaging System!")
        print("Choose a role:")
        print("1. Publisher")
        print("2. Subscriber")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            client_name = input("Enter publisher name: ").strip()
            publisher_role(client_name)
        elif choice == "2":
            client_name = input("Enter subscriber name: ").strip()
            subscriber_role(client_name)
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
