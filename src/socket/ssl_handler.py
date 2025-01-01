import json
import ssl
from src.data.var import server
'''
Dữ Liệu:

domain: Domain sau khi phân giải dns
ssl_context: Đối tượng chứa danh sách các ssl
'''

def sni_gen(sock, server_name, context):
    from src.exception.DomainNotFound import DomainNotFound

    global domain
    
    if server_name not in server:
        domain = "u r dead idiot"
        print("Domain not found")
    else:
        domain = server_name

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