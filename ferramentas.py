"""
Aqui ficam as "tools" (ferramentas) que os agentes podem chamar.
Cada função marcada com @function_tool vira uma ferramenta que o
agente da OpenAI Agents SDK consegue usar para executar ações reais
no nosso banco fictício (consultar saldo, achar contato, fazer PIX, etc).
"""

from agents import function_tool
import dados_ficticios as dados


@function_tool
def consultar_saldo() -> str:
    """Consulta o saldo atual da conta do cliente."""
    saldo = dados.conta_cliente["saldo"]
    return f"O saldo atual da conta é R$ {saldo:.2f}".replace(".", ",")


@function_tool
def buscar_destinatario(nome_destinatario: str) -> str:
    """
    Procura um destinatário na lista de contatos do cliente pelo nome.

    Args:
        nome_destinatario: nome (ou parte do nome) da pessoa que vai
            receber o PIX, por exemplo "Ana".
    """
    nome_procurado = nome_destinatario.strip().lower()

    for contato in dados.contatos:
        if nome_procurado in contato["nome"].lower():
            return (
                f"Destinatário encontrado: {contato['nome']} "
                f"(chave PIX: {contato['chave_pix']})"
            )

    return (
        f"Não encontrei nenhum contato chamado '{nome_destinatario}' "
        "na lista de contatos do cliente."
    )


@function_tool
def realizar_pix(nome_destinatario: str, valor: float) -> str:
    """
    Realiza um PIX simulado: verifica se o destinatário existe, se há
    saldo suficiente e, se estiver tudo certo, debita o valor da conta
    e registra a transação no histórico.

    Só deve ser chamada DEPOIS que o cliente confirmar a transação.

    Args:
        nome_destinatario: nome do destinatário do PIX.
        valor: valor em reais que será enviado.
    """
    nome_procurado = nome_destinatario.strip().lower()

    # 1) Verifica se o destinatário existe na lista de contatos.
    contato_encontrado = None
    for contato in dados.contatos:
        if nome_procurado in contato["nome"].lower():
            contato_encontrado = contato
            break

    if contato_encontrado is None:
        return (
            f"Não foi possível concluir o PIX: destinatário "
            f"'{nome_destinatario}' não está na lista de contatos."
        )

    # 2) Verifica se o valor é válido.
    if valor <= 0:
        return "Não foi possível concluir o PIX: o valor deve ser maior que zero."

    # 3) Verifica se há saldo suficiente.
    if valor > dados.conta_cliente["saldo"]:
        saldo_atual = dados.conta_cliente["saldo"]
        return (
            "Não foi possível concluir o PIX: saldo insuficiente. "
            f"Saldo disponível: R$ {saldo_atual:.2f}".replace(".", ",")
        )

    # 4) Tudo certo: debita o valor e registra a transação.
    dados.conta_cliente["saldo"] -= valor
    dados.historico_transacoes.append(
        {"destinatario": contato_encontrado["nome"], "valor": valor}
    )

    novo_saldo = dados.conta_cliente["saldo"]
    return (
        f"PIX de R$ {valor:.2f} para {contato_encontrado['nome']} "
        f"realizado com sucesso! Novo saldo: R$ {novo_saldo:.2f}"
    ).replace(".", ",")


@function_tool
def consultar_duvida(assunto: str) -> str:
    """
    Consulta a base de perguntas frequentes (FAQ) do banco sobre um
    assunto, por exemplo: "pix", "tarifa", "cartao", "conta",
    "emprestimo" ou "horario".

    Args:
        assunto: palavra-chave do assunto que o cliente quer saber.
    """
    assunto_procurado = assunto.strip().lower()

    for palavra_chave, resposta in dados.faq.items():
        if palavra_chave in assunto_procurado or assunto_procurado in palavra_chave:
            return resposta

    return (
        "Não encontrei essa informação na nossa base de perguntas "
        "frequentes. Assuntos disponíveis: pix, tarifa, cartao, conta, "
        "emprestimo e horario."
    )
