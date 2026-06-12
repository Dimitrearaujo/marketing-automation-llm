"""
Email Personalizer — monta prompts personalizados para geração de email via LLM.
Formata o prompt; não realiza chamadas de API.
"""

from __future__ import annotations

TEMPLATES_PROMPT: dict[str, str] = {
    "hot": """\
Você é um especialista em vendas consultivas B2B.

Escreva um email de abordagem DIRETA para {nome}, que é {cargo} na empresa {empresa}.
O lead está no estágio QUENTE do funil (score {score}/100) e já demonstrou forte interesse.

Contexto do lead:
- Empresa: {empresa} ({porte_empresa})
- Setor: {empresa_setor}
- Comportamentos recentes: {comportamentos}
- Tem budget declarado: {tem_budget}

O email deve:
1. Reconhecer o interesse demonstrado pelo lead
2. Propor uma reunião ou demo nos próximos 2 dias
3. Destacar 1 resultado específico que empresas do mesmo setor obtiveram
4. Ter CTA claro com link de agendamento
5. Ser conciso (máximo 150 palavras)

Tom: profissional, direto, sem rodeios. Assunto do email incluso.
""",
    "warm": """\
Você é um especialista em marketing de conteúdo B2B.

Escreva um email de nutrição para {nome}, que é {cargo} na empresa {empresa}.
O lead está no estágio MORNO do funil (score {score}/100) — está considerando a solução.

Contexto do lead:
- Empresa: {empresa} ({porte_empresa})
- Setor: {empresa_setor}
- Comportamentos recentes: {comportamentos}

O email deve:
1. Abordar uma dor específica do setor {empresa_setor}
2. Apresentar um caso de sucesso relevante
3. Oferecer um conteúdo de valor (guia, calculadora ou checklist)
4. CTA suave: "Veja como funciona" ou "Baixe o material"
5. Máximo 200 palavras

Tom: educativo, empático, sem pressão de venda. Assunto do email incluso.
""",
    "cold": """\
Você é um especialista em inbound marketing.

Escreva um email de boas-vindas/educação para {nome}, que é {cargo} na empresa {empresa}.
O lead está no estágio FRIO do funil (score {score}/100) — ainda descobrindo o problema.

Contexto do lead:
- Empresa: {empresa} ({porte_empresa})
- Setor: {empresa_setor}

O email deve:
1. Apresentar um problema comum no setor {empresa_setor} de forma provocativa
2. Mostrar que existe uma solução (sem vender diretamente)
3. Compartilhar 1 insight ou estatística relevante
4. CTA para conteúdo educativo (blog post, vídeo, podcast)
5. Máximo 180 palavras

Tom: consultivo, curioso, sem menção a preço ou produto. Assunto do email incluso.
""",
}


def montar_prompt(lead: dict, estagio: str) -> str:
    """
    Monta o prompt personalizado para geração de email via LLM.

    Parâmetros:
        lead (dict): dados do lead (nome, cargo, empresa, etc.)
        estagio (str): 'hot', 'warm' ou 'cold'

    Retorna:
        str: prompt formatado pronto para enviar ao LLM
    """
    template = TEMPLATES_PROMPT.get(estagio, TEMPLATES_PROMPT["cold"])

    comportamentos = lead.get("comportamentos", [])
    comportamentos_str = (
        ", ".join(comportamentos) if comportamentos else "nenhum registrado"
    )

    return template.format(
        nome=lead.get("nome", "Lead"),
        cargo=lead.get("cargo", "não informado"),
        empresa=lead.get("empresa", "não informada"),
        porte_empresa=lead.get("porte_empresa", "não informado"),
        empresa_setor=lead.get("empresa_setor", "não informado"),
        score=lead.get("score", 0),
        comportamentos=comportamentos_str,
        tem_budget="Sim" if lead.get("tem_budget") else "Não informado",
    )


def montar_payload_llm(lead: dict, estagio: str, modelo: str = "claude-opus-4-5") -> dict:
    """
    Monta o payload completo para chamada à API do LLM (Anthropic Messages API).
    Não realiza a chamada — apenas estrutura o objeto.

    Retorna dict compatível com anthropic.messages.create(**payload)
    """
    prompt = montar_prompt(lead, estagio)

    return {
        "model": modelo,
        "max_tokens": 600,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }
