# process.py

# thread_server.py

from socket import *
import os,sys
from multiprocessing import *
import traceback
import signal

HOST = '0.0.0.0'
PART = 8888
ADDR = (HOST,PART)

#客户端处理函数
def handler():
    print('Connect from',connfd.getpeername())
    while True:
        data = connfd.recv(1024)
        if not data:
            break
        print(data.decode())
        connfd.send(b'Receive request')
    connfd.close()
    sys.exit(0)

#创建套接字
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

signal.signal(signal.SIGCHLD,signal.SIG_IGN) #process会产生僵尸进程，用信号设置让系统自动处理回收
#等待客户端请求
while True:
    try:
        connfd.addr = s.accept()

    except KeyboardInterrupt:
        s.close()
        sys.exit('服务器退出')

    except Exception:
        traceback.print_exc()
        continue

    p = Process(target = handler, args = (connfd,)) #
    p.start()
    p.daemon = True #设置

