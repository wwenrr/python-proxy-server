import json
import socket
import time
import signal
import sys
import threading
import ssl

from src.data.var import max_connection
from src.data.var import server

lock = threading.Lock()

def start_server(port=443):
    try:
        from src.socket.sni_generator import sni_gen, ssl_loader

        global max_connection

        # Tạo context để wrap https :v
        main_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        main_context.sni_callback = sni_gen

        ssl_loader(main_context)

        print(f"\033[33m-----------------------------------------------\033[0m")

        # Tạo socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(2)
        print(f"\033[32mServer is listening on \033[0m{port}")
        print(f"\033[32mSố host tối đa: \033[0m{max_connection} \033[33m\n-----------------------------------------------\n\033[0m")

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
                from src.socket.handle_request import handle_request
                threading.Thread(target=handle_request, args=(client_socket, client_address)).start()
            except BrokenPipeError:
                print("bro")
            except OSError as e:
                print(f"OS error: {e}\n")
            except Exception as e:  
                print(f"Có lỗi xảy ra: {str(e)}\n")
    except Exception as e:
        print(f"{str(e)}")
    finally:
        server_socket.close()