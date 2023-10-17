import socket
import threading
import subprocess
import os

# Função para verificar se o ngrok está instalado na raiz
def is_ngrok_installed():
    try:
        subprocess.run(["./ngrok", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

if not is_ngrok_installed():
    print("ngrok is not installed in the root. Please install it and check your PATH.")
    exit(1)

def start_ngrok():
    # Inicie o ngrok para criar um túnel e exponha a porta 55555
    subprocess.run(["./ngrok", "tcp", "55555"])

def main():
    host = 'localhost'
    port = 55555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = []
    nicknames = []

    def broadcast(message):
        for client in clients:
            client.send(message)

    def handle(client):
        while True:
            try:
                message = client.recv(1024)
                broadcast(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break

    def receive():
        while True:
            client, address = server.accept()
            print("Connected with {}!".format(str(address)))

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print("Nickname is {}".format(nickname))
            broadcast('{} joined!'.format(nickname).encode('ascii'))
            client.send('Connected to Server!'.encode('ascii'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

    # Inicie o ngrok em uma thread separada
    ngrok_thread = threading.Thread(target=start_ngrok)
    ngrok_thread.start()

    print("Server is running in...")
    print("{}:{}".format(host, port))
    print("Use CTRL+C to interrupt!")

    receive()

if __name__ == "__main__":
    main()
