import threading
import socket
import sys
import os

port = 7778
IP = "localhost"

# Dicionário para armazenar salas e seus respectivos clientes
rooms = {}

# Dicionário para armazenar os clientes conectados
clients = {}

# Cores para identificar os usuários
colors = [
    "\033[1;31m",  # Vermelho
    "\033[1;32m",  # Verde
    "\033[1;33m",  # Amarelo
    "\033[1;34m",  # Azul
    "\033[1;35m",  # Magenta
    "\033[1;36m"   # Ciano
]
RESET_COLOR = "\033[0m"

server_running = True  # Variável para manter o estado do servidor

# Envia um comando para limpar a tela do cliente
def clear_screen(client):
    client.send("\033[H\033[J".encode())

# Lista as salas disponíveis para o cliente
def list_rooms(client):
    clear_screen(client)
    if rooms:
        salas_formatadas = "\n".join([f"{i+1}️⃣   {room} ({len(rooms[room])} online)" for i, room in enumerate(rooms.keys())])
        client.send(f"\n🌐 Salas disponíveis:\n{salas_formatadas}\n\nDigite o nome da sala para entrar ou para criar uma nova: ".encode())
    else:
        client.send("❌ Nenhuma sala disponível.\n\nDigite o nome da sala para criar uma nova: ".encode())

# Lida com um novo cliente que se conecta ao servidor
def handle_client(client):
    try:
        client.send("Digite seu nome: ".encode())
        username = client.recv(1024).decode().strip()
        
        if username.lower() == "/encerrar":
            client.send("\nEncerrando conexão...\n".encode())
            client.close()
            return
        
        # Define a cor do usuário e adiciona-o à lista de clientes
        color = colors[len(clients) % len(colors)]
        clients[client] = (username, color)

        # Encaminha o cliente para o menu de escolha de salas
        return_to_lobby(client)
    except:
        remove_client(client)

# Menu de escolha de salas para o cliente
def return_to_lobby(client):
    username, color = clients.get(client, ("Desconhecido", RESET_COLOR))
    while True:
        try:
            list_rooms(client)
            room = client.recv(1024).decode().strip()
            
            if room.lower() == "/encerrar":
                client.send("\nEncerrando conexão...\n".encode())
                remove_client(client)
                return
            
            # Se a sala não existir, cria uma nova
            if room not in rooms:
                rooms[room] = []
            
            # Adiciona o cliente à sala escolhida
            rooms[room].append(client)

            # Exibe a sala e inicia a comunicação
            show_room(client, room)
            handle_messages(client, room)
        except:
            remove_client(client)
            return

# Exibe informações sobre a sala ao cliente
def show_room(client, room):
    clear_screen(client)
    client.send(f"\n🏠 {room.upper()} 🏠\n".encode())

    # Notifica os outros clientes da entrada do novo usuário
    broadcast(f"\n{clients[client][1]}{clients[client][0]}{RESET_COLOR} entrou na sala.", room, client)

# Gerencia as mensagens enviadas dentro de uma sala
def handle_messages(client, room):
    username, color = clients.get(client, ("Desconhecido", RESET_COLOR))
    while True:
        try:
            msg = client.recv(2048).decode()

            # Se o usuário digitar "/encerrar", fecha a conexão
            if msg.lower() == "/encerrar":
                remove_client(client, room)
                client.close()
                break

            # Se o usuário digitar "/sair", volta ao menu de salas
            elif msg.lower() == "/sair":
                rooms[room].remove(client)
                broadcast(f"\n{color}{username}{RESET_COLOR} saiu da sala.", room, client)
                return_to_lobby(client)
                break

            # Envia a mensagem para os outros membros da sala
            else:
                broadcast(f"\n{color}<{username}>{RESET_COLOR} {msg}", room, client)
        except:
            remove_client(client, room)
            break

# Envia mensagens para todos os clientes da sala, exceto o remetente
def broadcast(msg, room, sender):
    for client in rooms.get(room, []):
        if client != sender:
            try:
                client.send(msg.encode())
            except:
                remove_client(client, room)

# Remove um cliente da sala e do servidor
def remove_client(client, room=None):
    username, color = clients.get(client, ("Desconhecido", RESET_COLOR))

    # Remove o cliente da sala e notifica os demais membros
    if room and client in rooms.get(room, []):
        rooms[room].remove(client)
        broadcast(f"\n{color}{username}{RESET_COLOR} saiu da sala.", room, client)

        # Se a sala estiver vazia, remove-a
        if not rooms[room]:
            del rooms[room]

    # Remove o cliente da lista global
    if client in clients:
        del clients[client]

    client.close()

# Função para ouvir comandos do servidor
def server_command_listener(server):
    global server_running
    while server_running:
        cmd = input().strip().lower()
        if cmd == "/shutdown":
            print("\n\033[1;31m⚠️  Encerrando o servidor...\033[0m\n")
            
            # Encerra a conexão de todos os clientes
            for client in list(clients.keys()):
                try:
                    client.send("\n\033[1;31m⚠️  O servidor foi encerrado. Sua conexão será fechada.\033[0m\n".encode())
                    client.close()
                except:
                    pass
            
            server_running = False
            server.close()
            os._exit(0)

# Função principal do servidor
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, port))
    server.listen()
    print("Servidor iniciado 🚀")

    threading.Thread(target=server_command_listener, args=(server,), daemon=True).start()

    while server_running:
        try:
            client, _ = server.accept()
            threading.Thread(target=handle_client, args=(client,)).start()
        except:
            break

# Inicia o servidor
main()
