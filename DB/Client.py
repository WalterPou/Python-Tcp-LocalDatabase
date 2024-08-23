#Lib
import socket
import threading

h = input('H: ')
p = int(input('P: '))

def order(client_socket):
	while True:
		message = client_socket.recv(4096)
		if not message:
			break
		print(f'Received from SSLSSMS (Server/Database): {message.decode()}')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((h, p))
print('Connection Establised!')
thread1 = threading.Thread(target=order, args=(client_socket,))
thread1.start()
while True:
	text = input()
	if not text:
		break
	client_socket.sendall(text.encode())