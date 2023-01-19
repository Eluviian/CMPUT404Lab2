import socket

BYTES_TO_READ = 4096
HOST = "127.0.0.1"  #special IP address, points back to your own computer, could also use localhost
PORT = 8080

def handle_connection(conn, address):  #called whenever we recieve a connection from a client
    with conn:  #closes conn socket when done
        print(f"Connected by: {address}")
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data: #if connection shut down
                break
            print(data)
            conn.send(data)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  #auto cleaning resources like sockets, s will get closed automatically
        s.bind((HOST, PORT)) #tuple, just like for connect() in client.py

        #cannot bind more than one socket to same address, port pair
        #when we set REUSEADDR to 1, we can interupt "timeout" on socket where it hangs around before it gets deleted and can get rebound
        #if you want to set more options, call setsockopt again (ex - reuse port?)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #level you want, reuse socket address (how to reuse port? different),  

        s.listen()

        conn, address = s.accept()  #returns socket and (ip,port)
        handle_connection(conn, address)

start_server()

