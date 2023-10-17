import os

def main():
    while True:
        print("Menu:")
        print("1. Use like client")
        print("2. Use default server")
        print("3. Use ngrok server")
        
        print("4. Exit")

        escolha = input("Make you choice ")

        if escolha == "1":
            os.system("python  client.py")  
        elif escolha == "2":
            os.system("python server.py")
        elif escolha == "3":
            os.system("python server_ngrok.py")   
        elif escolha == "4":
            print("Exiting")
            break
        else:
            print("Command invalid. Try again!")

if __name__ == "__main__":
    main()
