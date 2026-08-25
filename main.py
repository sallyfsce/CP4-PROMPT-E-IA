"""
Programa principal do sistema de atendimento do banco fictício.

Como funciona:
- O cliente digita uma mensagem (ex: "Faça um PIX de R$ 50 para a Ana").
- Essa mensagem sempre começa com o Agente de Atendimento.
- O Agente de Atendimento faz um handoff para o agente especialista
  correto (Agente PIX ou Agente de Dúvidas), que continua a conversa.
- A conversa continua rodando nesse mesmo agente até o cliente digitar
  algo que faça mais sentido para outro agente (o SDK cuida disso
  automaticamente através dos handoffs).

Para rodar:
    1. Instale as dependências:  pip install -r requirements.txt
    2. Configure sua chave da OpenAI:  export OPENAI_API_KEY="sua_chave"
    3. Execute:  python main.py
"""

import asyncio

from agents import Runner
from agentes import agente_atendimento
import dados_ficticios as dados


async def main():
    print("=" * 60)
    print("Banco Fictício - Sistema de Atendimento Inteligente")
    print("=" * 60)
    print("Digite sua mensagem (ou 'sair' para encerrar).\n")

    # Agente que está atendendo o cliente no momento. No início, é
    # sempre o Agente de Atendimento. Depois de um handoff, o SDK
    # devolve qual foi o "último agente" que respondeu, e usamos ele
    # para continuar a conversa no próximo turno.
    agente_atual = agente_atendimento

    # Histórico da conversa, no formato que o Runner entende.
    historico_conversa = []

    while True:
        mensagem_usuario = input("Você: ").strip()

        if mensagem_usuario.lower() in ("sair", "exit", "quit"):
            print("\nAtendimento encerrado. Até logo!")
            break

        if not mensagem_usuario:
            continue

        # Adiciona a nova mensagem do usuário ao histórico.
        historico_conversa.append({"role": "user", "content": mensagem_usuario})

        '''
        Executa o agente atual com todo o histórico da conversa.
        '''

        resultado = await Runner.run(agente_atual, historico_conversa)

        print(f"\n[{resultado.last_agent.name}]: {resultado.final_output}\n")

        # Atualiza o histórico e o agente atual para o próximo turno,
        # já considerando um possível handoff que tenha acontecido.
        historico_conversa = resultado.to_input_list()
        agente_atual = resultado.last_agent


def mostrar_estado_final():
    """Mostra o saldo final e o histórico de PIX feitos na sessão."""
    print("-" * 60)
    print("Resumo da sessão")
    print(f"Saldo final: R$ {dados.conta_cliente['saldo']:.2f}".replace(".", ","))
    if dados.historico_transacoes:
        print("Transações realizadas:")
        for transacao in dados.historico_transacoes:
            valor_str = f"R$ {transacao['valor']:.2f}".replace(".", ",")
            print(f"  - {valor_str} para {transacao['destinatario']}")
    else:
        print("Nenhuma transação realizada nesta sessão.")
    print("-" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        mostrar_estado_final()
