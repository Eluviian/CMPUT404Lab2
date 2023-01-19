import socket

BYTES_TO_READ = 4096

def get(host, port):
    request_data = b"GET / HTTP/1.1\nHost:"+host.encode('utf-8')+b"\n\n"  #byte string for get request
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create socket, specify it as internet socket, 
    s.connect((host,port)) #tuple, not two different params
    s.send(request_data)
    s.shutdown(socket.SHUT_WR)  #shutting down "write" (can also do read, or both, or entire socket)


    #listen for response
    response = s.recv(BYTES_TO_READ) #max number of bytes to read from server
    while len(response) > 0:
        #exit this while loop when server shuts down on its side
        print(response)
        response = s.recv(BYTES_TO_READ)

    s.close()

get("www.google.com", 80)  #80 is standard for unencrypted http requests, this is the port the google server is listening on



