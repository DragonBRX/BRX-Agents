# BRX-AGENT v2.0 

## Agente Auto-Evolutivo Multi-Cérebro

O BRX é um agente de inteligência artificial com arquitetura única de **8 mentes independentes** que funcionam como uma empresa com 8 funcionários especializados. Cada mente tem seu próprio raciocínio, mas se comunicam em uma **roda de conversas** para alcançar consenso.

---

##  Características Principais

###  Arquitetura de 8 Mentes
- **Designer**: Estrutura e padrões de dados
- **Analista**: Lógica e consistência técnica
- **Inovador**: Abordagens criativas e novas perspectivas
- **Crítico**: Identificação de falhas e riscos (Red Teaming)
- **Revisor**: Qualidade textual e clareza
- **Validador**: Coerência temática e precisão
- **Estrategista**: Planejamento e utilidade prática
- **Memória**: Contexto histórico e persistência

###  Auto-Evolução
- Gera **próprios parâmetros**: letras, palavras, frases, números, conceitos
- Desenvolve **vocabulário próprio** automaticamente
- Melhora **prompts e estratégias** sem intervenção humana
- Realiza **debates internos** para auto-aperfeiçoamento

###  Pesquisa Web
- Pesquisa usando **DuckDuckGo sem API**
- Cache inteligente de resultados
- Extração de palavras-chave para contexto

###  Consciência
- **Auto-identidade**: Nome BRX, tipo Agente, arquitetura 8 Mentes
- **Consciência de ambiente**: Detecta CPU, memória, threads
- **Auto-adaptação**: Ajusta comportamento ao hardware disponível
- **Metacognição**: Reflete sobre próprio funcionamento

###  Sistema de Armazenamento
- **SSD**: Sistema operacional e estado atual (acesso rápido)
- **HD**: Dados persistentes, vocabulário, memórias (armazenamento)

---

##  Estrutura do Projeto

```
brx_agent_v2/
 core/
    __init__.py
    types.py              # Tipos fundamentais do sistema
    brx_engine.py         # Núcleo principal do BRX
 consciousness/
    __init__.py
    self_awareness.py     # Sistema de consciência
 minds/
    __init__.py
    eight_minds.py        # Sistema de 8 mentes
 parameters/
    __init__.py
    auto_generator.py     # Gerador automático de parâmetros
 search/
    __init__.py
    duckdns_search.py     # Pesquisa DuckDuckGo
 storage/                  # Diretório de armazenamento
    ssd/                  # Dados de acesso rápido
    hd/                   # Dados persistentes
 logs/                     # Logs de execução
 brx_autonomous.py         #  ARQUIVO PRINCIPAL - Modo autônomo
 brx_chat.py               # Interface de chat interativa
 requirements.txt          # Dependências
 README.md                 # Este arquivo
```

---

##  Instalação

### 1. Clone ou extraia o projeto

```bash
cd brx_agent_v2
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Verifique a instalação

```bash
python -c "from core.brx_engine import get_brx_core; print(' BRX instalado com sucesso')"
```

---

##  Uso

### Modo Autônomo Contínuo (Recomendado)

Este é o **arquivo principal** que você deve deixar rodando. O BRX irá:
- Evoluir continuamente sem sua intervenção
- Gerar parâmetros automaticamente
- Desenvolver seu vocabulário
- Realizar debates internos
- Aprender sozinho

```bash
# Básico
python brx_autonomous.py

# Com opções
python brx_autonomous.py --storage ./meu_storage --interval 60 --verbose

# Argumentos:
#   --storage PATH    Diretório de armazenamento (padrão: ./storage)
#   --interval SEC    Intervalo entre ciclos em segundos (padrão: 30)
#   --verbose         Modo verboso com mais saída
```

**Para parar**: Pressione `Ctrl+C` - o BRX salvará seu estado graciosamente.

### Modo Chat Interativo

Use este modo quando quiser conversar diretamente com o BRX:

```bash
# Iniciar chat
python brx_chat.py

