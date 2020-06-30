"""
    简易聊天室客户端
chat room
env:python3.6
socket fork 练习
"""
from socket import *
import os,sys

#服务器地址
ADDR=('10.0.2.15',8888)

#发送消息
def send_msg(s,name):
    while True:
        try:
            text=input("发言：")
        except KeyboardInterrupt:
            text='quit'
        #退出聊天室
        if text=='quit':
            msg="Q "+name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")

        msg="C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)


#接收消息
def recv_msg(s):
    while True:
        data,addr=s.recvfrom(2048)
        #服务器发送EXIT表示让客户端退出
        if data.decode()=='EXIT':
            sys.exit()
        print(data.decode())

#创建网络连接
def main():
    s=socket(AF_INET,SOCK_DGRAM)
    while True:
        name=input("输入姓名：")
        msg="L " +name                   #请求聊天协议
        s.sendto(msg.encode(),ADDR)    #输入姓名，发送给服务区
        #等待服务器回应
        data,addr=s.recvfrom(1024)
        if data.decode()=='OK':    #如果允许进入聊天室，服务端发送'OK',给客户端
            print("您已进入聊天室")
            break
        else:
            print(data.decode()+"\n发言",end='')

    #创建新的进程
    pid=os.fork()
    if pid<0:
        sys.exit("Error!")
    elif pid ==0:
        send_msg(s,name)
    else:
        recv_msg(s)

if __name__=='__main__':
    main()