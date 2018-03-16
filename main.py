import socket
import threading
from concurrent.futures import ThreadPoolExecutor

__port_list = [27788, 1, 3, 6, 9, 13, 17, 19, 20, 21, 22, 23, 24, 25, 30, 32, 37, 42, 49, 53, 70, 79, 80, 81, 82, 83, 84, 88,
               89, 99, 106, 109, 110, 113, 119, 125, 135, 139, 143, 146, 161, 163, 179, 199, 211, 222, 254, 255, 259,
               264, 280, 301, 306, 311, 340, 366, 389, 406, 416, 425, 427, 443, 444, 458, 464, 481, 497, 500, 512, 513,
               514, 524, 541, 543, 544, 548, 554, 563]
__thread_limit = 2000
__delay = 10

# __port_list = list(range(1, 65535))


def __tcp_connect(ip, port_number, delay, output):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    tcp_sock.settimeout(delay)

    try:
        result = tcp_sock.connect_ex((ip, int(port_number)))
        if result == 0:
            output[port_number] = 'OPEN'
            # print("{}:{}".format(port_number, 'OPEN'))
        else:
            output[port_number] = 'CLOSE'
            # print("{}:{}".format(port_number, 'CLOSE'))
        tcp_sock.close()

    except socket.error as e:
        output[port_number] = 'CLOSE'
    else:
        output[port_number] = 'CLOSE'


def __scan_ports_helper(ip, delay, output):
    port_index = 0
    with ThreadPoolExecutor(max_workers=__thread_limit) as executor:
        while port_index < len(__port_list):
            executor.submit(__tcp_connect, ip, __port_list[port_index], delay, output)
            port_index = port_index + 1


def __scan_ports(ip, delay):
    output = {}
    # __scan_ports_helper2(ip, delay, output)
    thread = threading.Thread(target=__scan_ports_helper, args=(ip, delay, output))
    thread.start()

    while len(output) < len(__port_list):
        print("最大线程数：{}，活动线程数：{}，端口数：{}，已扫描端口数：{}，已扫描端口量百分比：{}%\r".format(__thread_limit, threading.active_count(),
                                                                           len(__port_list), len(output),
                                                                           round(len(output) / len(__port_list) * 100,
                                                                                 2)), end='')
        continue
    print('\n')
    for port in __port_list:
        if output[port] == 'OPEN':
            print(str(port) + ': ' + output[port])
    return output


if __name__ == '__main__':
    __scan_ports('67.218.156.98', __delay)
    # __scan_ports('192.168.0.250', __delay, )


