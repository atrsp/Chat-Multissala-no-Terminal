import threading
import socket
import os

# Configuração do cliente
port = 7777  # Porta do servidor
IP = "localhost"  # Endereço IP do servidor

# Função para limpar a tela do terminal
def clear_screen():
    # Verifica o sistema operacional e executa o comando apropriado para limpar a tela
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para exibir o menu inicial com comandos disponíveis
def show_menu():
    clear_screen()
    # Exibe o menu com cores e emojis para melhorar a experiência do usuário
    print("\033[1;36m" + "="*40)
    print("     🎉 Bem-vindo ao Chat Multissala 🎉")
    print("="*40 + "\033[0m")
    print("\n\033[1;33mCOMANDOS DISPONÍVEIS:\033[0m")
    print("  🔹 \033[1;32m/sair\033[0m       - Sai da sala atual e volta ao menu.")
    print("  🔹 \033[1;31m/encerrar\033[0m   - Fecha completamente a conexão.")
    print("  🔹 \033[1;34m/quem\033[0m    - Lista os usuários de uma sala.")
    print("  🔹 \033[1;35m@usuário\033[0m    - Envia mensagem privada para um usuário.")
    print("\n🌟 \033[1;36mDivirta-se e boas conversas!\033[0m\n")
    print("="*40 + "\n")

# Função principal do cliente
def main():
    show_menu()
    # Cria um socket TCP/IP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Tentativa de conexão com o servidor
    try:
        client.connect((IP, port))
    except:
        # Se a conexão falhar, exibe uma mensagem de erro e encerra o programa
        return print("\n\033[1;31mNão foi possível conectar ao servidor.\033[0m\n")

    # Inicia uma thread para receber mensagens do servidor
    threading.Thread(target=receive, args=[client]).start()

    # Chama a função que permite o envio de mensagens pelo usuário
    send(client)

# Função para receber mensagens do servidor
def receive(client):
    while True:
        try:
            # Recebe mensagens do servidor (tamanho máximo de 2048 bytes)
            msg = client.recv(2048).decode()
            if not msg:
                # Se a mensagem estiver vazia, a conexão foi encerrada
                break
            print(msg)
        except:
            # Se ocorrer um erro, encerra a conexão
            break

    print("\n\033[1;31mConexão encerrada pelo servidor.\033[0m")
    os._exit(0)  # Encerra o programa

# Função para enviar mensagens para o servidor
def send(client):
    while True:
        try:
            # Captura a mensagem digitada pelo usuário
            msg = input()
            client.send(msg.encode())  # Envia a mensagem para o servidor

            # Se o usuário digitar "/encerrar", fecha a conexão
            if msg.lower() == "/encerrar":
                print("\n\033[1;31mEncerrando conexão...\033[0m\n")
                client.close()
                break
        except:
            # Se ocorrer um erro, encerra a conexão
            break

# Inicia o cliente
main()