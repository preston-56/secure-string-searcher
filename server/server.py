import ssl
import socket
import threading
import time
import sys
import os

# Append the root directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import read_config
from search.search import SearchEngine

class StringSearchServer:
    def __init__(self):
        self.host, self.port, self.file_path, self.reread_on_query, self.ssl_enabled, self.ssl_cert, self.ssl_key = read_config()
        print(f"SSL enabled: {self.ssl_enabled}, Cert: {self.ssl_cert}, Key: {self.ssl_key}")
        self.search_engine = SearchEngine(self.file_path, self.reread_on_query)
        self.is_running = False

    def handle_connection(self, conn, addr):
        try:
            if self.ssl_enabled:
                print('SSL enabled')
                ssl_versions = [
                    ssl.PROTOCOL_TLSv1_2,
                    ssl.PROTOCOL_TLS,  # Try the generic TLS protocol
                ]
                for ssl_version in ssl_versions:
                    try:
                        conn = ssl.wrap_socket(conn, server_side=True, certfile=self.ssl_cert, keyfile=self.ssl_key, ssl_version=ssl_version)
                        print('SSL handshake complete')
                        break
                    except ssl.SSLError as e:
                        print(f"SSL error: {e}")
                else:
                    print("No compatible SSL/TLS version found")
                    return

            data = conn.recv(1024)

            try:
                data = data.decode('utf-8', errors='replace').strip("\x00")
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")
                conn.sendall(b"Error: Invalid UTF-8 data received\n")
                return

            start_time = time.time()
            response = "STRING EXISTS" if self.search_engine.search_string(data) else "STRING NOT FOUND"
            execution_time = time.time() - start_time
            print(f"DEBUG: Query: {data}, IP: {addr[0]}, Execution time: {execution_time:.5f} seconds")
            conn.sendall(response.encode() + b"\n")

        except ssl.SSLError as e:
            print(f"SSL error: {e}")
        except Exception as e:
            print(f"General error: {e}")
        finally:
            conn.close()

    def run(self):
        self.is_running = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((self.host, self.port))
                s.listen(1024)
                self.socket = s
                print(f"Server listening on {self.host}:{self.port}")
                while self.is_running:
                    conn, addr = s.accept()
                    threading.Thread(target=self.handle_connection, args=(conn, addr)).start()
            except OSError as e:
                print(f"DEBUG: Failed to bind server to {self.host}:{self.port}. Error: {e}")
                self.is_running = False

    def stop(self):
        self.is_running = False
        if hasattr(self, 'socket'):
            self.socket.close()

if __name__ == "__main__":
    server = StringSearchServer()
    server.run()