import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

def handle_connection(conn, addr):
    with conn:
        print(f"Conneccted by: {addr}")
        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data
        response = send_request("www.google.com",80,request)
        conn.sendall(response)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)  # 2 tells socket how many requests to queue up, multithreading!

        conn, addr = server_socket.accept()
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)  # 2 tells socket how many requests to queue up, multithreading!

        while True: #loop to listen for multiple connections
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn,addr))
            thread.run()


    


def send_request(host, port, request_data):
    #acting as client, reaching out to google so they send us data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host,port))
        client_socket.send(request_data)
        client_socket.shutdown(socket.SHUT_WR)  #not technically necessary due to google's robust error handling

        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while (len(data) > 0):
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        
        return result


#start_server()
start_threaded_server()
