# BRX-Agent v7.0 - Sistema Multi-Mente Aprimorado

## Visão Geral

O BRX-Agent v7.0 é um sistema autônomo multi-agente com 12 especialistas, consciência expandida, busca web inteligente e persistência robusta de conhecimento.

## Novidades da v7.0

### 12 Agentes Especialistas
- **Engenheiro** - Arquitetura de software
- **CientistaDados** - Análise estatística
- **CISO** - Segurança e riscos
- **Economista** - Viabilidade financeira
- **Psicologo** - Experiência do usuário
- **Filosofo** - Ética e lógica
- **CPO** - Estratégia de produto
- **PesquisadorML** - Machine Learning
- **DevOps** - Infraestrutura e CI/CD (NOVO)
- **Blockchain** - Tecnologia blockchain (NOVO)
- **CloudArchitect** - Computação em nuvem (NOVO)
- **DataEngineer** - Engenharia de dados (NOVO)

### Banco de Dados JSON
- Base de conhecimento estruturada em JSON
- 12 domínios de conhecimento
- Padrões, métricas e frameworks organizados
- Fácil extensão e manutenção

### Persistência Robusta
- SQLite com WAL mode
- Sistema de tokens de treinamento
- Cache de busca web
- Parâmetros com metadados ricos

### Busca Web Inteligente
- DuckDuckGo sem API key
- Múltiplas estratégias de parse
- Cache inteligente
- Fallback automático

## Instalação

```bash
# Clone o repositório
git clone https://github.com/DragonBRX/BRX-Agents.git
cd BRX-Agents

# Instale as dependências
pip install -r requirements.txt
```

## Uso

### Modo Completo
```bash
python brx_autonomous_v7.py
```

### Tópicos Específicos
```bash
python brx_autonomous_v7.py --topicos "ia,ml,cloud"
```

### Sem Web Search
```bash
python brx_autonomous_v7.py --no-web --rodadas 10
```

### Modo Interativo
```bash
python brx_autonomous_v7.py --interativo
```

## Estrutura do Projeto

```
BRX-Agents/
├── core/
│   ├── brx_engine_v7.py          # Motor principal v7.0
│   ├── knowledge_base_v7.json    # Base de conhecimento
│   └── brx_engine.py             # Versão anterior (mantida)
├── agents/                        # Agentes especialistas
├── parameters/
│   ├── auto_generator_v7.py      # Gerador de parâmetros v7.0
│   └── auto_generator.py         # Versão anterior (mantida)
├── consciousness/
│   ├── self_awareness_v7.py      # Consciência v7.0
│   └── self_awareness.py         # Versão anterior (mantida)
├── search/                        # Busca web
├── utils/                         # Utilitários
├── docs/                          # Documentação
├── tests/                         # Testes
├── brx_autonomous_v7.py          # Entry point v7.0
├── brx_autonomous.py             # Versão anterior (mantida)
└── README_V7.md                  # Este arquivo
```

## Comandos do Modo Interativo

- `pensar [tópico]` - Gera um pensamento
- `aprender` - Registra aprendizado
- `status` - Mostra status do sistema
- `processar [tópico]` - Processa com 12 agentes
- `parametros` - Estatísticas de parâmetros
- `ajuda` - Mostra ajuda
- `sair` - Encerra

## Banco de Dados

O sistema utiliza SQLite com:
- Tabela `parametros` - Parâmetros gerados
- Tabela `criticas` - Críticas entre agentes
- Tabela `ciclos_debate` - Histórico de debates
- Tabela `memoria_global` - Memória compartilhada
- Tabela `agente_performance` - Performance dos agentes
- Tabela `busca_web_cache` - Cache de buscas
- Tabela `tokens_treinamento` - Tokens de treinamento

## Configuração

As configurações estão em `core/brx_engine_v7.py`:

```python
@dataclass
class BRXConfig:
    MAX_WORKERS: int = 12
    NUM_RODADAS_PADRAO: int = 20
    WEB_SEARCH_ENABLED: bool = True
    THRESHOLD_POSITIVO: float = 0.60
    THRESHOLD_NEGATIVO: float = 0.35
```

## Requisitos

- Python 3.8+
- requests
- beautifulsoup4
- psutil
- colorama (opcional)

## Licença

MIT License
