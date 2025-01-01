import json

if __name__ == "__main__":
    from src.data import var
    
    # Nạp biến từ file config
    var.init()

    #Nạp hàm khởi chạy socket
    from src.socket.server import start_proxy   

    # Chạy socket
    start_proxy()