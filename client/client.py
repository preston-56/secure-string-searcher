import ssl
import socket

def send_query(host, port, query, certfile=None, keyfile=None, cafile='ca.crt'):
    context = ssl.create_default_context(cafile=cafile)
    if certfile and keyfile:
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    
    try:
        with socket.create_connection((host, port)) as sock:
            sock.settimeout(30)  # Set the timeout on the socket
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.sendall(query.encode('utf-8'))  # Ensure the query is encoded in UTF-8
                response = ssock.recv(1024)  # Define a buffer size
                return response.decode('utf-8').strip()  # Ensure the response is decoded from UTF-8
    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    except socket.timeout:
        print("Socket timeout: The server did not respond in time.")
    except Exception as e:
        print(f"General error: {e}")