import threading
import socket
import os

port = 7778
IP = "localhost"

# Função para limpar a tela do terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para exibir o menu inicial com comandos disponíveis
def show_menu():
    clear_screen()
    print("\033[1;36m" + "="*40)
    print("     🎉 Bem-vindo ao Chat Multissala 🎉")
    print("="*40 + "\033[0m")
    print("\n\033[1;33mCOMANDOS DISPONÍVEIS:\033[0m")
    print("  🔹 \033[1;32m/sair\033[0m       - Sai da sala atual e volta ao menu.")
    print("  🔹 \033[1;31m/encerrar\033[0m   - Fecha completamente a conexão.")
    print("\n🌟 \033[1;35mDivirta-se e boas conversas!\033[0m\n")
    print("="*40 + "\n")

# Função principal do cliente
def main():
    show_menu()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Tentativa de conexão com o servidor
    try:
        client.connect((IP, port))
    except:
        return print("\n\033[1;31mNão foi possível conectar ao servidor.\033[0m\n")

    # Inicia uma thread para receber mensagens do servidor
    threading.Thread(target=receive, args=[client]).start()

    # Chama a função que permite o envio de mensagens pelo usuário
    send(client)

# Função para receber mensagens do servidor
def receive(client):
    while True:
        try:
            msg = client.recv(2048).decode()
            if not msg:
                break
            print(msg)
        except:
            break

    print("\n\033[1;31mConexão encerrada pelo servidor.\033[0m")
    os._exit(0)

# Função para enviar mensagens para o servidor
def send(client):
    while True:
        try:
            msg = input()
            client.send(msg.encode())

            # Se o usuário digitar "/encerrar", fecha a conexão
            if msg.lower() == "/encerrar":
                print("\n\033[1;31mEncerrando conexão...\033[0m\n")
                client.close()
                break
        except:
            break

# Inicia o cliente
main()
