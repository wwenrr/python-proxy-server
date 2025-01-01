from src.data.var import server
import json

def round_robin(domain):
    global server
    forward_size = len(server[domain]['forwarding'])
    
    if 'cur_table' not in server[domain]:
        position = 0
        
        server[domain]['cur_table'] = [0] * forward_size
        server[domain]['cur_table'][0] = 1
    else:
        position = server[domain]['cur_table'].index(1)
        server[domain]['cur_table'][position] = 0
        server[domain]['cur_table'][(position + 1) % forward_size] = 1
        position += 1

    print(server[domain]['cur_table'])
    return server[domain]['forwarding'][position % forward_size]


