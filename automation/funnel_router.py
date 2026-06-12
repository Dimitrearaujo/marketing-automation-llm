"""
Funnel Router — classifica leads por estágio do funil e define próxima ação.
Lógica totalmente local, sem chamadas de API.
"""

from __future__ import annotations

ESTAGIOS = {
    "hot": {
        "min_score": 71,
        "label": "Quente",
        "descricao": "Lead pronto para abordagem comercial direta",
        "proxima_acao": "ligacao_comercial",
        "sla_horas": 2,
    },
    "warm": {
        "min_score": 40,
        "label": "Morno",
        "descricao": "Lead em nutrição ativa, próximo à decisão",
        "proxima_acao": "email_nurturing_avancado",
        "sla_horas": 24,
    },
    "cold": {
        "min_score": 0,
        "label": "Frio",
        "descricao": "Lead no topo do funil, precisa de educação",
        "proxima_acao": "email_educacional",
        "sla_horas": 72,
    },
}

SEQUENCIAS: dict[str, list[str]] = {
    "hot": [
        "ligacao_comercial",
        "envio_proposta",
        "follow_up_proposta",
        "fechamento",
    ],
    "warm": [
        "email_case_sucesso",
        "email_demo_convite",
        "email_preco_personalizado",
        "ligacao_qualificacao",
    ],
    "cold": [
        "email_boas_vindas",
        "email_problema_solucao",
        "email_educacional_1",
        "email_educacional_2",
        "email_social_proof",
    ],
}


def classificar_estagio(score: int) -> str:
    """Retorna o estágio do funil ('hot', 'warm' ou 'cold') com base no score."""
    if score > 70:
        return "hot"
    elif score >= 40:
        return "warm"
    return "cold"


def rotear_lead(lead: dict) -> dict:
    """
    Classifica o lead no funil e retorna roteamento completo.

    Parâmetros esperados:
        score (int): pontuação do lead (0-100)
        nome (str): nome do lead
        email (str): email do lead

    Retorna dict com:
        estagio, label, proxima_acao, sla_horas, sequencia_completa
    """
    score = int(lead.get("score", 0))
    estagio = classificar_estagio(score)
    config = ESTAGIOS[estagio]

    return {
        "nome": lead.get("nome", ""),
        "email": lead.get("email", ""),
        "score": score,
        "estagio": estagio,
        "label": config["label"],
        "descricao": config["descricao"],
        "proxima_acao": config["proxima_acao"],
        "sla_horas": config["sla_horas"],
        "sequencia_completa": SEQUENCIAS[estagio],
    }


def rotear_batch(leads: list[dict]) -> list[dict]:
    """Roteia uma lista de leads."""
    return [rotear_lead(lead) for lead in leads]
