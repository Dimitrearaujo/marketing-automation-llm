"""
Lead Scorer — pontua leads de 0 a 100 com base em atributos.
Lógica totalmente local, sem chamadas de API.
"""

from __future__ import annotations

CARGO_SCORES: dict[str, int] = {
    "ceo": 30,
    "cto": 28,
    "coo": 26,
    "diretor": 22,
    "gerente": 15,
    "coordenador": 10,
    "analista": 6,
    "estagiario": 2,
    "assistente": 4,
}

EMPRESA_SCORES: dict[str, int] = {
    "enterprise": 20,
    "mid-market": 15,
    "smb": 10,
    "startup": 8,
    "autonomo": 4,
}

COMPORTAMENTO_SCORES: dict[str, int] = {
    "demo_solicitada": 20,
    "pagina_preco_visitada": 15,
    "case_lido": 10,
    "webinar_assistido": 8,
    "email_aberto": 5,
    "site_visitado": 3,
}


def score_lead(lead: dict) -> int:
    """
    Calcula pontuação de 0 a 100 para um lead.

    Parâmetros esperados no dict:
        cargo (str): cargo do lead (ex: "CEO", "Gerente")
        porte_empresa (str): porte da empresa (ex: "enterprise", "smb")
        comportamentos (list[str]): lista de ações realizadas
        empresa_setor (str, opcional): setor da empresa
        tem_budget (bool, opcional): se há orçamento disponível

    Retorna:
        int: score de 0 a 100
    """
    total = 0

    # Pontuação por cargo
    cargo = str(lead.get("cargo", "")).lower().strip()
    for key, pts in CARGO_SCORES.items():
        if key in cargo:
            total += pts
            break

    # Pontuação por porte da empresa
    porte = str(lead.get("porte_empresa", "")).lower().strip()
    for key, pts in EMPRESA_SCORES.items():
        if key in porte:
            total += pts
            break

    # Pontuação por comportamentos
    comportamentos = lead.get("comportamentos", [])
    if isinstance(comportamentos, list):
        for comportamento in comportamentos:
            c = str(comportamento).lower().strip()
            pts = COMPORTAMENTO_SCORES.get(c, 0)
            total += pts

    # Bônus: tem budget declarado
    if lead.get("tem_budget") is True:
        total += 10

    # Bônus: setor prioritário
    setor = str(lead.get("empresa_setor", "")).lower()
    setores_prioritarios = ["saude", "educacao", "financeiro", "tecnologia", "varejo"]
    if any(s in setor for s in setores_prioritarios):
        total += 5

    return min(total, 100)


def score_batch(leads: list[dict]) -> list[dict]:
    """Pontua uma lista de leads e retorna cada um com o campo 'score' preenchido."""
    result = []
    for lead in leads:
        scored = dict(lead)
        scored["score"] = score_lead(lead)
        result.append(scored)
    return result
