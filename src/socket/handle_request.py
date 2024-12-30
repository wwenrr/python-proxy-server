from src.socket.server import lock
from src.data.var import max_connection

http_wait = """HTTP/1.1 200 OK
Content-Type: text/plain

"""

http_error = """HTTP/1.1 400 Error
Content-Type: text/plain

Giới hạn kết nối
"""

connect = 0

def handle_request(client_socket, client_address):
    try:
        global connect
        with lock: 
            connect += 1

        rev = client_socket.recv(2048).decode('utf-8')

        if(connect >= max_connection):
            print("Giới hạn kết nối, kết nối thất bại!\n")
            client_socket.send(http_error.encode('utf-8'))
        else:
            print(f"\033[94mConnection from {client_address}\033[0m, số lượng kết nối: {connect}/{max_connection} \n")
            from src.socket.location import location_detector

            result = location_detector(rev)

            if result is not None:
                destination_addr, new_rev = result
            else:
                raise Exception("Không thể lấy thông tin từ location_detector.")

            if destination_addr != None:
                client_socket.send(http_wait.encode())
                
                from src.socket.forwarding import forward
                forward(client_socket, destination_addr.split(":"), new_rev)
            else:
                client_socket.send(http_error.encode('utf-8'))
    except Exception as e:
        print(str(e))
    finally:
        client_socket.close()
        with lock:  
                connect -= 1
         

def error_request(client_socket, client_address):
    global connect

    rev = client_socket.recv(2048).decode('utf-8')

    if(connect >= max_connection):
        print("Giới hạn kết nối, kết nối thất bại!\n")
        client_socket.send(http_error.encode('utf-8'))
    else:
        print(f"Connection from {client_address}, số lượng kết nối: {connect}/{max_connection} \n")
        with lock: 
            connect += 1
        
        from src.view.send_html_file import send_file
        client_socket.send(http_error.encode('utf-8'))

    client_socket.close()
    with lock:  
            connect -= 1