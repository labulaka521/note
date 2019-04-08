"""
端口转发
RUN the example as
 python portforwarder.py :8080 10.126.152.199:80

"""
from gevent import monkey;monkey.patch_all()
import socket
import sys
import signal
import gevent
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname


class PortForwarder(StreamServer):
    # 创建一个服务器来转发
    def __init__(self, listener, dest, **kwargs):
        StreamServer.__init__(self, listener, **kwargs)
        self.dest = dest

    def handle(self, source, address):
        log('%s:%s accepted', *address[:2])
        try:
            dest = create_connection(self.dest)
        except IOError as ex:
            log('%s:%s failed to connect to %s:%s', address[0], address[1],
                self.dest[0], self.dest[1], ex)
            return
        forwarders = (gevent.spawn(forward, source, dest, self),
                      gevent.spawn(forward, dest, source, self))
        gevent.joinall(forwarders)

    def close(self):
        if self.closed:
            sys.exit('Multiple exit signals received - aborting')
        else:
            log('Closing listen socket')
            StreamServer.close(self)


def forward(source, dest, server):
    #

    try:
        source_address = '%s:%s' % source.getpeername()[:2]
        dest_address = '%s:%s' % dest.getpeername()[:2]
        print(source_address, dest_address, 'source dest')
    except socket.error as ex:
        log('Failed to get all peer names: %s' % ex)
        return
    try:
        while True:
            try:
                data = source.recv(1024)
                print(data,source_address,'data')
                # log('%s->%s: %r', source_address, dest_address, data[:50])
                if not data:
                    break
                dest.sendall(data)
            except KeyboardInterrupt:
                if not server.closed:
                    server.close()
                break
            except socket.error:
                log('connection close from %s forward to %s' % (source_address, dest_address))
                # if not server.closed:
                #     server.close()
                break
    finally:
        source.close()
        dest.close()
        server = None


def parse_address(address):
    'return: remote  forward address port 10.126.152.199 80'
    try:
        hostname, port = address.rsplit(':', 1)
        port = int(port)
    except ValueError:
        sys.exit('Excepted HOST:PORT: %r' % address)
    # print(gethostbyname(hostname), port)
    return gethostbyname(hostname), port


def main():
    args = sys.argv[1:]
    if len(args) != 2:
        sys.exit('Usage: %s source-address destination-address' % __file__)
    source = args[0]
    dest = parse_address(args[1])
    server = PortForwarder(source, dest)
    log('Starting port forwarder %s:%s -> %s:%s', *(server.address[:2] + dest))
    # gevent.signal(signal.SIGTERM, server.close)       # 当portforwarder 接收到TERM 或者INT 信号会关闭监听的socket 并且等待所有的连接退出完成
    # gevent.signal(signal.SIGINT, server.close)
    server.start()
    gevent.wait()


def log(message, *args):
    message = message % args
    sys.stderr.write(message + '\n')


if __name__ == '__main__':
    main()
