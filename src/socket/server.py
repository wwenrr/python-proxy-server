import socket
import threading
import ssl
import time

http_error = """HTTP/1.1 400 Error
Content-Type: text/plain

Giới hạn kết nối
"""

def handle_client(client_socket, domain):
    lock = threading.Lock()
    from src.socket.proxy import finding_port_and_handle_connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    t2_status = False

    def forward_data(source, destination, client=True):
        nonlocal t2_status
        source.settimeout(3)

        while True:
            try:
                data = source.recv(1024)

                print(f"Package from: {'client' if client else 'server'} {len(data)}")

                if(client): 
                    print(data.decode('utf-8').split('\n')[0])

                if len(data) > 0:
                    destination.sendall(data)  
                else:
                    print("no data left bye bye")
                    break
            except Exception:
                break

    finding_port_and_handle_connection(server_socket, domain)
    t1 = threading.Thread(target=forward_data, args=(client_socket, server_socket))
    t1.start()
    
    forward_data(server_socket, client_socket, False)
    # print("t2 done")
    
    t1.join()
    # print("t1 done")

    client_socket.close()
    # server_socket.close()


def start_proxy():
    from src.socket.ssl_handler import  sni_gen, ssl_loader

    # Tạo context để wrap https 
    main_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    main_context.sni_callback = sni_gen

    ssl_loader(main_context)

    print("\n---------------------------------\n")

    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    proxy_socket.bind(('0.0.0.0', 443)) 
    proxy_socket.listen(5)

    print(f"Proxy đang lắng nghe trên cổng 443...")

    # Bọc socket = https
    server_socket = main_context.wrap_socket(proxy_socket, server_side=True)

    from src.exception.DomainNotFound import DomainNotFound
    while True:
        try:
            client_socket, client_address = server_socket.accept()

            from src.socket.ssl_handler import domain

            print(f"\033[33mKết nối từ client {client_address} \033[0m,\033[94m từ domain {domain}\033[0m")

            threading.Thread(target=handle_client, args=(client_socket, domain)).start()
        except Exception as e:
            continue
