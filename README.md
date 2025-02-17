# Chat Multissala

## Descrição
Este é um projeto de um servidor de chat multissala desenvolvido em Python, permitindo que os usuários se conectem a diferentes salas de conversa simultaneamente. O sistema suporta funcionalidades como mensagens privadas, listagem de salas e salas com senha.

O projeto aborda desafios relacionados à comunicação em redes, manipulação de múltiplas conexões via threads e gerenciamento de salas de bate-papo dinâmicas.

## Tecnologias Utilizadas
- **Linguagem:** Python 3
- **Bibliotecas:**
  - `socket` - Para a comunicação entre cliente e servidor.
  - `threading` - Para manipulação de múltiplas conexões simultâneas.
  - `os` - Para interação com o sistema operacional, como limpeza da tela.

## Como Executar

### Requisitos
- Python 3 instalado.

### Instruções de Execução

1. **Clone o repositório:**
   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   ```

2. **Inicie o servidor:**
   ```sh
   python3 server.py
   ```

3. **Execute o cliente:**
   ```sh
   python3 client.py
   ```

## Como Testar
1. Inicie o servidor.
2. Abra múltiplos terminais e execute o cliente em cada um deles.
3. Experimente entrar em diferentes salas digitando o nome da sala ao conectar.
4. Teste os comandos implementados para os clientes, como:
   - `/sair` - Sai da sala atual e retorna para o lobby.
   - `/encerrar` - Fecha a conexão do cliente.
   - `/quem` - Lista os usuários na sala.
   - `@usuário digite_a_mensagem` - Envia uma mensagem privada.
5. Verifique a funcionalidade de exclusão de salas vazias.

## Funcionalidades Implementadas
- Conexão de múltiplos clientes a um servidor de chat.
- Criação de salas de bate-papo dinâmicas.
- Permissão para definir senha ao criar uma sala.
- Listagem de salas e usuários conectados.
- Mensagens públicas e privadas entre usuários.
- Fechamento automático de salas vazias.
- Encerramento do servidor com comando `/shutdown` (no terminal do servidor).

## Possíveis Melhorias Futuras
- Implementar interface gráfica para facilitar a interação.
- Melhorar a segurança, incluindo criptografia nas mensagens.
- Criar um sistema de autenticação de usuários, verificando nomes repetidos.
- Implementar suporte para histórico de conversa.

