from __future__ import print_function
import gevent
from gevent import subprocess


import sys


if sys.platform.startswith('win'):
    print('Unable to run on windows')
else:
    p1 = subprocess.Popen(['uname'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['ls'], stdout=subprocess.PIPE)

    gevent.wait([p1, p2],timeout=2)

    if p1.poll:
        print('uname: %r' % p1.stdout.read())
    else:
        print('uname: job is still running!')
    if p2.poll:
        print('ls: %r' % p2.stdout.read())
    else:
        print('ls: job is still running!')
    p1.stdout.close()
    p2.stdout.close()
