from automation.lead_scorer import score_lead


def test_lead_quente_com_comportamentos_fortes_score_alto():
    lead_hot = {
        "cargo": "CEO",
        "porte_empresa": "enterprise",
        "comportamentos": ["demo_solicitada", "pagina_preco_visitada", "case_lido"],
        "tem_budget": True,
        "empresa_setor": "saude",
    }
    assert score_lead(lead_hot) > 70


def test_lead_sem_dados_score_baixo():
    assert score_lead({}) < 30
