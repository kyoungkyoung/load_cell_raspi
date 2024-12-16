import socket
import time

class ServerRas:
    def __init__(self, port=5000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        print("Server started. Waiting for connection...")
        self.conn, self.addr = self.server_socket.accept()
        print(f"Connected by {self.addr}")

    def send_weight(self, weight):
        try:
            self.conn.sendall(weight)
            return True
        except Exception as e:
            print(f"Error sending data: {e}")
            return False


    def send_data(self, message):
        try:
            self.conn.sendall(message.encode())
            #time.sleep(2)
            return True
        except Exception as e:
            print(f"Error sending data: {e}")
            return False
        
    def receive_data(self):
        try:
            message_len_bytes = self.conn.recv(4)
            
            #print(f"message_len_bytes = {len(message_len_bytes)}")





            if not message_len_bytes:
                print("Connection closed by client.")
                return None
            message_len = int.from_bytes(message_len_bytes, 'big')

            data_bytes = self.conn.recv(message_len)
            data = data_bytes.decode('utf-8')


            #print(f"data_bytes = {len(data_bytes)}")
            #print(data)


            return data
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    def close(self):
        self.conn.close()
        self.server_socket.close()
        print("Connection closed")
