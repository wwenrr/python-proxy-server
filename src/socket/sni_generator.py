import json
import ssl
from src.data.var import server
'''
Dữ Liệu:

ssl_context: Đối tượng chứa danh sách các ssl
'''

def ssl_loader(main_context):
    for domain, config in server.items():
        if 'ssl' in config:
            certfile = config['ssl']['cert']
            keyfile = config['ssl']['key']
            try:
                main_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
                print(f"Chứng chỉ SSL cho domain {domain} đã được nạp.")
            except Exception as e:
                print(f"\033[31mLỗi khi nạp chứng chỉ SSL cho domain {domain}: \033[0m{str(e)}")
                exit(0)

def sni_gen(sock, server_name, context):
    try:
        from src.data.var import server

        if server_name not in server:
            raise Exception("Domain không tồn tại trong file config")
        
        if "ssl" not in server[server_name]:
            raise Exception("Chứng chỉ ssl chưa được config")

        ssl = server[server_name]['ssl']
    
        context.load_cert_chain(
            certfile=ssl['cert'],
            keyfile=ssl['key']
        )
    except Exception as e:
        print(f"lỗi: {str(e)}")
        raise