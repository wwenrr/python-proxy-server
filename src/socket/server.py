import json
import socket
import time
import signal
import sys
import threading
import ssl

http_wait = """HTTP/1.1 200 OK
Content-Type: text/plain

"""

http_error = """HTTP/1.1 400 Error
Content-Type: text/plain

Giới hạn kết nối
"""

from src.data.var import max_connection
from src.data.var import server

connect = 0

lock = threading.Lock()

def handle_request(client_socket, client_address):
    global connect

    try:
        rev = client_socket.recv(2048).decode('utf-8')

        if(connect >= max_connection):
            print("Giới hạn kết nối, kết nối thất bại!\n")
            client_socket.send(http_error.encode('utf-8'))
        else:
            print(f"Connection from {client_address}, số lượng kết nối: {connect}/{max_connection} \n")
            with lock: 
                connect += 1
            
            client_socket.send(http_wait.encode())
            # time.sleep(1)
            client_socket.send("hello world\n".encode('utf-8'))
            # time.sleep(5)
            client_socket.send(":vvvvv".encode('utf-8'))
    except BrokenPipeError:
        print("Client hủy kết nối đột ngột")
    except OSError as e:
        print(f"OS error: {e}")
    except Exception as e:  
        print(f"Có lỗi xảy ra: {e} \n")
    finally:
        client_socket.close()
        with lock:  
                connect -= 1

def start_server(port=443):
    try:
        from src.socket.helper import sni_gen

        global max_connection

        # Tạo context để wrap https :v
        main_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        main_context.sni_callback = sni_gen

        # Tạo socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(2)
        print(f"Server is listening on {port}")
        print(f"Số host tối đa: {max_connection} \n-----------------------------------------------\n")

        # Bọc socket = https
        server_socket = main_context.wrap_socket(server_socket, server_side=True)

        def handle_signal(signum, frame):
            print("\nServer is shutting down...")
            server_socket.close()
            sys.exit(0)  

        signal.signal(signal.SIGINT, handle_signal)

        while True:
            try:
                client_socket, client_address = server_socket.accept()
                thread = threading.Thread(target=handle_request, args=(client_socket, client_address))
                thread.start()
            except Exception as e:  
                print(f"Có lỗi xảy ra: {e}")
    finally:
        server_socket.close()