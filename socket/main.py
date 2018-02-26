import socket
import threading as th

var=40

def f(v):
    while(1):
        global var
        var=var+v
        print(var)

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("127.0.0.1", 80))

t =th.Thread(target=f,args=(-1,))
t.start();
t2 =th.Thread(target=f,args=(1,))
t2.start();