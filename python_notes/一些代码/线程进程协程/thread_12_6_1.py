# 保存线程的状态信息
# 每次线程会创建一个自已专属的套接字链接(self.local.lock)
# 


from socket import socket, AF_INET, SOCK_STREAM
from functools import partial
import threading


class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.local = threading.local()

    def __enter__(self):
        if hasattr(self.local, 'sock'):
            print('Aleady connected')
        self.local.sock = socket(self.family, self.type)
        self.local.sock.connect(self.address)
        return self.local.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.local.sock.close()
        del self.local.sock

def test(conn):
    with conn as s:
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'HOST: www.python.org\r\n')
        s.send(b'\r\n')
        resp = b''.join(iter(partial(s.recv, 8192), b''))
        print(resp)
        # https://stackoverflow.com/questions/15331726/how-does-the-functools-partial-work-in-python
    #print(resp)
    print('Got {} bytes'.format(len(resp)))

if __name__ == '__main__':
    conn = LazyConnection(('www.python.org',80))
    t1 = threading.Thread(target=test,args=(conn,))
    t2 = threading.Thread(target=test,args=(conn,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

