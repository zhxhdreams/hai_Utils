#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: hai 
# @Created Date: 2018-11-17 21:06:17 

import sys
import os
import time
import signal


class Daemon:
    def __init__(self, pidfile='/var/run/daemon.pid', logfile='/var/log/daemon.log', stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        # 需要获取调试信息，改为stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr'，以root身份运行。
        self.stdin = stdin
        self.stdout = logfile
        self.stderr = logfile
        self.pidfile = pidfile

    def _daemonize(self):

        def sig_handler(sig, frame):
            sys.stdout.write('sig is : %d\n' % sig)
            if sig == signal.SIGTERM:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                sys.exit(0)
            else:
                sys.exit(1)


        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGQUIT, sig_handler)

        try:
            # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
            pid = os.fork()  # 第一次fork，生成子进程，脱离父进程
            if pid > 0:
                sys.exit(0)  # 退出主进程
        except OSError as e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' %
                             (e.errno, e.strerror))
            sys.exit(1)

        os.chdir("/")   # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
        os.setsid()     # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。
        os.umask(0)     # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。

        # 第二次fork，禁止进程打开终端
        try:
            pid = os.fork()  
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' %
                             (e.errno, e.strerror))
            sys.exit(1)

        # 进程已经是守护进程了，重定向标准文件描述符
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdin.close()
        # si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+', 0)
        # os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # 注册退出函数，根据文件pid判断是否存在进程
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write('%s\n' % pid)
    

    def start(self):
        sys.stdout.write('starting service~\n')
        sys.stdout.flush()
        # 检查pid文件是否存在以探测是否存在进程
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = 'pidfile %s already exist. Daemon already running!\n'
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # 启动监控
        self._daemonize()
        self._run()

    def stop(self):
        # 从pid文件中获取pid
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:  # 重启不报错
            message = 'pidfile %s does not exist. Daemon not running!\n'
            sys.stderr.write(message % self.pidfile)
            return
        
        # 杀进程
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
        except OSError as err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)


    def restart(self):
        self.stop()
        time.sleep(2)
        self.start()


    # 用子类继承Daemon类并重写 _run() 函数实现自己的逻辑
    def _run(self):
        """ run your fun"""
        while True:
            # fp=open('/tmp/result','a+')
            #fp.write('Hello World\n')
            sys.stdout.write('%s:hello world\n' % (time.ctime()))
            sys.stdout.flush()
            time.sleep(2)
