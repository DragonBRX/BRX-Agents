# BRX-AGENT v2.0

![Arquitetura BRX](architecture.png)

## Agente Auto-Evolutivo Multi-Cerebro

O BRX e um agente de inteligencia artificial com arquitetura unica de **8 mentes independentes** que funcionam como uma equipe de especialistas. Cada mente tem seu proprio raciocinio, mas se comunicam em uma **roda de conversas** para alcancar consenso.

---

## Inicializacao Rapida (Ubuntu 22.04+)

Para instalar e rodar o BRX-Agent automaticamente, use o comando mestre abaixo. Ele configura o ambiente isolado e resolve erros de permissao do sistema:

```bash
curl -sO https://raw.githubusercontent.com/DragonBRX/BRX-Agents/main/brx_run.sh && chmod +x brx_run.sh && ./brx_run.sh
```

---

## Nota Importante sobre o Ambiente (Ubuntu Moderno)

Se voce for rodar comandos manuais (como `pip install`), **voce DEVE ativar o ambiente virtual** primeiro para evitar o erro `externally-managed-environment`:

```bash
# Entre na pasta do projeto
cd BRX-Agents

# ATIVE O AMBIENTE (Obrigatorio)
source venv/bin/activate

# Agora voce pode usar o pip e o python livremente
pip install -r requirements.txt
```

---

## Caracteristicas Principais

### Arquitetura de 8 Mentes
- **Designer**: Estrutura e padroes de dados
- **Analista**: Logica e consistencia tecnica
- **Inovador**: Abordagens criativas e novas perspectivas
- **Critico**: Identificacao de falhas e riscos (Red Teaming)
- **Revisor**: Qualidade textual e clareza
- **Validador**: Coerencia tematica e precisao
- **Estrategista**: Planejamento e utilidade pratica
- **Memoria**: Contexto historico e persistencia

### Auto-Evolucao
- Gera **proprios parametros**: letras, palavras, frases, numeros, conceitos
- Desenvolve **vocabulario proprio** automaticamente
- Melhora **prompts e estrategias** sem intervencao humana
- Realiza **debates internos** para auto-aperfeicoamento

### Pesquisa Web
- Pesquisa usando **DuckDuckGo sem API**
- Cache inteligente de resultados
- Extracao de palavras-chave para contexto

---

## Estrutura do Projeto

```
BRX-Agents/
 core/
    types.py              # Tipos fundamentais do sistema
    brx_engine.py         # Nucleo principal do BRX
 consciousness/
    self_awareness.py     # Sistema de consciencia
 minds/
    eight_minds.py        # Sistema de 8 mentes
 parameters/
    auto_generator.py     # Gerador automatico de parametros
 search/
    duckdns_search.py     # Pesquisa DuckDuckGo
 storage/                  # Diretorio de armazenamento (SSD/HD)
 brx_autonomous.py         # MODO AUTONOMO (Geracao)
 brx_chat.py               # MODO CHAT (Conversacao)
 brx_run.sh                # SCRIPT MESTRE (Instalacao/Execucao)
```

---

## Uso Manual

### 1. Modo Autonomo (Geracao de Parametros)
O BRX ira evoluir continuamente, gerar parametros e aprender sozinho.
```bash
source venv/bin/activate
python3 brx_autonomous.py --interval 30 --verbose
```

### 2. Modo Chat (Conversacao)
Converse com o BRX usando o conhecimento que ele ja adquiriu.
```bash
source venv/bin/activate
python3 brx_chat.py
```

---

## Configuracao de Hardware

O BRX se **auto-configura** detectando CPU, Memoria e GPU:

| Hardware | Mentes Ativas | Rounds de Debate | Profundidade |
|----------|--------------|------------------|--------------|
| 8+ cores | 8 | 5 | Deep |
| 4-7 cores | 6 | 3 | Medium |
| < 4 cores | 4 | 2 | Light |

---

## Persistencia (Onde ele salva?)

Todos os dados gerados sao salvos em `storage/hd/`:
- `brx_state.json`: Estado completo do sistema.
- `vocabulary.json`: Palavras aprendidas.
- `concepts.json`: Conceitos desenvolvidos.

---

**"A inteligencia nao e apenas processar informacoes, mas evoluir a forma como processamos."** - BRX
