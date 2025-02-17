# Chat Multissala

## Descrição
Este é um projeto de um servidor de chat multissala desenvolvido em Python, permitindo que os usuários se conectem a diferentes salas de conversa simultaneamente. O sistema suporta funcionalidades como mensagens privadas, listagem de salas, gerenciamento de conexões e permissões de criador da sala.

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
4. Teste os comandos implementados, como:
   - `/sair` - Sai da sala atual.
   - `/encerrar` - Fecha a conexão do cliente.
   - `/quem` - Lista os usuários na sala.
   - `@usuário mensagem` - Envia uma mensagem privada.
5. Verifique a funcionalidade de criador da sala e exclusão de salas vazias.

## Funcionalidades Implementadas
- Conexão de múltiplos clientes a um servidor de chat.
- Criação de salas de bate-papo dinâmicas.
- Permissão para definir senha ao criar uma sala.
- Listagem de salas e usuários conectados.
- Mensagens públicas e privadas entre usuários.
- Comandos de gerenciamento de conexões.
- Fechamento automático de salas vazias.
- Encerramento do servidor com comando `/shutdown`.

## Possíveis Melhorias Futuras
- Implementar interface gráfica para facilitar a interação.
- Adicionar suporte a logs persistentes em arquivo.
- Melhorar a segurança, incluindo criptografia nas mensagens.
- Criar um sistema de autenticação de usuários.
- Implementar suporte para histórico de conversa.

