from automation.campaign_builder import construir_campanha
from automation.funnel_router import SEQUENCIAS


def test_construir_campanha_gera_touchpoints_e_preserva_dados_do_lead():
    lead = {
        "nome": "Maria Santos",
        "email": "maria@empresa.com",
        "empresa": "Empresa X",
        "empresa_setor": "saude",
        "estagio": "warm",
        "score": 55,
    }

    campanha = construir_campanha(lead, SEQUENCIAS["warm"])

    assert len(campanha["touchpoints"]) >= 3
    assert campanha["lead_nome"] == "Maria Santos"
    assert campanha["estagio"] == "warm"
