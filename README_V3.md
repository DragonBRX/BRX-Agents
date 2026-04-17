# BRX-AGENT v3.0 🧠

## Sistema de Processamento de Linguagem Natural 100% Offline

O BRX-Agent v3.0 é um sistema de inteligência artificial completamente offline que processa linguagem natural em **8 camadas** usando um **banco de conhecimento embutido** e **processamento simbólico**.

---

## 🌟 Características Principais

### ✅ 100% Offline
- **Não depende de internet**
- Todo processamento é local
- Banco de conhecimento embutido

### 🧠 8 Mentes em Camadas
1. **Caracteres** - Analisa cada letra individualmente
2. **Léxico** - Processa palavras e vocabulário
3. **Sintática** - Analisa estrutura gramatical
4. **Semântica** - Extrai significado e intenção
5. **Lógica** - Aplica raciocínio lógico
6. **Memória** - Acessa contexto da conversa
7. **Geração** - Cria respostas coerentes
8. **Validação** - Verifica e melhora respostas

### 📚 Banco de Conhecimento Embutido
- **Geografia**: Todos os 26 estados + DF do Brasil
- **Linguagem**: Alfabeto completo, vocabulário base
- **Matemática**: Números e propriedades
- **Fatos gerais**: Dias, meses, cores, direções

### 🔤 Processamento Granular
Processa texto em múltiplas camadas:
```
Texto → Caracteres → Palavras → Frases → Conceitos
```

---

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/DragonBRX/BRX-Agents.git
cd BRX-Agents

# Execute o chat
python brx_chat_v3.py
```

---

## 💬 Uso

### Chat Interativo
```bash
python brx_chat_v3.py
```

### Modo Verbose (mostra processamento das mentes)
```bash
python brx_chat_v3.py --verbose
```

### Executar Testes
```bash
python test_v3.py
```

---

## 📝 Exemplos de Uso

### Saudação Simples
```
👤 Você: Oi
🤖 BRX: Olá! Sou o BRX, pronto para ajudar.
```

### Pergunta com Restrição de Letra
```
👤 Você: Qual estado do Brasil não tem a letra A?
🤖 BRX: Encontrei 7 resultado(s): 
        Sergipe, Tocantins, Rio de Janeiro, 
        Rio Grande do Sul, Rio Grande do Norte, 
        Espírito Santo, Distrito Federal
```

### Listar Estados
```
👤 Você: Liste os estados do Brasil
🤖 BRX: Aqui está a lista com 27 item(ns): 
        Acre, Alagoas, Amapá, Amazonas, 
        Bahia, Ceará, Distrito Federal...
```

### Comandos Especiais
```
👤 Você: estados          # Lista todos os estados
👤 Você: sem letra A      # Estados sem a letra A
👤 Você: estatisticas     # Mostra estatísticas
👤 Você: ajuda            # Mostra comandos disponíveis
👤 Você: sair             # Encerra o chat
```

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        BRX-AGENT v3.0                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   ENTRADA    │───▶│ PROCESSAMENTO│───▶│   SAÍDA      │  │
│  │   (Texto)    │    │  Granular    │    │  (Resposta)  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                              │                              │
│                              ▼                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SISTEMA DE 8 MENTES                      │  │
│  ├──────────┬──────────┬──────────┬──────────┬──────────┤  │
│  │Caracteres│  Léxico  │Sintática │Semântica │  Lógica  │  │
│  │  (1)     │   (2)    │   (3)    │   (4)    │   (5)    │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
│  ┌──────────┬──────────┬──────────┐                         │
│  │  Memória │ Geração  │Validação │                         │
│  │   (6)    │   (7)    │   (8)    │                         │
│  └──────────┴──────────┴──────────┘                         │
│                              │                              │
│                              ▼                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           BANCO DE CONHECIMENTO                       │  │
│  ├──────────┬──────────┬──────────┬──────────┐          │  │
│  │Geografia │Linguagem │Matemática│  Geral   │          │  │
│  │ (Estados│(Alfabeto │(Números) │(Fatos)   │          │  │
│  │Cidades) │Palavras) │          │          │          │  │
│  └──────────┴──────────┴──────────┴──────────┘          │  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Estatísticas

### Banco de Conhecimento
- **Geografia**: 50+ entradas (estados, capitais, regiões)
- **Linguagem**: 100+ entradas (alfabeto, palavras)
- **Matemática**: 1000+ entradas (números 0-1000)
- **Geral**: 20+ entradas (fatos comuns)

### Parâmetros
- **Letras**: 52+ (a-z, A-Z, acentuadas)
- **Dígitos**: 10 (0-9)
- **Símbolos**: 30+
- **Vocabulário**: 200+ palavras

---

## 🔧 Componentes

| Arquivo | Descrição |
|---------|-----------|
| `core/brx_engine_v3.py` | Núcleo principal do sistema |
| `core/knowledge_base.py` | Banco de conhecimento embutido |
| `core/text_processor.py` | Processador granular de texto |
| `minds/eight_minds_v3.py` | Sistema de 8 mentes |
| `parameters/parameter_generator_v3.py` | Gerador de parâmetros |
| `brx_chat_v3.py` | Interface de chat |
| `test_v3.py` | Testes automatizados |

---

## 🎯 Capacidades

### ✅ O que o BRX pode fazer:
- Responder saudações
- Listar estados do Brasil
- Responder perguntas com restrições de letras
- Processar texto em múltiplas camadas
- Manter contexto da conversa
- Aprender com interações

### 🚧 Limitações:
- Conhecimento limitado ao banco embutido
- Não acessa internet para novas informações
- Processamento simbólico (não neural)

---

## 🔄 Comparação v2.0 vs v3.0

| Feature | v2.0 | v3.0 |
|---------|------|------|
| Dependência de Web | Sim (DuckDNS) | ❌ Não |
| Processamento | Simples | Granular (8 camadas) |
| Banco de Conhecimento | Mínimo | Completo |
| Sistema de Mentes | 8 mentes básicas | 8 mentes em camadas |
| Parâmetros | Básicos | Completos (letras, dígitos, símbolos) |
| Respostas | Baseadas em web | Baseadas em conhecimento embutido |
| Independência | Parcial | 100% Offline |

---

## 🛠️ Desenvolvimento

### Estrutura de Pastas
```
BRX-Agents/
├── core/                      # Núcleo do sistema
│   ├── brx_engine_v3.py      # Motor principal
│   ├── knowledge_base.py      # Banco de conhecimento
│   ├── text_processor.py      # Processador de texto
│   └── __init__.py
├── minds/                     # Sistema de mentes
│   ├── eight_minds_v3.py     # 8 mentes em camadas
│   └── __init__.py
├── parameters/                # Gerador de parâmetros
│   ├── parameter_generator_v3.py
│   └── __init__.py
├── brx_chat_v3.py            # Chat interativo
├── test_v3.py                # Testes
└── README_V3.md              # Esta documentação
```

---

## 📜 Licença

Este projeto é open source. Sinta-se livre para usar, modificar e distribuir.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Áreas para melhoria:
- Expandir banco de conhecimento
- Melhorar processamento semântico
- Adicionar mais idiomas
- Otimizar performance

---

## 🙏 Agradecimentos

Desenvolvido com foco em:
- **Independência**: Sistema 100% offline
- **Transparência**: Processamento explicável
- **Eficiência**: Código otimizado e modular
- **Escalabilidade**: Arquitetura expansível

---

**BRX-AGENT v3.0** - *Inteligência Artificial Offline e Transparente* 🧠✨
