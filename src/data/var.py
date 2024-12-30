import json

'''
File Dữ Liệu Chính Của Server

data: Dữ liệu chung từ config.json
server: Các khối server để ánh xạ dữ liệu
max_connection: Số kết nối tối đa tới proxy
'''

def init():
    global max_connection
    global server
    global data

    with open('config.json', 'r') as file:
        data = json.load(file)
        server = data['server']
        max_connection = data['max_connection']