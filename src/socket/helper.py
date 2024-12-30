import json

def get_cert(domain):
    print("hello")

def parse_http_request(request):
    lines = request.splitlines()
    method, path, _ = lines[0].split(" ")  # GET / HTTP/1.1
    headers = {}

    # Parse các header từ dòng 2 trở đi
    for line in lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

    # Tạo JSON từ các phần đã phân tích
    request_data = {
        "method": method,
        "path": path,
        "headers": headers
    }

    return json.dumps(request_data, indent=4)