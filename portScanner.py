# -*- coding: utf-8 -*-
"""
端口扫描工具类，使用到了线程池，速度快
Usage:
  python portScanner.py <host>
For Example:
  python portScanner.py www.baidu.com
"""

import socket
import threading
import logging
import re
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor

__author__ = 'LiaoJinghang'
__version__ = '0.01'

# 日志配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='log.log',
    filemode='a',

    )


class PortScanner(object):
    """
    端口扫描工具类
    """
    def __init__(self, host, port_list=None, timeout=1):
        """
        构造
        :param host: 主机，可以是域名或者IP
        :param port_list: 端口列表，如果不指定，将扫描所有端口
        """
        self.__ip = None
        self.__host = host
        if port_list is None:
            self.__port_list = self.__get_port()
        else:
            self.__port_list = port_list
        self.__delay = timeout # 超时
        self.__thread_limit = 2000
        self.__output = {}

    @staticmethod
    def __get_port():
        """
        生成端口号数组
        :return: 端口号数组
        """
        return list(range(1, 65535))

    @staticmethod
    def __is_ip(ip):
        """
        检查是否是IP
        :param ip: 要检查的字符串
        :return: 如果是IP格式，返回真，否则返回假
        """
        return re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)

    def __tcp_connect(self, port_number):
        """
        连接/扫描指定端口，如果连接上，说明端口开放
        :param port_number: 要扫描的端口
        """
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        tcp_sock.settimeout(self.__delay)

        try:
            result = tcp_sock.connect_ex((self.__ip, int(port_number)))
            logging.debug("端口%s 返回值是%s", port_number, result)
            if result == 0:
                self.__output[port_number] = 'OPEN'
            else:
                self.__output[port_number] = 'CLOSE'
            tcp_sock.close()

        except socket.error as e:
            self.__output[port_number] = 'CLOSE'

    def __scan_ports_helper(self):
        """
        用线程池进行多线程扫描
        """
        port_index = 0
        with ThreadPoolExecutor(max_workers=self.__thread_limit) as executor:
            while port_index < len(self.__port_list):
                executor.submit(self.__tcp_connect, self.__port_list[port_index])
                port_index = port_index + 1

    def __scan_ports(self):
        """
        扫描端口，同时显示扫描状态
        """
        if self.__is_ip(self.__host):
            self.__ip = self.__host
        else:
            try:
                print("正在获取主机[{}]的IP……".format(self.__host))
                self.__ip = socket.gethostbyname(self.__host)
                print("主机[{}]的IP是：{}".format(self.__host, self.__ip))
            except socket.error as e:
                print("获取主机[{}]的IP出错，错误信息：{}".format(self.__host, e))
                return
                pass
        print("开始扫描[{}]的端口……".format(self.__ip))
        thread = threading.Thread(target=self.__scan_ports_helper)
        thread.start()
        while len(self.__output) < len(self.__port_list):
            self.__show_status()

            continue
        print()
        self.__show_result()

    def __show_status(self):
        """
        显示扫描状态
        """
        print(
            "最大线程数：{}，活动线程数：{}，端口数：{}，已扫描端口数：{}，已扫描端口量百分比：{}%    \r".format(
                self.__thread_limit, threading.active_count(),
                len(self.__port_list),
                len(self.__output),
                round(len(self.__output) / len(self.__port_list) * 100, 2)
            ),
            end=''
        )

    def __show_result(self):
        """
        显示结果
        """
        print("端口开放情况:")
        count = 0
        for port in self.__port_list:
            if self.__output[port] == 'OPEN':
                print(str(port) + ': ' + self.__output[port])
                count += 1
        if count == 0:
            print("没有开放端口")

    def run(self):
        """
        开始扫描
        """
        start_time = time.time()
        self.__scan_ports()
        stop_time = time.time()
        print("扫描结束，用时：%f 秒"%(stop_time-start_time))

    @staticmethod
    def __usage():
        """
        使用方法
        """
        print("Usage:\n  python %s <host>"%(os.path.basename(__file__)))
        print("For Example:\n  python %s www.baidu.com"%(os.path.basename(__file__)))
        pass

    @classmethod
    def start(cls):
        """
        开始扫描，处理参数
        """

        if len(sys.argv) < 2:
            PortScanner.__usage()
            return
        argv = sys.argv[1:]
        param = {
            "host": None,
            "-t": 1,
            "-p": None  # 端口号，用逗号隔开
        }
        # 获取参数
        i = 0
        while i < len(argv):
            if argv[i].startswith('-'):
                if argv[i] in param and (i+1) < len(argv):
                    param[argv[i]] = argv[i + 1]
                    i += 2
                else:
                    PortScanner.__usage()
                    return
            else:
                if param.get("host") is None:
                    param["host"] = argv[i]
                    i += 1
                else:
                    PortScanner.__usage()
                    return
        if param["-p"] is not None:
            param["-p"] = param["-p"].split(',')
            pass

        scanner = PortScanner(param["host"], port_list=param["-p"], timeout=param["-t"])
        scanner.run()
        pass


def main():
    """
    main函数，入口
    """
    PortScanner.start()

if __name__ == "__main__":
    main()
    pass
