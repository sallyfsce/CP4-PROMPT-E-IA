## INTEGRANTES

```
Aneliza Rondina Bonafé - RM: 572977
Rafaella Ferreira de Moraes - RM: 571030

```

# Sistema de Atendimento Inteligente - Banco Fictício

Trabalho de faculdade utilizando o **OpenAI Agents SDK** para simular
o atendimento de um banco, usando os conceitos de **Agents**, **Tools**
e **Handoffs**.

## Ideia geral

O cliente manda uma mensagem em linguagem natural (ex: *"Faça um PIX
de R$ 50 para a Ana"*). Essa mensagem é recebida por um **Agente de
Atendimento**, que entende a intenção do cliente e faz um **handoff**
(passagem de bastão) para o agente especialista certo:

- **Agente PIX** → cuida de transferências PIX.
- **Agente de Dúvidas** → responde perguntas sobre o banco.

## Estrutura dos arquivos

```
banco_ia/
├── dados_ficticios.py   # "banco de dados" fictício (contatos, saldo, FAQ)
├── ferramentas.py       # tools que os agentes podem chamar
├── agentes.py           # definição dos 3 agentes e dos handoffs
├── main.py              # loop de conversa (programa principal)
└── requirements.txt     # dependência do projeto
```

### 1. `dados_ficticios.py`
Guarda tudo em memória (sem banco de dados de verdade):
- `conta_cliente`: saldo do cliente.
- `contatos`: lista de pessoas para quem dá pra fazer PIX.
- `historico_transacoes`: PIX que foram confirmados na sessão.
- `faq`: respostas prontas para o Agente de Dúvidas.

### 2. `ferramentas.py` (Tools)
Cada função com `@function_tool` é uma ferramenta que um agente pode
chamar sozinho, quando achar necessário:

- `consultar_saldo()` — devolve o saldo atual.
- `buscar_destinatario(nome)` — procura alguém na lista de contatos.
- `realizar_pix(nome, valor)` — confere destinatário e saldo, debita o
  valor e registra a transação (só deve ser chamada depois que o
  cliente confirmar).
- `consultar_duvida(assunto)` — busca a resposta certa na FAQ do banco.

### 3. `agentes.py` (Agents + Handoffs)
- **Agente de Atendimento**: não tem tools, só decide para qual
  especialista encaminhar a conversa (`handoffs=[agente_pix,
  agente_duvidas]`).
- **Agente PIX**: usa as tools de PIX. As instruções dele obrigam a
  sempre **mostrar os dados do PIX (nome, chave, valor) e pedir
  confirmação do cliente antes de executar a transferência**.
- **Agente de Dúvidas**: usa a tool `consultar_duvida` para responder
  com base na FAQ do banco.

### 4. `main.py`
Um loop simples de conversa no terminal. A cada mensagem do cliente,
chamamos `Runner.run(agente_atual, historico_conversa)`. O resultado
nos diz qual foi o último agente que respondeu (`resultado.last_agent`)
— isso é importante porque, depois de um handoff, a conversa passa a
rodar no agente especialista, e não mais no Agente de Atendimento.

## Como rodar

1. Instalar as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configurar a chave da API da OpenAI (necessária para o modelo
   entender a linguagem natural e decidir os handoffs/tools):
   ```bash
   export OPENAI_API_KEY="sua_chave_aqui"
   ```
3. Rodar o programa:
   ```bash
   python main.py
   ```

## Exemplo de conversa esperada

```
Você: Faça um PIX de R$ 50 para a Ana

[Agente PIX]: Encontrei a Ana na sua lista de contatos (chave PIX:
ana@email.com). Você confirma o envio de R$ 50,00 para ela?

Você: sim, confirmo

[Agente PIX]: PIX de R$ 50,00 para Ana realizado com sucesso! Novo
saldo: R$ 1450,00

Você: qual a tarifa do PIX?

[Agente de Dúvidas]: Nosso banco não cobra tarifa de manutenção de
conta nem tarifa para enviar PIX...

Você: sair
```

## Observações do trabalho

- Os dados (contatos, saldo) são fictícios e ficam apenas em memória
  (são reiniciados toda vez que o programa é executado).
- O foco do trabalho é mostrar a colaboração entre agentes usando
  **handoffs** (delegação de conversa) e **tools** (execução de ações
  no sistema), como pedido no enunciado.
- Por segurança, o Agente PIX foi instruído a **sempre pedir
  confirmação** ao cliente antes de executar a tool `realizar_pix`.
