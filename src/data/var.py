import json

'''
File Dữ Liệu Chính Của Server

data: Dữ liệu chung từ config.json
server: Các khối server để ánh xạ dữ liệu
max_connection: Số kết nối tối đa tới proxy
ssl_context: Danh sách các key
'''

def init():
    global max_connection
    global server
    global data

    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
            server = data['server']
            max_connection = data['max_connection']

            if(data == None or server == None or max_connection == None):
                raise Exception("Không tìm thấy dữ liệu")
    except Exception as e:
        print(e.message)
        exit(0)