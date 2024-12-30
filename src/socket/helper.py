import json

def sni_gen(sock, server_name, context):
    try:
        from src.data.var import server

        print(f"Connection to {server_name}")

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