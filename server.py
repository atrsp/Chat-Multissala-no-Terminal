import threading
import socket
import os

# Configurações do servidor
port = 7778
IP = "localhost"

# Estruturas de dados para gerenciar salas, clientes e logs
rooms = {}  # Estrutura: {room_name: {"clients": [], "creator": client, "password": senha}}
clients = {}  # Estrutura: {client_socket: (username, color)}
logs = []  # Armazena mensagens do chat para fins de log

# Cores para os nomes dos usuários
colors = ["\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;34m", "\033[1;35m", "\033[1;36m"]
RESET_COLOR = "\033[0m"
server_running = True

# Função para limpar a tela do cliente
def clear_screen(client):
    client.send("\033[H\033[J".encode())

# Função para exibir o menu de comandos do servidor
def show_server_menu():
    print("\n\033[1;36mComandos do Servidor:\033[0m")
    print("  🔹 \033[1;31m/shutdown\033[0m   - Desliga o servidor e desconecta todos.\n")
    print("  🔹 \033[1;33m/logs\033[0m   - Mostra os logs do sistema.\n")

# Função para listar as salas disponíveis para o cliente
def list_rooms(client):
    clear_screen(client)
    available_rooms = [f"{i+1}️⃣ {room} ({len(info['clients'])} online)" for i, (room, info) in enumerate(rooms.items())]
    message = "\n🌐 Salas disponíveis:\n" + "\n".join(available_rooms) if rooms else "❌ Nenhuma sala disponível."
    client.send(f"{message}\n\nDigite o nome da sala para entrar ou criar uma nova: ".encode())

# Função para lidar com a conexão de um cliente
def handle_client(client):
    try:
        client.send("Digite seu nome: ".encode())
        username = client.recv(1024).decode().strip()

        if username.lower() == "/encerrar":
            client.send("\nEncerrando conexão...\n".encode())
            client.close()
            return

        # Atribui uma cor ao usuário e o adiciona à lista de clientes
        # Escolhe a cor do usuário usando o operador módulo (%) para garantir que as cores sejam distribuídas ciclicamente entre os usuários conectados
        color = colors[len(clients) % len(colors)]
        clients[client] = (username, color)

        # Retorna o cliente ao lobby (menu de salas)
        return_to_lobby(client)
    except:
        remove_client(client)

# Função para retornar o cliente ao lobby (menu de salas)
def return_to_lobby(client):
    while True:
        try:
            list_rooms(client)
            room = client.recv(1024).decode().strip()

            if room.lower() == "/encerrar":
                remove_client(client)
                return

            # Se a sala não existir, cria uma nova
            if room not in rooms:
                client.send("🔒 Deseja proteger essa sala com senha? (s/n): ".encode())
                use_password = client.recv(1024).decode().strip().lower() == "s"
                password = ""

                if use_password:
                    client.send("Digite a senha da sala: ".encode())
                    password = client.recv(1024).decode().strip()

                rooms[room] = {"clients": [], "creator": client, "password": password}

            # Se a sala for privada, solicita a senha
            elif rooms[room]["password"]:
                client.send("🔑 Esta sala é privada. Digite a senha: ".encode())
                entered_password = client.recv(1024).decode().strip()

                if entered_password != rooms[room]["password"]:
                    client.send("❌ Senha incorreta! Voltando ao lobby...\n".encode())
                    continue

            # Adiciona o cliente à sala e exibe a sala
            rooms[room]["clients"].append(client)
            show_room(client, room)
            handle_messages(client, room)
        except:
            remove_client(client)
            return

# Função para exibir a sala atual para o cliente
def show_room(client, room):
    clear_screen(client)
    creator = "(Criador)" if rooms[room]["creator"] == client else ""
    client.send(f"\n🏠 {room.upper()} 🏠 {creator}\n".encode())
    broadcast(f"{clients[client][1]}{clients[client][0]}{RESET_COLOR} entrou na sala.", room, client)

