"""
main.py — Demonstração do pipeline completo de marketing automation.

Executa o pipeline sem necessidade de API keys:
  1. Score dos leads
  2. Roteamento por estágio do funil
  3. Montagem dos prompts de email
  4. Construção das campanhas
"""

import json
import os
from pathlib import Path

from automation.lead_scorer import score_batch
from automation.funnel_router import rotear_batch
from automation.email_personalizer import montar_prompt
from automation.campaign_builder import construir_campanha, resumo_campanha


def carregar_leads(caminho: str = "examples/leads_sample.json") -> list[dict]:
    path = Path(caminho)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def executar_pipeline(leads: list[dict]) -> None:
    print("=" * 60)
    print("  MARKETING AUTOMATION PIPELINE — CD Tech")
    print("=" * 60)

    # Etapa 1: Lead Scoring
    print("\n[1/4] Pontuando leads...")
    leads_scored = score_batch(leads)
    for lead in leads_scored:
        print(f"  - {lead['nome']:25s} score: {lead['score']:>3}/100")

    # Etapa 2: Roteamento de funil
    print("\n[2/4] Roteando leads no funil...")
    leads_roteados = rotear_batch(leads_scored)
    for lead in leads_roteados:
        print(
            f"  - {lead['nome']:25s} estágio: {lead['estagio'].upper():>4} "
            f"| próxima ação: {lead['proxima_acao']}"
        )

    # Etapa 3: Prompts de email
    print("\n[3/4] Gerando prompts de email personalizados...")
    for lead in leads_roteados:
        prompt = montar_prompt(lead, lead["estagio"])
        preview = prompt.split("\n")[0]
        print(f"  - {lead['nome']:25s} prompt: {preview[:60]}...")

    # Etapa 4: Campanhas
    print("\n[4/4] Construindo campanhas...")
    for lead in leads_roteados:
        campanha = construir_campanha(lead, lead["sequencia_completa"])
        print(f"\n{resumo_campanha(campanha)}")

    print("\n" + "=" * 60)
    print("  Pipeline concluído com sucesso!")
    print("=" * 60)


def main() -> None:
    leads = carregar_leads()
    executar_pipeline(leads)


if __name__ == "__main__":
    main()
