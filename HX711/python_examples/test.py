import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(1)

print("waiting for connection...")
conn, addr = server_socket.accept()
print(f"connected by {addr}")

conn.send(b"Hello, Sessac!")
conn.close()
print("connection closed")
