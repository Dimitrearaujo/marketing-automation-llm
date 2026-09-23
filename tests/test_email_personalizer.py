import pytest

from automation.email_personalizer import montar_prompt

LEAD = {
    "nome": "João Silva",
    "cargo": "CEO",
    "empresa": "TechCorp",
    "porte_empresa": "mid-market",
    "empresa_setor": "tecnologia",
    "score": 85,
    "comportamentos": ["demo_solicitada"],
    "tem_budget": True,
}

ROTULO_ESTAGIO = {"hot": "QUENTE", "warm": "MORNO", "cold": "FRIO"}


@pytest.mark.parametrize("estagio", ["hot", "warm", "cold"])
def test_prompt_contem_nome_do_lead_e_estagio(estagio):
    prompt = montar_prompt(LEAD, estagio)
    assert "João Silva" in prompt
    assert estagio.upper() in prompt.upper() or ROTULO_ESTAGIO[estagio] in prompt
