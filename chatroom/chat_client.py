"""
聊天室客户端
"""
from socket import *
from multiprocessing import Process
import sys

# 服务器地址
ADDR = ("127.0.0.1", 8000)


def login(sock):
    while True:
        name = input("请输入姓名:")
        # 发送请求
        msg = "L " + name
        sock.sendto(msg.encode(), ADDR)
        # 等待回复
        data, addr = sock.recvfrom(1024)
        if data.decode() == "Ok":
            print("您已进入聊天室")
            return name
        else:
            print("该用户已存在")

def send_msg(sock, name):
    while True:
        try:
            content = input("请发送消息：")
        except Exception:
            content = "exit"

        if content == "exit":
            msg = "E %s" % name
            sock.sendto(msg.encode(),ADDR)
            sys.exit("您已退出聊天室")
        msg = "C %s %s" % (name, content)
        sock.sendto(msg.encode(), ADDR)

def recv_msg(sock):
    while True:
        # 服务端所有消息都在这里接收
        data, addr = sock.recvfrom(1024)
        msg = "\n" + data.decode() + "\n发送消息:"
        print(msg, end='')


def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('0.0.0.0', 55555))  # 保证客户端地址不变
    # 进入聊天室
    name = login(sock)
    # 创建子进程
    p = Process(target=recv_msg, args=(sock,))
    p.daemon = True
    p.start()
    send_msg(sock, name)  # 发送消息


if __name__ == '__main__':
    main()
