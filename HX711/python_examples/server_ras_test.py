import socket
import time

class Server_ras_test:
    def __init__(self, port=5000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(10)
        print("Server started. Waiting for connection...")
        self.conn, self.addr = self.server_socket.accept()
        print(f"Connected by {self.addr}")

    def send_data(self, message):
        try:
            self.conn.sendall(message.encode())
            return True
        except Exception as e:
            print(f"Error sending data: {e}")
            return False

    def close(self):
        self.conn.close()
        self.server_socket.close()
        print("Connection closed")

