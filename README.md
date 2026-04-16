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

## Solucao para o Erro: externally-managed-environment

Se voce tentar usar o `pip` e receber este erro, e porque o Ubuntu esta protegendo o sistema. Siga estes passos exatos para resolver:

### 1. Criar o Ambiente (Se ainda nao existir)
```bash
cd BRX-Agents
python3 -m venv venv
```

### 2. Instalar usando o modulo do Python (O Segredo)
Em vez de usar apenas `pip`, use o comando abaixo que força o uso do ambiente isolado:
```bash
./venv/bin/python3 -m pip install -r requirements.txt
```

### 3. Rodar o Modelo
```bash
# Modo Autonomo
./venv/bin/python3 brx_autonomous.py

# Modo Chat
./venv/bin/python3 brx_chat.py
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

**"A inteligencia nao e apenas processar informacoes, mas evoluir a forma como processamos."** - BRX
