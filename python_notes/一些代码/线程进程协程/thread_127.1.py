# 创建一个线程池
# 使用concurrent.futures ThreadPoolExecutor

from socket import AF_INET,SOCK_STREAM,socket
from concurrent.futures import ThreadPoolExecutor


def echo_client(sock, client_addr):
    print('Got connection from',client_addr)
    while True:
        msg = sock.recv(65536)
        if not msg:
            break
        sock.sendall(msg)

    print('Client closed connection')
    sock.close()


def echo_server(addr):
    pool = ThreadPoolExecutor(128)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        pool.submit(echo_client, client_sock, client_addr)


echo_server(("",15002))

