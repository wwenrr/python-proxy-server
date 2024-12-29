import socket
import time
import signal
import sys
import threading

http_wait = """HTTP/1.1 200 OK
Content-Type: text/plain

"""

http_error = """HTTP/1.1 400 Error
Content-Type: text/plain

Giới hạn kết nối
"""

connect = 0
max_connection = 5
lock = threading.Lock()

def handle_request(client_socket, client_address):
    global connect

    try:
        # rev = client_socket.recv(2048).decode('utf-8')

        if(connect >= max_connection):
            print("Giới hạn kết nối, kết nối thất bại!\n")
            client_socket.send(http_error.encode())
            client_socket.close()
        else:
            # print(f"Request receive:\n {rev}")
            print(f"Connection from {client_address}, số lượng kết nối: {connect}/{max_connection}\n")
            with lock: 
                connect += 1
            
            client_socket.send(http_wait.encode())
            time.sleep(1)
            client_socket.send("chờ xíu bro\n".encode())
            time.sleep(5)
            client_socket.send("chờ xong r".encode())
    except BrokenPipeError:
        print("Client hủy kết nối đột ngột")
    except OSError as e:
        print(f"OS error: {e}")
    except Exception as e:  
        print(f"Có lỗi xảy ra: {e}")
    finally:
        client_socket.close()
        with lock:  
                connect -= 1

def start_server(host='0.0.0.0', max_connec = 5, port=80):
    global max_connection
    max_connection = max_connec

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(max_connection)
    print(f"Server is listening on {host}:{port}")
    print(f"Số host tối đa: {max_connec}")

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