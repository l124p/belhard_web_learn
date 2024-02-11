import socket
import sys

HOST = "127.0.0.1" 
PORT = 7771
req = b'GET /index.html HTTP/1.1'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(req)
    print('Wait 1')
    data = s.recv(1024).decode('UTF-8')
    print('Wait 2')
print("Connection closed")
print(f"Received {data!r}")