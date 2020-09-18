"""
Author: Liang
email: 936176514@qq.com
Time:2020-9-12
Env: python 3.6
socket and Process exercise
"""
from socket import *

# 服务器地址
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)

# 存储用户信息{name:address}
user = {}


# 框架启动函数
def do_login(sock, name, addr):
    if name in user:
        sock.sendto(b"Fail", addr)
        return
    else:
        sock.sendto(b"Ok", addr)
        # 通知其他人[''[/
        msg = "欢迎%s进入聊天室" % name
        for i in user:
            sock.sendto(msg.encode(), user[i])
        user[name] = addr  # 加入这个人
        print(user)


def do_chat(sock, name, content):
    msg = "%s : %s" % (name, content)
    for i in user:
        if i != name:
            sock.sendto(msg.encode(),user[i])


def do_exit(sock, name):
    del user[name]
    msg = "%s退出聊天室" % name
    for i in user:
        sock.sendto(msg.encode(), user[i])


def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ADDR)

    # 循环等待接收请求(总分处理模式）
    while True:
        # 所有请求都在这里接收
        data, addr = sock.recvfrom(1024)
        tmp = data.decode().split(" ",2)
        # 根据情况选择功能
        if tmp[0] == "L":
            # tmp ---> [L, name]
            do_login(sock, tmp[1], addr)
        if tmp[0] == "C":
            # tmp ---> [C, name, content]
            do_chat(sock, tmp[1], tmp[2])
        if tmp[0] == "E":
            do_exit(sock,tmp[1])


if __name__ == '__main__':
    main()
