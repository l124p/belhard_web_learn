import socket

HOST = '127.0.0.1'
PORT = 7771
OK = b'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\n\n'
ERR = b'HTTP/1.1 404 OK\nontent-Type: text/html; charset=UTF-8\n\n'

def send_file(file_name):
    try:
        with open(file_name, 'rb') as f:
            client_conn.send(OK)
            client_conn.send(f.read()) 
    except IOError:
        client_conn.send(ERR)

def index():
    with open ('index.html', 'rb') as f:
        return f.read()

def products(path):
    path = path.lstrip('/')
    with open (path, 'rb') as f:
        return f.read()

def about():
    with open ('about/index.html', 'rb') as f:
        return f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST,PORT))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.listen(3)
    
    while True:
        client_conn, addr = server.accept()
        with client_conn:
            print(f"Connected by {addr}")

            print(f"Recieve data")
            data = client_conn.recv(1024).decode('utf-8')
            #print(f"data={data}")

            path = data.split()[1]
            print(path[-4:])

            if path == '/' or path == '/index.html':
                client_conn.send(OK)
                client_conn.send(index())

            elif path == '/about/':
                client_conn.send(OK)
                client_conn.sendall(about())

            elif '/products/' in path and path[-4:] not in ['.jpg', '.png', '.gif']:
                client_conn.send(OK)
                client_conn.send(products(path))    

            elif path[-4:] in ['.jpg', '.png', '.gif']:
                print("send file:", path.strip('/'))
                send_file(path.strip('/')) 

            else:
                print("Страница не найдена")
                client_conn.send(ERR)
