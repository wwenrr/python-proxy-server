import os

http_error = """HTTP/1.1 400 Error
Content-Type: text/plain

Giới hạn kết nối
"""

def send_file(client_socket, file_path="src/view/not-found.html"):
    try:
        # Kiểm tra nếu file tồn tại
        if not os.path.isfile(file_path):
            error_message = "404 Not Found\n"
            client_socket.sendall(f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n{error_message}".encode('utf-8'))
            return
        
        client_socket.send("Không thấy trang".encode('utf-8'))

    except Exception as e:
        print(f"Lỗi khi gửi file: {str(e)}")
        # Nếu có lỗi, gửi 500 Internal Server Error
        client_socket.sendall("HTTP/1.1 500 Internal Server Error\r\n\r\nLỗi khi gửi file.".encode('utf-8'))
