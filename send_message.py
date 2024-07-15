import socket
import threading
import time

ANDROID_IP_ADDRESS = '10.0.2.16'  # Replace with the IP address of your Android device
PORT = 5005  # Choose a port number

HOST = '192.168.23.228'  # Loopback for local testing 228 is computerip
# PORT = 5005        # Port to listen on
accepted_CLIENTS = 2     # Maximum number of clients to connect

# connected_clients = 0
client_lock = threading.Lock()
# messages_received = []  # List to store messages from clients

# def handle_client(conn, addr):
#     global connected_clients
#     print(f"Connected to {addr}")
#     try:
#         while True:

#             data = conn.recv(1024)  # Receive data from the client
#             if not data:
#                 break  # No more data from client
#             # Store received message with the clie  3nt's address
#             with client_lock:
#                 messages_received.append((addr, data))
#                 message = data.decode("utf-8")
#                 # Check if messages from two different clients have been received
#                 if message == "Object detected!":
#                     print("Messages received", message)
#                     print("Sending message to Android app...")

#                     # Example: Sending a message to the Android device
#                      # Port on which the Android device is listening
#                     android_message = b"Message from server to Android device"

#                     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as android_socket:
#                         android_socket.connect((ANDROID_IP_ADDRESS, 5005))
#                         android_socket.sendall(android_message)

#                     print("Message sent to Android app.")
#                     messages_received.clear()  # Clear the list after handling

#             conn.sendall(data)  # Echo back the received data
#     finally:
#         with client_lock:
#             connected_clients -= 1
#         conn.close()  # Ensure the connection is closed


# def server():
#     global connected_clients
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         s.listen()
#         print(f"Server listening on {HOST}:{PORT}")
#         while True:
#             conn, addr = s.accept()
#             with client_lock:
#                 if connected_clients < 100:
#                     # Start a new thread to handle the client
#                     threading.Thread(target=handle_client, args=(conn, addr)).start()
#                     connected_clients += 1
#                     while True:
#                         print("Message sent to Android app")
#                         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as android_socket:
#                             android_socket.connect((ANDROID_IP_ADDRESS, 5005))
#                             android_socket.sendall("android_message")
#                         time.sleep(2)

#                 else:
#                     print("Max clients reached. Connection rejected.")
#                     conn.close()

# if __name__ == "__main__":
#     server_thread = threading.Thread(target=server)
#     server_thread.start()



# import socket
ANDROID_IP_ADDRESS = '10.0.2.16'  # Replace with the IP address of your Android device
# ANDROID_IP_ADDRESS = '10.182.100.154'  # Replace with the IP address of your Android device
 
PORT = 5005  # Choose a port number



# Listen for incoming connections


print(f"Server listening on port {PORT}")

if __name__ == "__main__":
    x = False
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    connected_clients = {}
    connected_ips = set()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            ip_address = client_address[0]  # Extract IP address
            if ip_address not in connected_ips:
                print(f"Connection from {client_address}")
                connected_clients[ip_address] = client_socket
                connected_ips.add(ip_address)
            else:
                print(f"Duplicate {client_address} ignored.")
                client_socket.close()  # Close the duplicate connection immediately

            if len(connected_ips) >= 2:
                # Send a message to all unique clients
                message = "Person detected!"
                for client_socket in connected_clients.values():
                    client_socket.send(message.encode())

                # Close all connections
                for client_socket in connected_clients.values():
                    client_socket.close()

                connected_clients.clear()
                connected_ips.clear()
                print("All connections closed.")
                
    finally:
        for client_socket in connected_clients.values():
            client_socket.close()
        print("All connections closed.")
