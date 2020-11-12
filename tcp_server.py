from threading import Thread
import socket
import sys

client_list = []

def sendAll(msg, source_sock):
    for client_sock in client_list:
        if client_sock != source_sock:
            client_sock.sendall(msg)

def handleClient(sock, addr):
    welcome_string = f"> New user {addr} entered ({len(client_list)} user{'s' if len(client_list) >= 2 else ''} online)"
    print(welcome_string)

    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            sendAll(data, sock)

        except:
            break

    client_list.remove(sock)
    goodbye_string = f"< The user {addr} left ({len(client_list)} user{'s' if len(client_list) >= 2 else ''} online)"
    print(goodbye_string)    

def main(args):
    # e.g. python3 server.py 127.0.0.1 8888
    if len(args) != 3:
        print("usage: python3 server.py IP_ADDR PORT")
        return
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    _, server_host, server_port = args
    server_sock.bind((server_host, int(server_port)))
    server_sock.listen()

    print(f"server started on port {server_port}")

    while True:
        try:
            # (sock, addr)
            client_sock, raw_addr = server_sock.accept()
            client_list.append(client_sock)
            
            cli_host, cli_port = raw_addr
            client_addr = f"{cli_host}:{cli_port}"
            
            th = Thread(target=handleClient, args=(client_sock, client_addr))
            th.daemon = True
            th.start()

        except KeyboardInterrupt:
            for client_sock, _ in client_list:
                client_sock.close()
            
            server_sock.close()
            print("\nexit")
            break

if __name__ == "__main__":
    main(sys.argv)
