from threading import Thread
import socket
import sys

client_list = []

def main(args):
    # e.g. python3 server.py 127.0.0.1 8888
    if len(args) != 3:
        print("usage: python3 server.py host port")
        return
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    _, server_host, server_port = args
    server_sock.bind((server_host, int(server_port)))

    print(f"Relay server started on port {server_port}")

    while True:
        try:
            data, addr = server_sock.recvfrom(1024)
            
            if not data:
                continue            
            
            if addr not in client_list:
                client_list.append(addr)
            
            print(f"msg from [{addr[0]}:{addr[1]}]")

            for client in client_list:
                if client == addr:
                    continue
                server_sock.sendto(data, client)

        except KeyboardInterrupt:           
            server_sock.close()
            print("\nexit")
            break

if __name__ == "__main__":
    main(sys.argv)
