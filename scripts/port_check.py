import socket
s=socket.socket()
res=s.connect_ex(('127.0.0.1',8000))
print('connect_ex',res)
s.close()
