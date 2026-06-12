"""
Campaign Builder — monta estrutura de campanha com sequência de touchpoints.
Lógica totalmente local, sem chamadas de API.
"""

from __future__ import annotations

from datetime import datetime, timedelta

TOUCHPOINT_CONFIGS: dict[str, dict] = {
    "email_boas_vindas": {
        "canal": "email",
        "tipo": "educacional",
        "delay_dias": 0,
        "assunto_modelo": "Bem-vindo, {nome} — como {empresa_setor} resolve X com automação",
    },
    "email_educacional_1": {
        "canal": "email",
        "tipo": "educacional",
        "delay_dias": 3,
        "assunto_modelo": "O erro que 80% das empresas de {empresa_setor} cometem",
    },
    "email_educacional_2": {
        "canal": "email",
        "tipo": "educacional",
        "delay_dias": 7,
        "assunto_modelo": "Case: como {empresa_setor} aumentou receita em 30%",
    },
    "email_social_proof": {
        "canal": "email",
        "tipo": "social_proof",
        "delay_dias": 12,
        "assunto_modelo": "O que empresas como {empresa} estão fazendo diferente",
    },
    "email_problema_solucao": {
        "canal": "email",
        "tipo": "educacional",
        "delay_dias": 5,
        "assunto_modelo": "Você já parou para calcular quanto isso custa por mês?",
    },
    "email_case_sucesso": {
        "canal": "email",
        "tipo": "social_proof",
        "delay_dias": 2,
        "assunto_modelo": "Como {empresa_setor} economizou 15h/semana com automação",
    },
    "email_demo_convite": {
        "canal": "email",
        "tipo": "conversao",
        "delay_dias": 5,
        "assunto_modelo": "{nome}, posso te mostrar isso em 20 minutos?",
    },
    "email_preco_personalizado": {
        "canal": "email",
        "tipo": "conversao",
        "delay_dias": 9,
        "assunto_modelo": "Proposta exclusiva para {empresa}",
    },
    "ligacao_qualificacao": {
        "canal": "telefone",
        "tipo": "qualificacao",
        "delay_dias": 12,
        "assunto_modelo": "Ligação de qualificação — {nome}",
    },
    "ligacao_comercial": {
        "canal": "telefone",
        "tipo": "venda",
        "delay_dias": 0,
        "assunto_modelo": "Ligação comercial urgente — {nome}",
    },
    "envio_proposta": {
        "canal": "email",
        "tipo": "proposta",
        "delay_dias": 1,
        "assunto_modelo": "Proposta personalizada para {empresa} — válida por 5 dias",
    },
    "follow_up_proposta": {
        "canal": "whatsapp",
        "tipo": "follow_up",
        "delay_dias": 3,
        "assunto_modelo": "Follow-up: proposta para {nome}",
    },
    "fechamento": {
        "canal": "telefone",
        "tipo": "fechamento",
        "delay_dias": 5,
        "assunto_modelo": "Decisão final — {nome} / {empresa}",
    },
}


def construir_touchpoint(nome_touchpoint: str, lead: dict, data_inicio: datetime) -> dict:
    """Constrói um touchpoint individual da campanha."""
    config = TOUCHPOINT_CONFIGS.get(nome_touchpoint, {})
    delay = config.get("delay_dias", 0)
    data_envio = data_inicio + timedelta(days=delay)

    assunto = config.get("assunto_modelo", nome_touchpoint).format(
        nome=lead.get("nome", "Lead"),
        empresa=lead.get("empresa", "sua empresa"),
        empresa_setor=lead.get("empresa_setor", "seu setor"),
    )

    return {
        "ordem": None,  # preenchido no build_campaign
        "nome": nome_touchpoint,
        "canal": config.get("canal", "email"),
        "tipo": config.get("tipo", "educacional"),
        "data_envio": data_envio.strftime("%Y-%m-%d"),
        "assunto": assunto,
        "status": "agendado",
    }


def construir_campanha(lead: dict, sequencia: list[str]) -> dict:
    """
    Monta a estrutura completa de campanha para um lead.

    Parâmetros:
        lead (dict): dados do lead (nome, empresa, estagio, score, etc.)
        sequencia (list[str]): lista de nomes de touchpoints na ordem correta

    Retorna:
        dict com metadados da campanha e lista de touchpoints
    """
    data_inicio = datetime.now()
    touchpoints = []

    for i, nome in enumerate(sequencia):
        tp = construir_touchpoint(nome, lead, data_inicio)
        tp["ordem"] = i + 1
        touchpoints.append(tp)

    estagio = lead.get("estagio", "cold")
    score = lead.get("score", 0)

    return {
        "campanha_id": f"camp_{lead.get('email', 'lead').replace('@', '_').replace('.', '_')}",
        "lead_nome": lead.get("nome", ""),
        "lead_email": lead.get("email", ""),
        "estagio": estagio,
        "score": score,
        "total_touchpoints": len(touchpoints),
        "duracao_dias": touchpoints[-1]["data_envio"] if touchpoints else "0",
        "data_inicio": data_inicio.strftime("%Y-%m-%d"),
        "touchpoints": touchpoints,
    }


def resumo_campanha(campanha: dict) -> str:
    """Retorna string legível com o resumo da campanha."""
    lines = [
        f"Campanha: {campanha['campanha_id']}",
        f"Lead: {campanha['lead_nome']} ({campanha['lead_email']})",
        f"Estágio: {campanha['estagio'].upper()} | Score: {campanha['score']}/100",
        f"Total de touchpoints: {campanha['total_touchpoints']}",
        "",
        "Sequência:",
    ]
    for tp in campanha["touchpoints"]:
        lines.append(
            f"  {tp['ordem']:>2}. [{tp['data_envio']}] {tp['canal'].upper():>10} — {tp['assunto']}"
        )
    return "\n".join(lines)
