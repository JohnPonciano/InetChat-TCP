import socket
import threading


nickname = input("Choose your Nickname: ")
host = input("Choose Host IP: ")
port = int(input("Choose Host Port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        message = '{}:{}'.format(nickname,input(''))
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()