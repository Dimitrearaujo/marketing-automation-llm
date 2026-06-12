"""
marketing-automation-llm — Pipeline de automação de marketing com LLMs.
"""

from .lead_scorer import score_lead, score_batch
from .funnel_router import classificar_estagio, rotear_lead, rotear_batch
from .email_personalizer import montar_prompt, montar_payload_llm
from .campaign_builder import construir_campanha, resumo_campanha

__all__ = [
    "score_lead",
    "score_batch",
    "classificar_estagio",
    "rotear_lead",
    "rotear_batch",
    "montar_prompt",
    "montar_payload_llm",
    "construir_campanha",
    "resumo_campanha",
]
