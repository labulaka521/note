# gunicron介绍
gunicron是一个适用于python的wsgi 服务器，基于prefork模型，所有的请求和响应都是工作进程来处理的。 
所以存在一个管理进程，然后管理者多 `TTIN` `TTOU`  `CHLD `
- HUP，重启所有的配置和所有的worker进程
- QUIT，正常关闭，它会等待所有worker进程处理完各自的东西后关闭
- INT/TERM，立即关闭，强行中止所有的处理
- TTIN，增加一个worker进程
- TTOU，减少一个worker进程
- USR1，重新打开由master和worker所有的日志处理
- USR2，重新运行master和worker
- WINCH，正常关闭所有worker进程，保持主控master进程的运行


1. 同步wooker 
一次只处理一个请求，如果期间发生错误只会影响一个请求
2. 异步worker  
基于greenlets(通过eventlet和gevent)

什么情况下选择异步worker

- 需要长时间阻塞调用的应用，比如外部的web service
- 直接给internet提供服务
- 流请求和响应（是类似flv流么？）
- 长轮询
- Web sockets

# 使用gunicorn来部署flask
gunicorn配置文件  
**gunicorn_config.py**
```
# Sample Gunicorn configuration file.

#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.
#
#   backlog - The number of pending connections. This refers
#       to the number of clients that can be waiting to be
#       served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should
#       only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048
#       range.
#

bind = '127.0.0.1:8000'
backlog = 2048

#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES)
#       range. You'll want to vary this a bit to find the best
#       for your particular application's work load.
#
#   worker_class - The type of workers to use. The default
#       sync class should handle most 'normal' types of work
#       loads. You'll want to read
#       http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
#       for information on when you might want to choose one
#       of the other worker classes.
#
#       A string referring to a Python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values
#       can be seen at
#       http://docs.gunicorn.org/en/latest/settings.html#worker-class
#
#   worker_connections - For the eventlet and gevent worker classes
#       this limits the maximum number of simultaneous clients that
#       a single process can handle.
#
#       A positive integer generally set to around 1000.
#
#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
#
#       Generally set to thirty seconds. Only set this noticeably
#       higher if you're sure of the repercussions for sync workers.
#       For the non sync workers it just means that the worker
#       process is still communicating and is not tied to the length
#       of time required to handle a single request.
#
#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#
#       A positive integer. Generally set in the 1-5 seconds range.
#

workers = 3
worker_class = 'gevent'
worker_connections = 1024
timeout = 30
keepalive = 2

#
#   spew - Install a trace function that spews every line of Python
#       that is executed when running the server. This is the
#       nuclear option.
#
#       True or False
#

spew = False

#
# Server mechanics
#
#   daemon - Detach the main Gunicorn process from the controlling
#       terminal with a standard fork/fork sequence.
#
#       True or False
#
#   raw_env - Pass environment variables to the execution environment.
#
#   pidfile - The path to a pid file to write
#
#       A path string or None to not write a pid file.
#
#   user - Switch worker processes to run as this user.
#
#       A valid user id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getpwnam(value) or None
#       to not change the worker process user.
#
#   group - Switch worker process to run as this group.
#
#       A valid group id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getgrnam(value) or None
#       to change the worker processes group.
#
#   umask - A mask for file permissions written by Gunicorn. Note that
#       this affects unix socket permissions.
#
#       A valid value for the os.umask(mode) call or a string
#       compatible with int(value, 0) (0 means Python guesses
#       the base, so values like "0", "0xFF", "0022" are valid
#       for decimal, hex, and octal representations)
#
#   tmp_upload_dir - A directory to store temporary request data when
#       requests are read. This will most likely be disappearing soon.
#
#       A path to a directory where the process owner can write. Or
#       None to signal that Python should choose one on its own.
#

daemon = False
#raw_env = [
#    'DJANGO_SECRET_KEY=something',
#    'SPAM=eggs',
#]
pidfile = '/run/gunicorn.pid'
umask = 0
user = 'natadmin'
group = 'natadmin'
tmp_upload_dir = None
reload = True

#
#   Logging
#
#   logfile - The path to a log file to write to.
#
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output
#
#       A string of "debug", "info", "warning", "error", "critical"
#

#errorlog = '-'
loglevel = 'info'
#accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = "/var/log/gunicorn/access.log"
errorlog = '/var/log/gunicorn/error.log'

#
# Process naming
#
#   proc_name - A base to use with setproctitle to change the way
#       that Gunicorn processes are reported in the system process
#       table. This affects things like 'ps' and 'top'. If you're
#       going to be running more than one instance of Gunicorn you'll
#       probably want to set a name to tell them apart. This requires
#       that you install the setproctitle module.
#
#       A string or None to choose a default of something like 'gunicorn'.
#

proc_name = None

#
# Server hooks
#
#   post_fork - Called just after a worker has been forked.
#
#       A callable that takes a server and worker instance
#       as arguments.
#
#   pre_fork - Called just prior to forking the worker subprocess.
#
#       A callable that accepts the same arguments as after_fork
#
#   pre_exec - Called just prior to forking off a secondary
#       master process during things like config reloading.
#
#       A callable that takes a server instance as the sole argument.
#
#
# def post_fork(server, worker):
#     server.log.info("Worker spawned (pid: %s)", worker.pid)
#
# def pre_fork(server, worker):
#     pass
#
# def pre_exec(server):
#     server.log.info("Forked child, re-executing.")
#
# def when_ready(server):
#     server.log.info("Server is ready. Spawning workers")
#
# def worker_int(worker):
#     worker.log.info("worker received INT or QUIT signal")
#
#     ## get traceback info
#     import threading, sys, traceback
#     id2name = {th.ident: th.name for th in threading.enumerate()}
#     code = []
#     for threadId, stack in sys._current_frames().items():
#         code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
#             threadId))
#         for filename, lineno, name, line in traceback.extract_stack(stack):
#             code.append('File: "%s", line %d, in %s' % (filename,
#                 lineno, name))
#             if line:
#                 code.append("  %s" % (line.strip()))
#     worker.log.debug("\n".join(code))
#
# def worker_abort(worker):
#     worker.log.info("worker received SIGABRT signal")
```

**启动命令**  

可以使用supervisord 来管理gunicron的启动与重启，
然后使用nginx 来反向代理端口

`gunicorn -D -c gunicorn_config.py app:app`


nginx
```
server {
        listen 80 default_server;
        root  /home/natadmin/snat_server/dist;
        charset utf-8;
        access_log  /var/log/nginx/snat_flask_access.log;
        error_log  /var/log/nginx/snat_flask_error.log;
        location /api {
            proxy_pass         http://127.0.0.1:8000;
            proxy_redirect     off;

            proxy_set_header   Host                 $host;
            proxy_set_header   X-Real-IP            $remote_addr;
            proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Proto    $scheme;
        }
        location / {
            try_files $uri $uri/ /index.html;
        }
}
```
supervisor
```
nat.ini
[program:nat]
command = pipenv run gunicorn app:app -c gunicorn_config.py
directory = /home/natadmin/snat_server
autostart = true
autorestart = true
user=natadmin
```
