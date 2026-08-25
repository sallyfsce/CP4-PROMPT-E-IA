"""
Este arquivo guarda os "dados fictícios" do nosso banco, tudo em memória
(dicionários e listas do Python). Não usamos banco de dados de verdade,
pois o objetivo do trabalho é praticar Agents, Tools e Handoffs.
"""

# Conta do cliente que está usando o sistema.
# Vamos simular apenas UMA conta, a do usuário.
conta_cliente = {
    "titular": "Você",
    "saldo": 1500.00,
}

# Lista de contatos (destinatários) que o cliente pode usar para fazer PIX.
# Cada contato tem um nome e uma chave PIX fictícia.
contatos = [
    {"nome": "Ana", "chave_pix": "ana@email.com"},
    {"nome": "Bruno", "chave_pix": "11999990001"},
    {"nome": "Carla", "chave_pix": "carla@email.com"},
    {"nome": "Diego", "chave_pix": "22999990002"},
    {"nome": "Eduarda", "chave_pix": "eduarda@email.com"},
]

# Histórico de transações realizadas na sessão atual.
# Cada PIX confirmado é adicionado nessa lista.
historico_transacoes = []

# Perguntas frequentes usadas pelo Agente de Dúvidas.
faq = {
    "pix": "O PIX é um meio de pagamento instantâneo. Você pode enviar PIX "
           "24 horas por dia, todos os dias, e o dinheiro cai na conta do "
           "destinatário em poucos segundos, sem nenhuma tarifa.",
    "tarifa": "Nosso banco não cobra tarifa de manutenção de conta nem "
               "tarifa para enviar PIX. Transferências (TED) têm uma tarifa "
               "de R$ 5,00 por operação.",
    "cartao": "Oferecemos cartão de débito e crédito sem anuidade. O limite "
               "do cartão de crédito é definido de acordo com a análise de "
               "crédito do cliente.",
    "conta": "Nossa conta digital é gratuita, sem tarifa de manutenção, e "
              "pode ser aberta totalmente pelo aplicativo do banco.",
    "emprestimo": "Trabalhamos com empréstimo pessoal com taxas a partir de "
                   "1,5% ao mês, sujeito à análise de crédito.",
    "horario": "O aplicativo do banco funciona 24 horas por dia. Já o "
                "atendimento humano funciona de segunda a sexta, das 8h às "
                "20h.",
}
