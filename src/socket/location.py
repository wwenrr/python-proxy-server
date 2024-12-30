def change_first_line(list, first_line, result):
    first_line[1] = f"/{result}"
    list[0] = " ".join(first_line)

    output = "\n".join(list)

    return output

def get_host_line(request):
    lines = request.split('\n')
    
    for line in lines:
        if line.startswith('Host:'):
            return line.strip()  
    
    return None

def location_detector(rev):
    try:
        from src.data.var import server

        # print(f"{rev}\n")

        list = rev.split('\n')

        first_line = list[0]
        host_line = get_host_line(rev)

        parts = first_line.split()

        domain = host_line.split(' ')[1].strip()
        location = parts[1].strip().split('/')

        # print(domain)
        # print(server[domain]['location'])
        # print(f"location: {location}")

        for route in server[domain]['location']:
            for key in route:
                location_list = key.split('/')
                size = len(location_list)

                if location[:size] == location_list:
                    remain = len(location) - size

                    # print(location[-remain:])

                    if size == len(location):
                        result = ''
                        final = f"{route[key]}"
                    else:
                        result = '/'.join(location[-remain:])
                        final = f"{route[key]}/{result}"

                    new_rev = change_first_line(list, parts, result)

                    return [route[key], new_rev]

        return None
    except Exception as e:
        print(str(e))
        return None