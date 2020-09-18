import sys
from socket import *
from time import sleep


class Ftpclient():
    def __init__(self, sock):
        self.sock = sock

    def do_list(self):
        self.sock.send(b"LIST")
        result = self.sock.recv(1024).decode()
        if result == "ok":
            files = self.sock.recv(1024*1024)
            print(files.decode())
        else:
            print("文件库为空")

    def upload(self):
        filename = input("请输入文件地址:")
        try:
            file = open(filename,"rb")
        except:
            print("文件不存在")
            return
        filename = filename.split("/")[-1]
        self.sock.send(b"STOR"+filename.encode())
        result = self.sock.recv(1024).decode()
        if result == "ok":
            while True:
                data = file.read(1024)
                if not data:
                    break
                self.sock.send(data)
            sleep(0.1)
            self.sock.send(b"transfer complete")
            file.close()

            info = self.sock.recv(1024)
            print(info.decode())
            # print("发送完成")
        else:
            print("文件已存在，请更改文件名")

    def download(self,filename):
        # 发送请求
        msg = "RETR" + filename
        self.sock.send(msg.encode())
        # 等待回复
        result = self.sock.recv(128).decode()
        address = input("请输入保存地址:")
        if result == 'OK':

            # file = open("/home/tarena/" + filename, 'wb')
            file = open(address + filename, 'wb')

            while True:
                data = self.sock.recv(1024)
                if data == b'##':
                    break
                file.write(data)
            file.close()
            print("传输完成")
        else:
            print("文件不存在")

    def exit(self):
        self.sock.send(b"exit")
        self.sock.close()
        sys.exit()



def main():
    sock = socket()
    sock.connect(("127.0.0.1", 8800))
    ftp = Ftpclient(sock)
    while True:
        print("""
        1.查看所有文件
        2.上传文件
        3.下载文件
        4.退出终端
        """)
        choice = input("请输入菜单选项:")
        if choice == "1":
            ftp.do_list()
        elif choice == "2":
            ftp.upload()
        elif choice == "3":
            filename = input("请输入文件名称:")
            ftp.download(filename)
        elif choice == "4":
            ftp.exit()


if __name__ == '__main__':
    main()
