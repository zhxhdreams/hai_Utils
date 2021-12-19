# -*- coding: utf-8 -*-
# @Author: hai
# @Date: 2021-12-17 01:10:00

import httpx
import os
import queue
import re
import sys
import threading
import time
import logging

import hai_Utils.Util as Util

logger = logging.getLogger()
tlist = []


class DownloadInfo():
    link = None
    fileDir = None
    fileName = None
    description = ''
    useProxy = False
    headers = None


# 线程池设置
# 线程数量设置
# 超时设置
# 重连设置
# Header 设置
# 代理设置
# 设置下载队列完成时触发事件
# 增加下载任务
# 读取 Ban 域名列表
# 增加 Ban 域名列表条目
# 取消 Ban 域名列表条目
# 清空 Ban 域名列表
# 读取需要代理的域名列表
# 增加需要代理的域名列表条目
# 取消需要代理的域名列表条目
# 清空需要代理的域名列表
class DownloadUtil2():
    lock = threading.Lock()
    timeOut = 30
    retries = 3
    headers = {}
    threadNum = 2
    threadDownloadList = []
    # 下载队列
    queueDownload = queue.Queue()
    isDestory = False
    defaultDownloadDir = None
    banList = []
    useProxysHostList = []
    queueDownloadFinishCallBack = None
    proxies = None
    client = None
    ProxyClient = None

    class _DownloadThread2(threading.Thread):
        def run(self):
            print('thread name = {} args = {}'.format(threading.current_thread().name, self._args))
            outer = self._args[0]
            pattern = r'[\\/:*?"<>|\r\n]+'

            transport = httpx.HTTPTransport(retries=outer.retries)
            limits = httpx.Limits(max_keepalive_connections=None, max_connections=None)
            client = httpx.Client(limits=limits, transport=transport, timeout=outer.timeOut, headers=outer.headers, http2=True)
            if outer.proxies:
                proxyClient = httpx.Client(limits=limits, transport=transport, timeout=outer.timeOut, headers=outer.headers, proxies=outer.proxies, http2=True)
            else:
                proxyClient = None

            while True:
                if outer.isDestory:
                    break
                if outer.queueDownload.empty():
                    time.sleep(5)
                else:
                    outer.lock.acquire()
                    item = outer.queueDownload.get()
                    outer.queueDownload.task_done()
                    outer.lock.release()
                    if item.fileName:
                        fileName = re.sub(pattern, '-', item.fileName)
                    else:
                        fileName = re.sub(pattern, '-', str(item.link).split('/')[-1])
                    filePath = None
                    if not item.fileDir:
                        filePath = os.path.join(outer.defaultDownloadDir, fileName)
                    else:
                        filePath = os.path.join(item.fileDir, fileName)
                    # logger.info('正在下载: ' + description)
                    try:
                        response = None
                        _headers = None
                        if item.headers:
                             _headers = item.headers
                        else:
                            _headers = outer.headers
                        if item.useProxy:
                            if proxyClient:
                                response = proxyClient.get(item.link, headers=_headers)
                            else:
                                logger.warning('未设置代理信息，不能使用代理下载!')
                                continue
                        else:
                            response = client.get(item.link, headers=_headers)
                        with open(filePath, 'wb') as f:
                            for data in response.iter_bytes():
                                f.write(data)
                        if outer.queueDownloadFinishCallBack:
                            outer.queueDownloadFinishCallBack(item)
                    except Exception as e:
                        if os.path.exists(filePath):
                            os.remove(filePath)
                        logger.warning(str(e))
                        continue

    def setPoolNum(self, poolNum):
        self.poolNum = poolNum
        return self

    def setTimeOut(self, timeOut):
        self.timeOut = timeOut
        return self

    def setRetries(self, retries):
        self.retries = retries
        return self

    def setHeaders(self, headers):
        self.headers = headers
        return self

    def setThreadNum(self, threadNum):
        self.threadNum = threadNum
        return self

    def setProxies(self, proxies):
        self.proxies = proxies
        return self

    def setQueueDownloadFinishCallBack(self, callback):
        self.queueDownloadFinishCallBack = callback
        return self

    def addDownloadTask(self, url, fileDir=None, fileName=None, description=None, headers=None):
        host = Util.get_website_domain(url)
        if host in self.banList:
            return
        item = DownloadInfo()
        item.link = url
        item.fileDir = fileDir
        item.fileName = fileName
        item.description = description
        item.headers = headers
        if host in self.useProxysHostList:
            item.useProxy = True
        self.queueDownload.put(item)

    def beginDownload(self, url, fileDir=None, fileName=None, description=None, headers=None):
        try:
            host = Util.get_website_domain(url)
            if host in self.banList:
                return
            _useProxy = False
            if host in self.useProxysHostList:
                _useProxy = True
            _fileName = None
            pattern = r'[\\/:*?"<>|\r\n]+'
            if fileName:
                _fileName = re.sub(pattern, '-', fileName)
            else:
                _fileName = re.sub(pattern, '-', str(url).split('/')[-1])
            filePath = None
            if not fileDir:
                filePath = os.path.join(self.defaultDownloadDir, _fileName)
            else:
                filePath = os.path.join(fileDir, _fileName)
            # logger.info('正在下载: ' + description)
            try:
                response = None
                _headers = None
                if headers:
                    _headers = headers
                else:
                    _headers = self.headers
                if _useProxy:
                    if self.ProxyClient:
                        response = self.proxyClient.get(url, headers=_headers)
                    else:
                        raise Exception('未设置代理信息，不能使用代理下载!')
                else:
                    response = self.client.get(url, headers=_headers)
                with open(filePath, 'wb') as f:
                    for data in response.iter_bytes():
                        f.write(data)
            except Exception as e:
                if os.path.exists(filePath):
                    os.remove(filePath)
                raise e
        except Exception as e:
            raise e

    def loadBanList(self, banlist):
        for item in banlist:
            self.addBanHost(item)

    def addBanHost(self, host):
        if isinstance(host, str):
            _host = Util.get_website_domain(host)
            if _host not in self.banList:
                self.banList.append(_host)

    def removeBanHost(self, host):
        if isinstance(host, str):
            _host = Util.get_website_domain(host)
            if _host in self.banList:
                self.banList.remove(_host)

    def clearBanHost(self):
        self.banList = []

    def loadUseProxysHostList(self, useProxysHostList):
        if not self.proxies:
            raise Exception('未设置代理信息!')
        for item in useProxysHostList:
            self.addUseProxysHost(item)

    def addUseProxysHost(self, host):
        if not self.proxies:
            raise Exception('未设置代理信息!')
        if isinstance(host, str):
            _host = Util.get_website_domain(host)
            if _host not in self.useProxysHostList:
                self.useProxysHostList.append(_host)

    def removeUseProxysHost(self, host):
        if isinstance(host, str):
            _host = Util.get_website_domain(host)
            if _host in self.useProxysHostList:
                self.useProxysHostList.remove(_host)

    def clearUseProxysHost(self):
        self.useProxysHostList = []

    def _startQueueThreads(self):
        for i in range(self.threadNum):
            t = self._DownloadThread(name='download-thread-' + str(i), args=(self,))
            t.start()
            # t._stop()
            self.threadDownloadList.append(t)

    def buildQueue(self):
        self.destory()
        self.threadDownloadList.clear()
        self.isDestory = False

        self.defaultDownloadDir = os.path.dirname(sys.argv[0])
        if self.defaultDownloadDir.strip() == '':
            self.defaultDownloadDir = sys.path[0]
        self.defaultDownloadDir += '\\download_files\\'
        if not os.path.exists(self.defaultDownloadDir):
            os.mkdir(self.defaultDownloadDir)
        print('defaultDownloadDir is {}\n'.format(self.defaultDownloadDir))
        self._startQueueThreads()
        return self

    def build(self):
        self.defaultDownloadDir = os.path.dirname(sys.argv[0])
        if self.defaultDownloadDir.strip() == '':
            self.defaultDownloadDir = sys.path[0]
        self.defaultDownloadDir += '\\download_files\\'
        if not os.path.exists(self.defaultDownloadDir):
            os.mkdir(self.defaultDownloadDir)
        print('defaultDownloadDir is {}\n'.format(self.defaultDownloadDir))

        transport = httpx.HTTPTransport(retries=self.retries)
        limits = httpx.Limits(max_keepalive_connections=None, max_connections=None)
        self.client = httpx.Client(limits=limits, transport=transport, timeout=self.timeOut, headers=self.headers, http2=True)
        if self.proxies:
            self.proxyClient = httpx.Client(limits=limits, transport=transport, timeout=self.timeOut, headers=self.headers, proxies=self.proxies, http2=True)
        else:
            self.proxyClient = None

        return self

    def destory(self):
        self.isDestory = True
        while True:
            isOver = True
            for t in self.threadDownloadList:
                if t.is_alive():
                    isOver = False
                    break
            if isOver:
                break
            time.sleep(2)

    def waitForFinish(self):
        self.queueDownload.join()
        self.destory()