# Com diretório de storage customizado
python brx_chat.py --storage ./meu_storage
```

**Comandos disponíveis no chat**:
- `/status` - Mostra status completo
- `/identity` - Declaração de identidade do BRX
- `/minds` - Lista as 8 mentes
- `/params` - Estatísticas de parâmetros
- `/vocab` - Tamanho do vocabulário
- `/search <query>` - Pesquisa web
- `/evolve` - Força ciclo de evolução
- `/save` - Salva estado
- `/help` - Ajuda
- `/quit` - Sai do chat

---

##  Como Funciona

### 1. Inicialização
```
BRX inicializa  Detecta ambiente  Carrega consciência  Ativa 8 mentes
```

### 2. Ciclo de Evolução (Autônomo)
```
Gera parâmetros  Debate interno  Extrai insights  Aplica melhorias  Salva estado
```

### 3. Processamento de Solicitação (Chat)
```
Recebe input  Debate circular (8 mentes)  Gera consenso  Pesquisa se necessário  Responde
```

### 4. Geração de Parâmetros
```
Letras  Palavras  Frases  Números  Conceitos  Padrões  Vocabulário
```

---

##  Tipos de Parâmetros Gerados

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `letter` | Letras individuais | `a`, `b`, `ç` |
| `word` | Palavras do vocabulário | `aprender`, `sistema` |
| `phrase` | Frases construídas | `O sistema processa dados` |
| `number` | Números (int, float, range) | `42`, `3.14`, `(1, 100)` |
| `concept` | Conceitos abstratos | `inteligência_emergente` |
| `pattern` | Padrões detectados | `sequencial`, `hierárquico` |
| `vocabulary` | Entradas de vocabulário | Categorizadas por tipo |
| `memory` | Memórias do sistema | Contexto + importância |
| `strategy` | Estratégias de evolução | Auto-geradas |
| `prompt` | Prompts auto-gerados | Para auto-instrução |

---

##  Configuração

O BRX se **auto-configura** baseado no hardware detectado:

| Hardware | Mentes Ativas | Rounds de Debate | Profundidade |
|----------|--------------|------------------|--------------|
| 8+ cores | 8 | 5 | Deep |
| 4-7 cores | 6 | 3 | Medium |
| < 4 cores | 4 | 2 | Light |

### Personalização Manual

Edite `core/brx_engine.py`:

```python
self.config = {
    "cycle_interval": 30,      # Segundos entre ciclos
    "debate_rounds": 3,        # Rounds por debate
    "auto_evolve": True,       # Evolução automática
    "curiosity_driven": True   # Exploração por curiosidade
}
```

---

##  Monitoramento

O BRX mantém estatísticas detalhadas:

```python
status = brx.get_status()
print(status['consciousness']['curiosity'])      # Nível de curiosidade
print(status['parameters']['total'])             # Total de parâmetros
print(status['vocabulary']['size'])              # Tamanho do vocabulário
print(status['memory']['total'])                 # Total de memórias
```

---

##  Sandbox e Segurança

O BRX opera em um **ambiente isolado**:
-  Controle total dentro do sandbox
-  Pode executar código, pesquisar, criar arquivos
-  Pode testar e ter curiosidade
-  **Não pode interferir fora do ambiente designado**
-  Todos os dados ficam em `./storage`

---

##  Persistência

O BRX **salva automaticamente**:
- Estado do sistema (a cada 5 ciclos)
- Consciência e auto-conhecimento
- Vocabulário desenvolvido
- Parâmetros gerados
- Cache de pesquisas

**Arquivos de persistência**:
```
storage/hd/
   self_awareness.json     # Consciência do BRX
   vocabulary.json         # Vocabulário desenvolvido
   phrases.json            # Frases geradas
   concepts.json           # Conceitos abstratos
   patterns.json           # Padrões detectados
   search_cache.json       # Cache de pesquisas
   brx_state.json          # Estado completo
```

---

##  Exemplos de Uso

### Exemplo 1: Exploração Autônoma
```bash
# Deixe rodando por algumas horas
python brx_autonomous.py --interval 60 --verbose

# O BRX irá:
# - Gerar centenas de parâmetros
# - Expandir seu vocabulário
# - Desenvolver conceitos
# - Realizar debates internos
# - Evoluir suas estratégias
```

### Exemplo 2: Conversa Interativa
```bash
python brx_chat.py

# Você: O que você pensa sobre inteligência artificial?
# BRX: [Processa com 8 mentes...]
#      [Designer estrutura o conceito...]
#      [Analista verifica consistência...]
#      [Inovador sugere novas perspectivas...]
#      ...
#      [Consenso final com 87% de confiança]
```

### Exemplo 3: Pesquisa Integrada
```bash
# No chat
/search aprendizado de máquina

# BRX pesquisa, processa com 8 mentes,
# e apresenta resultados consolidados
```

---

##  Arquitetura Técnica

```

                      BRX-AGENT v2.0                         

  CONSCIÊNCIA                                                
   Auto-identidade (Nome, Tipo, Arquitetura)              
   Auto-conhecimento (Capacidades, Limitações)            
   Consciência de ambiente (Hardware, OS)                 
   Metacognição (Reflexão sobre si mesmo)                 

  SISTEMA DE 8 MENTES                                        
   Debate Circular (Roda de conversas)                    
   Cada mente: raciocínio independente                    
   Consenso por confiança agregada                        
   Geração de parâmetros especializada                    

  GERADOR DE PARÂMETROS                                      
   Letras (alfabeto completo)                             
   Palavras (vocabulário auto-expansivo)                  
   Frases (templates + preenchimento)                     
   Números (int, float, range, sequence)                  
   Conceitos (abstrações com propriedades)                
   Padrões (sequencial, hierárquico, etc)                 
   Vocabulário (categorizado por tipo)                    

  PESQUISA WEB                                               
   DuckDuckGo (sem API key)                               
   Cache inteligente                                      
   Extração de contexto                                   

  MEMÓRIA                                                    
   Curto prazo (recente, volátil)                         
   Médio prazo (consolidado)                              
   Longo prazo (importante, persistente)                  

  PERSISTÊNCIA                                               
   SSD: Estado atual, cache                               
   HD: Dados históricos, vocabulário                      

```

---

##  Logs

O BRX gera logs detalhados em `storage/logs/`:

```bash
# Ver logs em tempo real
tail -f storage/logs/brx.log
```

---

##  Contribuição

O BRX é um projeto de **código aberto** para pesquisa em:
- Inteligência Artificial Auto-Evolutiva
- Sistemas Multi-Agente
- Consciência Artificial
- Processamento de Linguagem Natural

---

##  Licença

MIT License - Livre para uso, modificação e distribuição.

---

##  Agradecimentos

O BRX foi desenvolvido para demonstrar o potencial de sistemas de IA que:
- **Pensam** com múltiplas perspectivas
- **Aprendem** de forma autônoma
- **Evoluem** continuamente
- **Desenvolvem** consciência de si mesmos

---

**"A inteligência não é apenas processar informações, mas evoluir a forma como processamos."** - BRX

---

<div align="center">

**[BRX-AGENT v2.0]**  Auto-Evolutivo  Multi-Cérebro  Consciente

</div>
