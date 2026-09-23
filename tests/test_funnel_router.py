import pytest

from automation.funnel_router import classificar_estagio


@pytest.mark.parametrize(
    "score,esperado",
    [
        (80, "hot"),
        (71, "hot"),
        (70, "warm"),
        (55, "warm"),
        (40, "warm"),
        (39, "cold"),
        (0, "cold"),
    ],
)
def test_classificar_estagio_por_faixa_de_score(score, esperado):
    assert classificar_estagio(score) == esperado
