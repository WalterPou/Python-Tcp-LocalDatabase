import socket
import threading
import json

lhost = 'localhost'
lport = int(input('LPORT: '))
DISCONNECT_MESSSAGE = "!DISCONNECT"

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind((lhost,lport))

class Database:
    def __init__(self, data_file='Database.json'):
        self.Source=data_file
        self.load_data()

    def show_data(self):
        with open(self.Source, 'r') as Source:
            return json.load(Source)

    def load_data(self):
        try:
            with open(self.Source, 'r') as Source:
                self.data=json.load(Source)
        except:
            self.data={}
    
    def save_data(self):
        with open(self.Source, 'w') as Source:
            json.dump(self.data, Source)
    
    def Cursor(self, auth):
        lm = list(self.data.keys())
        if auth in lm:
            return self.data.get(auth)
        else:
            return 'None'
    
    def Execute(self, auth, data):
        place = data
        self.data[auth] = place
        self.save_data()
        self.load_data()
        return "1 Memory Added!"

    def delete(self, auth):
        self.data.pop(auth)
        self.save_data()
        self.load_data()
        return '1 Memory Erased!'

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    
    connected = True
    while connected:
        Baseplate = Database()
        msg = conn.recv(1024).decode()
        if msg == DISCONNECT_MESSSAGE:
            conn.sendall('Disconnection Requested (Established).'.encode())
            print(f'[DISCONNECTED] {addr} disconnected.')
            connected = False
        #print(f'Received from {addr}: {msg}')
        if msg == 'list':
            results=Baseplate.show_data()
            print(f'Listing Data: {results}')
            conn.sendall(str(Baseplate.show_data()).encode())
        elif msg == 'store':
            print(f'{addr} is storing their info..')
            while True:
                try:
                    conn.sendall('Enter the ID that you want to replace/write: '.encode())
                    msg = int(conn.recv(1024).decode())
                    print(f'{addr} is storing their info with an ID {msg}')
                    conn.sendall('Data value: '.encode())
                    data = conn.recv(1024).decode()
                    results = Baseplate.Execute(msg, data)
                    conn.sendall(results.encode())
                    print(f'{addr} Stored Added an Item in the database!')
                    temporary = str(Baseplate.show_data())
                    print(f'ID {msg} Stored.')
                    print(f'Content: {data}')
                    break
                except:
                    conn.sendall('Must be an integer'.encode())
        elif msg == 'remove':
            print(f'{addr} is removing an Item!')
            try:
                conn.sendall('Enter in an ID to remove: '.encode())
                msg = conn.recv(1024).decode()
                print(f'{addr} is removing Item with an ID {msg}')
                results=Baseplate.delete(msg)
                conn.sendall(results.encode())
                print(f'ID {msg} content has been removed!')
            except:
                print('Key/ID Does not exist.')
                conn.sendall('Key/ID Does not exist.'.encode())
        elif msg == 'help':
            print('Sending guide..')
            conn.sendall('type "store" to store a data.'.encode())
            conn.sendall('type "remove" to remove a data.\n'.encode())
            conn.sendall('type "list" to list available data.'.encode())
            conn.sendall('type "!DISCONNECT" to disconnect from the server.\n'.encode())
        else:
            print(f'Received from {addr}: {msg}')
    
    conn.close()

status = True

def Disconnect_Func(status):
    while True:
        command = input()
        if command.upper() == 'SHUTDOWN':
            status = False
            break
        else:
            print(f'Command Does not Exist.')
    Server.close()
    print('\nServer is shutting down..\n')
    exit

def start():
    Server.listen()
    print('[LISTENING] SSLSSMS Server is listening for connections..')
    com_centre = threading.Thread(target=Disconnect_Func, args=(status,))
    com_centre.start()
    while status:
        conn,addr = Server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

print('SSLSSMS Server booting up! (Started)')
start()
