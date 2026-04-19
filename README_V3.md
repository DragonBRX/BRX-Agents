# BRX-AGENT v3.0 - Sistema Multi-Agente Dinamico

![Arquitetura BRX](architecture.png)

## Agente Auto-Evolutivo Multi-Cerebro + 100+ Agentes Especializados

O BRX e um agente de inteligencia artificial com arquitetura unica que combina:
- **8 mentes base** que funcionam como uma equipe de especialistas (sempre ativas)
- **100+ agentes especializados** que sao ativados dinamicamente conforme a tarefa
- Sistema de **orquestracao inteligente** que seleciona os melhores especialistas
- **Workspace colaborativo** onde todos os agentes veem o trabalho dos outros em tempo real

---

## O que ha de novo na v3.0?

### Sistema Multi-Agente Dinamico
- **100+ agentes especializados** em 12 categorias diferentes
- Ativacao automatica baseada na analise da tarefa
- Numero configuravel de agentes simultaneos (padrao: 8, max: 16)
- Todos os agentes trabalham em paralelo usando threads
- Visibilidade cruzada: cada agente ve o que os outros estao fazendo

### Categorias de Agentes
| Categoria | Quantidade | Exemplos |
|-----------|-----------|----------|
| Development | 30+ | Backend, Frontend, Mobile, Game, AI/ML, Blockchain |
| Design | 15+ | UI, UX, 3D, Motion, Graphic, Accessibility |
| Content | 12+ | Technical Writer, Copywriter, SEO, Newsletter |
| Data | 10+ | Data Engineer, Data Scientist, MLOps, Visualization |
| Security | 8+ | AppSec, Penetration Tester, Cloud Security, Compliance |
| Infrastructure | 12+ | DevOps, SRE, Cloud Architect, Kubernetes |
| Business | 8+ | Product Manager, Agile Coach, Growth Hacker |
| Research | 8+ | AI Researcher, Market Research, User Research |
| Creative | 20+ | Music Producer, Video, Photography, Concept Art |
| Communication | 5+ | Customer Support, Community Manager |
| Quality | 6+ | QA Analyst, Automation Engineer, Performance |
| Project | 5+ | Technical PM, Scrum Master |

### Como Funciona

```
Usuario: "Criar um site profissional de portfolio"

[Analisador de Tarefas]
  Detecta: website, profissional, portfolio
  Categorias: DEVELOPMENT, DESIGN
  
[Orquestrador]
  Ativa agentes especializados:
  - Bianca (Frontend Developer)
  - Arthur (Backend Developer)  
  - Isabela (UI Designer)
  - Juliana (UX Designer)
  - Carlos (Fullstack Developer)
  - Lara (Motion Designer)
  - Mia (Accessibility Specialist)
  - Lucas (QA Analyst)

[Execucao Paralela - 8 threads]
  Todos os agentes trabalham simultaneamente
  Cada um ve o progresso dos outros
  
[Workspace Colaborativo]
  - Contribuicoes visiveis em tempo real
  - Reacoes cruzadas entre agentes
  - Decisoes tomadas coletivamente
  
[Resultado Consolidado]
  - Consenso das 8 mentes base
  + Contribuicoes dos agentes especializados
  = Resposta completa e especializada
```

---

## Comando Unico de Instalacao e Execucao

```bash
curl -sO https://raw.githubusercontent.com/DragonBRX/BRX-Agents/main/brx_run.sh && chmod +x brx_run.sh && ./brx_run.sh
```

---

## Uso do Chat v3.0

### Iniciar o chat
```bash
python brx_chat_v3.py
```

### Comandos de Agente

```
/agents                    - Lista todos os 100+ agentes
/agents development        - Filtra por categoria
/agent dev_frontend        - Detalhes de um agente especifico
/categories                - Mostra categorias disponiveis
/analyze <tarefa>          - Analisa sem executar
/task <tarefa>             - Processa com equipe especializada
/multiagent on             - Ativa modo multi-agente
/multiagent off            - Desativa (modo legacy)
/maxagents 12              - Define numero de agentes
/workspace                 - Mostra workspace colaborativo
```

### Exemplos de Tarefas

```
[BRX] Criar um e-commerce com React e Node.js
      -> Ativa: Frontend, Backend, Fullstack, UI, UX, E-commerce, QA

[BRX] Desenvolver um app mobile de delivery
      -> Ativa: Mobile, Backend, UI, UX, QA, DevOps

[BRX] Criar identidade visual para minha startup
      -> Ativa: Graphic Designer, UI, UX, Copywriter

[BRX] Fazer analise de dados de vendas
      -> Ativa: Data Analyst, Data Scientist, Visualization

[BRX] Construir pipeline de CI/CD
      -> Ativa: DevOps, SRE, Cloud, Security

[BRX] Criar um jogo 2D plataforma
      -> Ativa: Game Dev, Concept Art, Game UI, Sound Designer
```

---

## Configuracao de Agentes

### Padrao de Threads
O BRX detecta automaticamente quantos threads seu CPU tem:
- **16+ threads**: 12 agentes
- **8-15 threads**: 8 agentes (padrao)
- **4-7 threads**: 4 agentes
- **1-3 threads**: 2 agentes

### Personalizar Quantidade
```bash
# 4 agentes
python brx_chat_v3.py --max-agents 4

# 12 agentes
python brx_chat_v3.py --max-agents 12

# No chat
/maxagents 6
```

---

## Solucao para o Erro: externally-managed-environment

O comando unico acima ja resolve este erro automaticamente. Para comandos manuais:

```bash
cd BRX-Agents
./venv/bin/python3 -m pip install -r requirements.txt

# Modo autonomo
./venv/bin/python3 brx_autonomous.py

# Chat interativo v3.0
./venv/bin/python3 brx_chat_v3.py

# Chat com 12 agentes
./venv/bin/python3 brx_chat_v3.py --max-agents 12
```

---

## Caracteristicas Principais

### Arquitetura de 8 Mentes Base (sempre ativas)
- **Designer**: Estrutura e padroes de dados
- **Analista**: Logica e consistencia tecnica
- **Inovador**: Abordagens criativas e novas perspectivas
- **Critico**: Identificacao de falhas e riscos (Red Teaming)
- **Revisor**: Qualidade textual e clareza
- **Validador**: Coerencia tematica e precisao
- **Estrategista**: Planejamento e utilidade pratica
- **Memoria**: Contexto historico e persistencia

### Sistema Multi-Agente (ativado por tarefa)
- **100+ agentes** em 12 categorias
- **Personalidade unica** para cada agente (precise, creative, pragmatic, analytical, etc.)
- **Skills especificas** por agente
- **Linguagens e ferramentas** especializadas
- **Ativacao inteligente** baseada em palavras-chave da tarefa
- **Execucao paralela** com threads
- **Visibilidade cruzada** no workspace

---

**"A inteligencia nao e apenas processar informacoes, mas evoluir a forma como processamos - agora com especialistas dinamicos."** - BRX v3.0
