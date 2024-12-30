import socket

def forward(client_socket, server_address, rev):
    try:
        # print(server_address)
        # print(client_socket)
        # print(rev)

        forward_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        forward_socket.connect((server_address[0], int(server_address[1])))

        forward_socket.sendall(rev.encode('utf-8'))
        server_response = forward_socket.recv(4096)

        client_socket.sendall(server_response)
    except Exception as e:
        print(f"Error forwarding request: {e}")
        client_socket.sendall(b"HTTP/1.1 400 Error\r\n\r\nError forwarding request.")
    finally:
        forward_socket.close()