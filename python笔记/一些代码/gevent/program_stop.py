import gevent
import signal
def run_forever():
    gevent.sleep(10000)

if __name__ == '__main__':
    gevent.signal(signal.SIGQUIT, gevent.shutdown)
    thread = gevent.span(run_forever)
    thread.join()
