'''
捕获kill信号
'''
import os
import time
import signal


class GracefulDeath:
    """Catch signals to allow graceful shutdown."""

    def __init__(self):
        self.receivedSignal = self.receivedTermSignal = False
        catchSignals = [
            1,
            2,
            3,
            10,
            12,
            15,
        ]
        for signum in catchSignals:
            signal.signal(signum, self.handler)

    def handler(self, signum, frame):
        self.lastSignal = signum
        self.receivedSignal = True
        if signum in [2, 3, 15]:
            self.receivedTermSignal = True


if __name__ == '__main__':
    print(os.getpid())
    sighandler = GracefulDeath()
    while True:
        if sighandler.receivedSignal:
            if sighandler.receivedTermSignal :
                print("Gracefully exiting due to receipt of signal {}".format(
                    sighandler.lastSignal))
                exit()v
            else:
                print("Ignoring signal {}".format(
                    sighandler.lastSignal))
                sighandler.receivedSignal = sighandler.receivedTermSignal = False

print("End of the program. I was killed gracefully :)")
