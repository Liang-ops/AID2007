import os
import time
from threading import Thread
from socket import *
from signal import *

HOST = "0.0.0.0"
PORT = 8800
ADDR = (HOST, PORT)
FTP = "/home/tarena/mypython_file/"


class Mythread(Thread):
    def __init__(self, connfd):
        self.connfd = connfd
        super().__init__()

    def do_list(self):
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b"FAIL")
            return
        else:
            self.connfd.send(b"ok")
            time.sleep(0.1)
            data = "\n".join(file_list)
            self.connfd.send(data.encode())

    def do_upload(self, name):
        if name[4:] in os.listdir(FTP):
            self.connfd.send("Fail 文件已存在".encode())
            return
        else:
            self.connfd.send(b"ok")
            file = open(FTP + "%s" % name[4:], "wb")
            while True:
                data = self.connfd.recv(1024)
                if data == b"transfer complete":
                    break
                file.write(data)
            file.close()
            # time.sleep(0.1)
            self.connfd.send(b"success")

    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            print(data)
            if not data or data == "exit":
                break
            elif data == "LIST":
                self.do_list()
            elif data[:4] == "STOR":
                self.do_upload(data)
            elif data[:4] == "RETR":
                filename = data[4:]
                self.do_download(filename)

        self.connfd.close()

    def do_download(self, name):
        try:
            file = open(FTP + name, 'rb')
        except:
            # 文件不存在
            self.connfd.send(b'FAIL')
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
            while True:
                data = file.read(1024)
                if not data:
                    break
                self.connfd.send(data)
            # 表示文件已经发送结束
            time.sleep(0.1)
            self.connfd.send(b'##')
            file.close()


def main():
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    signal(SIGCHLD, SIG_IGN)
    while True:
        connfd, addr = sock.accept()
        print("Connect from", addr)
        t = Mythread(connfd)
        t.daemon = True
        t.start()


if __name__ == '__main__':
    main()
