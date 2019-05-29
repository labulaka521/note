# 使用Queue来实现一个线程池
# 只在IO处理时使用线程池·
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue


def echo_client(q):
    sock, client_addr = q.get()
    print('Got connection from', client_addr)
    while True:
        msg = sock.recv(65535)
        if not msg:
            break
        sock.sendall(msg)

    print('Client closed connection')
    sock.close()


def echo_server(addr, nworkers):

    q = Queue()
    for n in range(nworkers):
        t = Thread(target=echo_client, args=(q,))
        t.daemon = True
        t.start()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        print(client_sock, client_addr)
        q.put((client_sock,client_addr))
echo_server(('',15003), 138)
