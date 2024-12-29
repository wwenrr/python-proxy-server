from src.socket.server import start_server   
import json

data = None

if __name__ == "__main__":
    with open('config.json', 'r') as file:
        data = json.load(file)
    
    start_server(max_connec=data.get('max_connection', 10))