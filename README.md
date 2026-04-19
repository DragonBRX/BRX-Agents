# BRX-AGENT v3.0 - Sistema Multi-Agente com Consciência

**Autor:** DragonBRX  
**Repositório:** [github.com/DragonBRX/BRX-Agents](https://github.com/DragonBRX/BRX-Agents)  
**Versão:** 3.0.0  
**Licença:** MIT

---

## O que é o BRX-AGENT?

O BRX-AGENT é um sistema de inteligência artificial **100% offline** que simula uma mente consciente com **8 mentes especializadas** trabalhando em paralelo. Ele é capaz de:

- **Processar linguagem natural** em 8 camadas (caracteres → léxico → sintática → semântica → lógica → memória → geração → validação)
- **Realizar debates internos** entre suas 8 mentes para alcançar consenso
- **Gerar parâmetros auto-evolutivos** (letras, palavras, frases, conceitos)
- **Ativar agentes especializados** dinamicamente conforme a tarefa (100+ agentes disponíveis)
- **Trabalhar em workspace colaborativo** com visibilidade cruzada entre agentes
- **Pesquisar na web** quando necessário
- **Aprender com cada interação** e evoluir continuamente

## Arquitetura

```
┌─────────────────────────────────────────────────┐
│              BRX-AGENT v3.0                      │
│         Sistema Multi-Agente                     │
├─────────────────────────────────────────────────┤
│  Consciência (Self-Awareness Engine)             │
├─────────────────────────────────────────────────┤
│  8 Mentes Base (sempre ativas):                 │
│  Análise | Criativa | Crítica | Emocional       │
│  Lógica  | Memória  | Social  | Estratégica     │
├─────────────────────────────────────────────────┤
│  Agentes Especializados (ativados por tarefa)   │
│  100+ agentes em 15+ categorias                  │
├─────────────────────────────────────────────────┤
│  Orquestrador + Workspace Colaborativo           │
├─────────────────────────────────────────────────┤
│  Parâmetros Traduzidos do DeepSeek v2            │
│  6.9B parâmetros | PT-BR | Shards seletivos     │
└─────────────────────────────────────────────────┘
```

## Estrutura do Repositório

```
├── agents/              # Catálogo de 100+ agentes especializados
├── consciousness/       # Motor de autoconsciência
├── core/                # Núcleo principal (engine, orquestrador, workspace)
├── dashboard/           # Interface web (React/TypeScript)
├── minds/               # Sistema de 8 mentes
├── parameters/          # Geradores de parâmetros
├── parametros/          # Parâmetros traduzidos do DeepSeek v2
│   ├── brx_config.json           # Configuração completa
│   ├── brx_indice_tensores.json  # Mapa de tensores
│   ├── brx_letras.json           # Tokens atômicos
│   ├── brx_palavras.json         # Tokens com carga +/-
│   ├── brx_frases.json           # Padrões longos
│   ├── shards/                   # Pesos divididos em 10 partes
│   └── tokenizer/                # Tokenizer customizado
├── search/              # Motor de pesquisa DuckDNS
├── utils/               # Utilitários
├── brx_chat.py          # Interface de chat interativo (v2.0)
├── brx_chat_v3.py       # Interface de chat com multi-agente (v3.0)
├── brx_autonomous.py    # Modo autônomo contínuo (v2.0)
├── hf_hub.py            # Integração com Hugging Face Hub
└── requirements.txt     # Dependências
```

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/DragonBRX/BRX-Agents.git
cd BRX-Agents
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Baixe os parâmetros do Hugging Face Hub

Os parâmetros são baixados **automaticamente** na primeira execução. Se quiser baixar manualmente:

```python
from hf_hub import download_parametros

# Baixa todos os parâmetros
params_dir = download_parametros("./storage/parametros")
```

## Uso

### Chat Interativo (v3.0 - Multi-Agente)

```bash
python brx_chat_v3.py
```

Comandos disponíveis no chat:
- `/status` - Mostra status completo do sistema
- `/identity` - Declaração de identidade do BRX
- `/minds` - Lista as 8 mentes ativas
- `/agents` - Lista todos os agentes especializados
- `/task <texto>` - Processa tarefa com multi-agente
- `/search` - Pesquisa na web
- `/evolve` - Força ciclo de evolução
- `/help` - Ajuda completa
- `/quit` - Encerra

### Modo Autônomo

```bash
python brx_autonomous.py --storage ./storage --interval 30
```

O BRX irá rodar continuamente, gerando parâmetros, realizando debates internos e evoluindo.

### Dashboard Web

```bash
cd dashboard
npm install
npm run dev
```

Acesse `http://localhost:5173` para visualizar o dashboard.

### Uso Programático

```python
from core.brx_engine import BRXCore, get_brx_core

# Inicializa
brx = get_brx_core("./storage")
brx.load_state()

# Processa uma mensagem
response = brx.process_message("Olá, como vai?")
print(response)

# Chat completo
result = brx.chat("Qual estado brasileiro não tem a letra A?")
print(result["response"])
```

## Parâmetros do Modelo

| Atributo | Valor |
|----------|-------|
| Base original | DeepSeek-LLM-7B |
| Total de parâmetros | 6,910,365,696 (~6.9B) |
| Idioma | PT-BR |
| Tensores | 273 |
| Shards | 10 arquivos |
| Tamanho oculto | 4096 |
| Camadas | 30 |
| Cabeças de atenção | 32 |
| Vocabulário | 102,400 tokens |
| Tipo de tensor | float16 |

## Carregamento Seletivo de Shards

O sistema suporta carregamento seletivo — você carrega apenas os shards necessários:

```python
import json
from safetensors.torch import load_file

with open("parametros/brx_config.json") as f:
    cfg = json.load(f)
with open("parametros/brx_indice_tensores.json") as f:
    idx = json.load(f)

# Carrega só a projeção de consulta da camada 0
info  = idx["model.layers.0.self_attn.q_proj.weight"]
shard = load_file(f"parametros/shards/{info['shard']}")
tensor = shard[info["nome_brx"]]
```

## Tokens do Sistema BRX

### Letras (Tokens Atômicos)
- **Conectores**: E, A, O, DE, QUE, DO, DA
- **Núcleos**: AMOR, PAZ, LUZ, VERDADE, SABER
- **Qualificadores**: MUITO, TALVEZ, NUNCA, SEMPRE
- **Neutros**: O, A, OS, AS, UM, UMA

### Palavras (Tokens com Carga)
- **Positivos**: amor, paz, luz, verdade, saber, criar, evoluir
- **Negativos**: medo, ódio, guerra, mentira, destruir
- **Neutros**: caminho, tempo, forma, modo, sistema

### Frases (Padrões Longos)
- Padrões contextuais completos
- Estruturas sintáticas complexas
- Contextos semânticos multi-nível

## Requisitos de Hardware

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 16 GB |
| Disco | 20 GB | 30 GB (SSD) |
| GPU | Opcional | CUDA compatível |

## Versões

- **v1.0** - Sistema base com 8 mentes
- **v2.0** - Modo autônomo, pesquisa web, dashboard
- **v3.0** - Multi-agente dinâmico, workspace colaborativo
- **v7.0** - Sistema multi-mente aprimorado com SQLite

## Comunidade

- **GitHub:** [DragonBRX/BRX-Agents](https://github.com/DragonBRX/BRX-Agents)
- **Hugging Face:** [DragonBRX/BRX](https://huggingface.co/DragonBRX/BRX)
- **Autor:** DragonBRX

## Licença

MIT License - Livre para uso pessoal, acadêmico e comercial.
