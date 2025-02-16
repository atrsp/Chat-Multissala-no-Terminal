# Chat Multissala

## Descrição
Este projeto implementa um sistema de chat multissala baseado em sockets, permitindo a criação e participação em salas de conversa. O objetivo é fornecer um ambiente dinâmico onde os usuários podem se conectar, enviar mensagens em tempo real e gerenciar salas de chat. 

### Desafios abordados:
- Gerenciamento dinâmico de salas, incluindo remoção automática de salas vazias.
- Diferenciação entre criadores de salas e participantes comuns.
- Implementação de comandos para interação, como sair de salas e encerrar conexões.
- Interface de linha de comando intuitiva para o usuário.

## Tecnologias Utilizadas
- **Linguagem:** Python
- **Bibliotecas:** `socket`, `threading`, `os`, `sys`

## Como Executar

### Requisitos
- Python 3.x instalado

### Instruções de Execução
1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   ```
2. **Acesse a pasta do projeto:**
   ```bash
   cd <PASTA_DO_PROJETO>
   ```
3. **Execute o servidor:**
   ```bash
   python servidor.py
   ```
4. **Execute o cliente (em outra janela do terminal):**
   ```bash
   python cliente.py
   ```

## Como Testar
1. Inicie o servidor.
2. Abra múltiplos terminais e execute várias instâncias do cliente.
3. Experimente criar salas, enviar mensagens e testar os comandos `/sair` e `/encerrar`.
4. Verifique se as salas vazias são removidas automaticamente.

## Funcionalidades Implementadas
- Criar e entrar em salas de chat dinâmicas.
- Mensagens em tempo real entre participantes da mesma sala.
- Remoção automática de salas vazias ao sair o último participante.
- Diferenciação entre criador e participantes da sala.
- Comando `/sair` para retornar à seleção de salas.
- Comando `/encerrar` para desconectar o cliente.
- Comando do servidor `/shutdown` para encerrar todas as conexões.

## Possíveis Melhorias Futuras
- Implementar uma interface gráfica para melhor experiência do usuário.
- Adicionar criptografia para proteger as mensagens enviadas.
- Suporte a salas privadas com senhas.
- Registro de mensagens no servidor para auditoria.
- Integração com banco de dados para salvar histórico de chats.

