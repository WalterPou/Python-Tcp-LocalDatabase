import socket
import threading
import time

h=input('H: ')
p=int(input('P: '))

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((h,p))

def order(client):
    while True:                                                                                   
        msg = client.recv(1024).decode()
        if not msg:
            break                                                                                 
        print(f'> ', end=' ')
        for char in msg:
            print(char, end='', flush=True)
            time.sleep(0.01)
        print('\n')

print('Connection Established!')
thread=threading.Thread(target=order,args=(client,))
thread.start()
while True:
    text=input()
    client.sendall(text.encode())