# Função para lidar com as mensagens enviadas pelo cliente na sala
def handle_messages(client, room):

    # Se client não existir no dicionário, username receberá "Desconhecido" e color receberá RESET_COLOR
    username, color = clients.get(client, ("Desconhecido", RESET_COLOR))
    while True:
        try:
            msg = client.recv(2048).decode()

            # Verifica se o cliente digitou o comando /encerrar para ser desconectado do servidor
            if msg.lower() == "/encerrar":
                remove_client(client, room)
                client.close()
                break

            # Verifica se o cliente digitou o comando /sair para sair da sala e voltar ao lobby
            elif msg.lower() == "/sair":
                rooms[room]["clients"].remove(client)
                broadcast(f"{color}{username}{RESET_COLOR} saiu da sala.", room, client)
                
                # Deleta a sala se ela estiver vazia
                if not rooms[room]["clients"]:
                    del rooms[room]

                return_to_lobby(client)
                break

            # Verifica se o cliente digitou o comando /quem para listar os usuários na sala
            elif msg.lower() == "/quem":
                users = ", ".join([clients[c][0] for c in rooms[room]["clients"]])
                client.send(f"👥 Usuários na sala: {users}\n".encode())

            # Verifica se o cliente digitou uma mensagem privada
            elif msg.startswith("@"):
                recipient_name, private_msg = msg[1:].split(" ", 1)

                # Procura um cliente (c) cujo nome (name) seja igual a recipient_name 
                # next() -> Retorna o primeiro resultado encontrado na busca
                recipient = next((c for c, (name, _) in clients.items() if name == recipient_name), None)
                if recipient:
                    recipient.send(f"\n🔒 Mensagem privada de {username}: {private_msg}\n".encode())
                else:
                    client.send("❌ Usuário não encontrado.\n".encode())
                    
            # Envia a mensagem para todos os clientes na sala
            else:
                logs.append(f"[{room}] {username}: {msg}") # Salva a mensagem enviada nos logs do sistema
                broadcast(f"{color}<{username}>{RESET_COLOR} {msg}", room, client) # Envia a mensagem para todos os demais clientes da sala
        except:
            remove_client(client, room)
            break

# Função para enviar uma mensagem para todos os clientes na sala, exceto o remetente
def broadcast(msg, room, sender):
    for client in rooms.get(room, {}).get("clients", []):
        if client != sender:
            try:
                client.send(msg.encode())
            except:
                remove_client(client, room)

# Função para remover um cliente da sala e da lista de clientes
def remove_client(client, room=None):
    username, color = clients.get(client, ("Desconhecido", RESET_COLOR))

    if room and client in rooms.get(room, {}).get("clients", []):

        # Tira o cliente da sala
        rooms[room]["clients"].remove(client)
        broadcast(f"{color}{username}{RESET_COLOR} saiu da sala.", room, client)

        # Se o último participante da sala sair, ela é deletada
        if not rooms[room]["clients"]:
            del rooms[room]
    
    # Tira o cliente da lista global de clientes
    if client in clients:
        del clients[client]
    
    # Fecha a conexão com o cliente
    client.close()

# Função para ouvir comandos do servidor (como /shutdown e /logs)
def server_command_listener(server):
    global server_running
    while server_running:
        cmd = input().strip().lower()

        # Verifica se o comando "/shutdown" foi digitado no terminal do servidor
        if cmd == "/shutdown":
            print("\n⚠️ Encerrando o servidor...\n")
            for client in list(clients.keys()):
                try:
                    # Desconecta todos os clientes
                    client.send("\n⚠️ O servidor foi encerrado.\n".encode())
                    client.close()
                except:
                    pass
            # Fecha o servidor
            server_running = False
            server.close()
            os._exit(0)
        
        # Verifica se o comando "/logs" foi digitado no terminal do servidor
        elif cmd == "/logs":
            # Imprime todas as mensagens enviadas no servidor, indicando sala, cliente e conteúdo da mensagem
            print("\n📜 LOGS DO SERVIDOR 📜")
            for log in logs:
                print(log)
        else: 
            print("\n❌ Comando inválido.\n")

# Função principal do servidor
def main():

    # Usei TCP para garantir que as mensagens sejam entregues corretamente e na ordem certa
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP

    # Liga o socket a um IP e a uma porta 
    server.bind((IP, port)) # Configuráveis no topo do arquivo para facilitar depuração

    # Servidor no modo de escuta
    server.listen()
    print("Servidor iniciado 🚀")

    show_server_menu()

    # Inicia uma thread para ouvir comandos do servidor
    threading.Thread(target=server_command_listener, args=(server,), daemon=True).start()

    while server_running:
        # Aceita novas conexões de clientes e cria uma thread para cada um
        try:
            # Quando um cliente se conecta, retorna dois valores: 
            # client (novo socket exclusivo para o cliente); 
            # _: o endereço do cliente (não está sendo usado, por isso o _)
            client, _ = server.accept()
            
            # Inicia uma nova thread para lidar com o cliente
            threading.Thread(target=handle_client, args=(client,)).start()
        except:
            break

# Inicia o servidor
main()
