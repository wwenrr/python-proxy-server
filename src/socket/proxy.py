from src.data.var import server
import socket

SERVER_IP = "34.96.134.68"

def finding_port_and_handle_connection(server_socket, domain):
    global server

    if domain in server:
        algo = server[domain]['load_balancin_algorithm']

        match algo:
            case 'round_robin':
                from src.socket.load_balancer import round_robin
                address = round_robin(domain)
                address = address.split(':')
                size = len(server[domain]['forwarding'])

                while size > 0:
                    try:
                        server_socket.connect((address[0], int(address[1])))
                        return
                    except Exception:
                        size -= 1
                        print(f"\033[31mConnection fail from address {address},\033[0m try annother one")
                        address = round_robin(domain)
                        address = address.split(':')

                
                
            case 'least_connection':
                print(2)

    


