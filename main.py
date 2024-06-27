import socket
import threading

def handle_client(client_socket, client_address):
    buffer_size = 1024
    
    try:
        data = client_socket.recv(buffer_size)
        if data:
            search_string = data.decode('utf-8').strip()
            # Example search logic:
            if search_string == "hello":
                response = "STRING EXISTS\n"
            else:
                response = "STRING NOT FOUND\n"

            client_socket.sendall(response.encode())

    except UnicodeDecodeError as e:
        print(f"Error decoding data from {client_address}: {e}")
        client_socket.sendall(b"Error: Invalid UTF-8 data received\n")

    except Exception as e:
        print(f"Error processing client request from {client_address}: {e}")

    finally:
        client_socket.close()

def main():
    host = '0.0.0.0'
    port = 44445
    backlog = 5
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(backlog)
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            
            # Handle each client in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    except OSError as e:
        print(f"Socket error: {e}")

    except Exception as e:
        print(f"Server error: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
