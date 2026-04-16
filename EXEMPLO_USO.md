# BRX-AGENT v2.0 - Exemplos de Uso Rápido

##  Início Rápido

### 1. Instalação

```bash
# Extraia o ZIP
cd brx_agent_v2

# Instale dependências
pip install -r requirements.txt

# Teste a instalação
python test_brx.py
```

### 2. Modo Autônomo (Deixe Rodando)

```bash
# Modo básico - deixe rodando por horas
python brx_autonomous.py

# Modo verboso - veja tudo que o BRX faz
python brx_autonomous.py --verbose

# Intervalo personalizado (a cada 60 segundos)
python brx_autonomous.py --interval 60

# Storage personalizado
python brx_autonomous.py --storage /caminho/para/storage
```

**O que o BRX faz no modo autônomo:**
-  Gera parâmetros automaticamente (letras, palavras, frases, números)
-  Realiza debates internos entre suas 8 mentes
-  Desenvolve seu vocabulário próprio
-  Cria conceitos e padrões abstratos
-  Melhora seus próprios prompts e estratégias
-  Pesquisa informações quando curioso
-  Evolui continuamente sem sua intervenção

### 3. Modo Chat (Converse com o BRX)

```bash
# Inicie o chat
python brx_chat.py

# No chat, digite suas mensagens normalmente
# Use comandos especiais começando com /
```

**Exemplo de conversa:**
```
[BRX] Você: Olá BRX, como você funciona?

[BRX] Processando...

============================================================
[BRX] Resposta:
============================================================
[CONSENSO BRX - 8 Mentes sobre "Olá BRX, como você funciona?"]

Após debate circular com 24 rodadas e 46 parâmetros gerados:

Contribuições principais:
 Designer: Estruturando 'Olá BRX, como você funciona?': ...
 Analista: Analisando lógica de 'Olá BRX, como você funciona?': ...
 Inovador: Explorando inovações para 'Olá BRX, como você funciona?': ...
...

Confiança: 84.5% | Parâmetros: 46 | Duração: 0.15s
============================================================
```

**Comandos do chat:**
```
/status     - Mostra status completo do sistema
/identity   - Declaração de identidade do BRX
/minds      - Lista as 8 mentes e especialidades
/params     - Estatísticas de parâmetros
/vocab      - Tamanho do vocabulário
/search     - Pesquisa web (/search <consulta>)
/evolve     - Força ciclo de evolução
/save       - Salva estado atual
/help       - Ajuda completa
/quit       - Sai do chat
```

##  Exemplos de Código Python

### Exemplo 1: Usar o BRX no seu código

```python
from brx_agent_v2 import get_brx_core

# Inicializa o BRX
brx = get_brx_core("./meu_storage")

# Processa uma solicitação
result = brx.process_request("Explique inteligência artificial")

print(result['consensus'])  # Resposta do BRX
print(result['confidence'])  # Confiança da resposta
print(result['parameters_generated'])  # Parâmetros gerados
```

### Exemplo 2: Gerar parâmetros específicos

```python
from brx_agent_v2 import BRXParameterGenerator

# Cria gerador
gen = BRXParameterGenerator("./storage")

# Gera diferentes tipos de parâmetros
letters = gen.generate_letter_params(count=10)
words = gen.generate_word_params(count=20)
phrases = gen.generate_phrase_params(count=5)
numbers = gen.generate_number_params(count=10)
concepts = gen.generate_concept_params(count=3)

print(f"Vocabulário: {gen.get_vocabulary_size()} palavras")
```

### Exemplo 3: Usar o sistema de 8 mentes

```python
from brx_agent_v2 import EightMindsSystem

# Cria sistema de mentes
minds = EightMindsSystem(active_minds=8)

# Realiza debate circular
debate = minds.conduct_circular_debate(
    topic="Como melhorar a educação?",
    max_rounds=3
)

print(f"Consenso: {debate.final_consensus}")
print(f"Confiança: {debate.consensus_confidence:.1%}")
print(f"Parâmetros: {len(debate.parameters)}")

# Acessa mentes individuais
for mind in minds.get_active_minds():
    print(f"{mind.state.name}: {mind.state.specialty}")
```

