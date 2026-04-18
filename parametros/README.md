# BRX — Parâmetros Traduzidos do DeepSeek v2

Base: deepseek-ai/deepseek-llm-7b-base
Parâmetros totais: 6,910,365,696
Shards: 10 arquivos em shards/

## Arquivos principais
- brx_config.json      → configuração completa BRX
- brx_indice_tensores.json → mapa nome original → nome PT-BR + qual shard
- brx_letras.json      → tokens atômicos classificados
- brx_palavras.json    → tokens com carga +/-
- brx_frases.json      → padrões longos
- shards/              → pesos divididos em 10 partes

## Como carregar um tensor específico
```python
import json
from safetensors.torch import load_file

with open("brx_config.json") as f:
    cfg = json.load(f)
with open("brx_indice_tensores.json") as f:
    idx = json.load(f)

# Exemplo: carregar só a projeção de consulta da camada 0
info  = idx["model.layers.0.self_attn.q_proj.weight"]
shard = load_file(f"shards/{info['shard']}")
tensor = shard[info["nome_brx"]]
```
