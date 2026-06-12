# marketing-automation-llm

[![CI](https://github.com/dimitrearaujo/marketing-automation-llm/actions/workflows/ci.yml/badge.svg)](https://github.com/dimitrearaujo/marketing-automation-llm/actions/workflows/ci.yml)

Pipeline de automação de marketing com LLMs: lead scoring, personalização de emails e nutrição por estágio de funil.

Desenvolvido por **CD Tech** — automação e agentes IA para pequenos negócios.

---

## Visão Geral do Pipeline

```
Lead (JSON)
    │
    ▼
[1] Lead Scorer        ← pontua 0–100 por cargo, empresa e comportamento
    │
    ▼
[2] Funnel Router      ← classifica: cold / warm / hot + define próxima ação
    │
    ▼
[3] Email Personalizer ← monta prompt para LLM gerar email no tom certo
    │
    ▼
[4] Campaign Builder   ← sequência de touchpoints (email, WhatsApp, ligação)
```

Toda a lógica de negócio roda **sem API keys**. A integração com LLM (Anthropic Claude) é opcional e usada apenas para gerar o conteúdo final dos emails.

---

## Estrutura do Projeto

```
marketing-automation-llm/
├── automation/
│   ├── lead_scorer.py       # Pontuação de leads (0–100)
│   ├── funnel_router.py     # Classificação cold/warm/hot
│   ├── email_personalizer.py# Montagem de prompts para LLM
│   └── campaign_builder.py  # Sequência de touchpoints
├── examples/
│   └── leads_sample.json    # 3 leads de exemplo
├── main.py                  # Demo do pipeline completo
├── requirements.txt
└── .env.example
```

---

## Instalação

```bash
git clone https://github.com/dimitrearaujo/marketing-automation-llm.git
cd marketing-automation-llm
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
```

---

## Uso

### Executar o pipeline de demonstração

```bash
python main.py
```

### Usar os módulos individualmente

```python
from automation.lead_scorer import score_lead
from automation.funnel_router import rotear_lead
from automation.email_personalizer import montar_prompt, montar_payload_llm
from automation.campaign_builder import construir_campanha, resumo_campanha

lead = {
    "nome": "Ana Souza",
    "email": "ana@clinica.com",
    "cargo": "CEO",
    "empresa": "Clínica Vida",
    "porte_empresa": "smb",
    "empresa_setor": "saude",
    "comportamentos": ["demo_solicitada", "pagina_preco_visitada"],
    "tem_budget": True,
}

# 1. Pontuar
lead["score"] = score_lead(lead)
print(f"Score: {lead['score']}/100")

# 2. Rotear
roteamento = rotear_lead(lead)
print(f"Estágio: {roteamento['estagio']}")

# 3. Gerar email com LLM (requer ANTHROPIC_API_KEY)
import anthropic, os
payload = montar_payload_llm(lead, roteamento["estagio"])
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
resposta = client.messages.create(**payload)
print(resposta.content[0].text)

# 4. Montar campanha
campanha = construir_campanha(roteamento, roteamento["sequencia_completa"])
print(resumo_campanha(campanha))
```

---

## Exemplo de Output do Pipeline

```
============================================================
  MARKETING AUTOMATION PIPELINE — CD Tech
============================================================

[1/4] Pontuando leads...
  - Ana Souza                score:  85/100
  - Carlos Lima              score:  23/100
  - Mariana Rocha            score:   9/100

[2/4] Roteando leads no funil...
  - Ana Souza                estágio:  HOT | próxima ação: ligacao_comercial
  - Carlos Lima              estágio: COLD | próxima ação: email_educacional
  - Mariana Rocha            estágio: COLD | próxima ação: email_educacional

[3/4] Gerando prompts de email personalizados...
  - Ana Souza                prompt: Você é um especialista em vendas consultivas B2B...
  - Carlos Lima              prompt: Você é um especialista em inbound marketing...

[4/4] Construindo campanhas...
Campanha: camp_ana_souza_clinica_com
Lead: Ana Souza (ana@clinica.com)
Estágio: HOT | Score: 85/100
Total de touchpoints: 4
  1. [2026-06-12] TELEFONE — Ligação comercial urgente — Ana Souza
  2. [2026-06-13]    EMAIL — Proposta personalizada para Clínica Vida — válida por 5 dias
  ...
```

---

## Integração com n8n ou Make (Webhook Trigger)

Exponha o pipeline como webhook para receber leads automaticamente de formulários, CRMs ou anúncios.

### n8n

1. Crie um nó **Webhook** no n8n (método POST)
2. Copie a URL gerada para `WEBHOOK_URL` no `.env`
3. No nó seguinte, use **Execute Command** ou **HTTP Request** para chamar `main.py` com o payload do lead
4. Ou use o nó **Python** (n8n Cloud) diretamente importando os módulos

```json
// Payload esperado no webhook
{
  "nome": "João Silva",
  "email": "joao@empresa.com",
  "cargo": "Diretor",
  "empresa": "Empresa ABC",
  "porte_empresa": "mid-market",
  "empresa_setor": "tecnologia",
  "comportamentos": ["email_aberto", "site_visitado"],
  "tem_budget": false
}
```

### Make (Integromat)

1. Crie um cenário com trigger **Webhooks > Custom Webhook**
2. Adicione um módulo **HTTP > Make a Request** apontando para seu servidor onde o pipeline roda
3. Mapeie os campos do formulário/CRM para o payload JSON acima

---

## Integração com HubSpot / RD Station

### HubSpot

```python
import requests, os

def sincronizar_hubspot(lead: dict, score: int, estagio: str):
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {os.environ['HUBSPOT_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "properties": {
            "email": lead["email"],
            "firstname": lead["nome"].split()[0],
            "lead_score": score,
            "lifecyclestage": "lead" if estagio == "cold" else "marketingqualifiedlead" if estagio == "warm" else "salesqualifiedlead",
        }
    }
    requests.post(url, json=payload, headers=headers)
```

### RD Station

```python
import requests, os

def sincronizar_rdstation(lead: dict, score: int):
    url = f"https://api.rd.services/platform/contacts"
    headers = {"Authorization": f"Bearer {os.environ['RD_STATION_TOKEN']}"}
    payload = {
        "email": lead["email"],
        "name": lead["nome"],
        "cf_lead_score": score,
        "tags": [f"automation-llm"],
    }
    requests.post(url, json=payload, headers=headers)
```

---

## Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `ANTHROPIC_API_KEY` | Só para geração de email | Chave da API Anthropic |
| `LLM_MODEL` | Não | Modelo Claude (padrão: `claude-opus-4-5`) |
| `HUBSPOT_API_KEY` | Não | Integração HubSpot CRM |
| `RD_STATION_TOKEN` | Não | Integração RD Station |
| `WEBHOOK_URL` | Não | Endpoint para receber leads via n8n/Make |

---

## Desenvolvido por

**CD Tech** — automação e agentes IA para pequenos negócios  
Fortaleza CE | [dimitrearaujo@gmail.com](mailto:dimitrearaujo@gmail.com)