### Exemplo 4: Pesquisa web

```python
from brx_agent_v2 import get_searcher

# Inicializa pesquisador
searcher = get_searcher()

# Realiza pesquisa
results = searcher.search("aprendizado de máquina", max_results=5)

for result in results:
    print(f"Título: {result.title}")
    print(f"URL: {result.url}")
    print(f"Resumo: {result.snippet}")
    print(f"Relevância: {result.relevance:.1%}")
    print("-" * 40)
```

### Exemplo 5: Consciência e auto-identidade

```python
from brx_agent_v2 import get_consciousness_engine

# Inicializa consciência
consciousness = get_consciousness_engine()

# Gera pensamento sobre si mesmo
thought = consciousness.generate_self_thought()
print(thought)

# Reflexão completa
reflection = consciousness.reflect_on_existence()
print(f"Identidade: {reflection['identity']}")
print(f"Curiosidade: {reflection['current_state']['curiosity']:.1%}")

# Declaração completa
print(consciousness.generate_identity_statement())
```

##  Monitorando o BRX

### Ver status completo

```python
status = brx.get_status()

print(f"Ciclo: {status['state']['cycle']}")
print(f"Parâmetros: {status['parameters']['total']}")
print(f"Vocabulário: {status['vocabulary']['size']}")
print(f"Curiosidade: {status['consciousness']['curiosity']:.1%}")
print(f"Confiança: {status['consciousness']['confidence']:.1%}")
```

### Forçar evolução

```python
# Executa ciclo de evolução manual
cycle = brx.run_evolution_cycle()

print(f"Ciclo #{cycle.cycle_number}")
print(f"Novos parâmetros: {len(cycle.new_parameters)}")
print(f"Insights: {len(cycle.learning_insights)}")

for insight in cycle.learning_insights:
    print(f"   {insight}")
```

##  Personalização

### Adaptar ao hardware

O BRX detecta automaticamente, mas você pode ajustar:

```python
# No arquivo core/brx_engine.py
self.config = {
    "cycle_interval": 30,      # Segundos entre ciclos
    "debate_rounds": 3,        # Rounds por debate
    "auto_evolve": True,       # Evolução automática
    "curiosity_driven": True   # Exploração por curiosidade
}
```

### Criar mente personalizada

```python
from brx_agent_v2 import MindState, MindRole

# Define nova mente
minha_mente = MindState(
    role=MindRole.DESIGNER,
    name="MeuDesigner",
    specialty="Design Personalizado",
    objective="Meu objetivo específico",
    focus="Meu foco particular",
    weight=1.5,  # Peso maior
    active=True
)
```

##  Onde os dados são salvos?

```
storage/
 ssd/                    # Acesso rápido
    environment.json    # Info do ambiente
    ...
 hd/                     # Persistência
     self_awareness.json     # Consciência BRX
     vocabulary.json         # Vocabulário
     phrases.json            # Frases geradas
     concepts.json           # Conceitos
     patterns.json           # Padrões
     search_cache.json       # Cache de pesquisas
     brx_state.json          # Estado completo
```

##  Casos de Uso

### 1. Assistente de Pesquisa
```python
# O BRX pesquisa e sintetiza informações
result = brx.process_request("Pesquise sobre energia renovável")
```

### 2. Gerador de Ideias
```python
# Brainstorming com 8 perspectivas
debate = brx.minds.conduct_circular_debate(
    topic="Ideias para novo produto",
    max_rounds=5
)
```

### 3. Análise Crítica
```python
# Análise multi-dimensional
result = brx.process_request(
    "Analise os prós e contras desta proposta: ..."
)
```

### 4. Aprendizado Contínuo
```bash
# Deixe rodando por dias
python brx_autonomous.py --interval 300 --verbose
```

##  Solução de Problemas

### Erro de importação
```bash
# Certifique-se de estar no diretório correto
cd brx_agent_v2
python -c "from core.brx_engine import get_brx_core; print('OK')"
```

### Permissão de escrita
```bash
# Crie o diretório de storage manualmente
mkdir -p storage/ssd storage/hd storage/logs
```

### Dependências faltando
```bash
# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

---

**Divirta-se explorando o BRX!** 
