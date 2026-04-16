# Guia de Instalacao Detalhado - BRX-Agent v2.0

Este guia explica como configurar o BRX-Agent no Ubuntu 22.04, 24.04 ou superior, resolvendo o bloqueio de instalacao de pacotes do sistema.

## Metodo Recomendado (Automatico)

Use o script mestre que cuida de toda a configuracao do ambiente isolado:

```bash
curl -sO https://raw.githubusercontent.com/DragonBRX/BRX-Agents/main/brx_run.sh && chmod +x brx_run.sh && ./brx_run.sh
```

---

## Metodo Manual (Passo a Passo)

Se voce preferir configurar manualmente, siga estes passos rigorosamente para evitar o erro `externally-managed-environment`.

### 1. Preparar o Sistema
```bash
sudo apt update && sudo apt install -y python3-pip python3-venv git curl
```

### 2. Clonar e Entrar na Pasta
```bash
git clone https://github.com/DragonBRX/BRX-Agents.git
cd BRX-Agents
```

### 3. Criar o Ambiente Virtual (VENV)
O Ubuntu moderno nao permite instalar pacotes Python fora de um ambiente isolado.
```bash
python3 -m venv venv
```

### 4. Ativar o Ambiente (CRUCIAL)
Voce deve rodar este comando **toda vez** que abrir um novo terminal para trabalhar no projeto:
```bash
source venv/bin/activate
```
*Apos rodar, voce vera `(venv)` no inicio do seu prompt do terminal.*

### 5. Instalar Dependencias
Agora que o ambiente esta ativo, o `pip` funcionara sem erros:
```bash
pip install --upgrade pip
pip install psutil requests
[ -f requirements.txt ] && pip install -r requirements.txt
```

---

## Como Executar

Sempre garanta que o ambiente esta ativo antes de rodar:

### Modo 1: Geracao Autonoma (Treinamento)
```bash
source venv/bin/activate
python3 brx_autonomous.py --interval 30 --verbose
```

### Modo 2: Chat Interativo
```bash
source venv/bin/activate
python3 brx_chat.py
```

---

## Solucao de Problemas

### Erro: `externally-managed-environment`
**Causa:** Voce tentou usar o `pip` sem ativar o `venv`.
**Solução:** Rode `source venv/bin/activate` e tente novamente.

### Erro: `Opcao invalida` no script
**Causa:** Rodar o script via `curl ... | bash` pode impedir a leitura do teclado.
**Solucao:** Baixe o script primeiro: `curl -sO ... && ./brx_run.sh`.

---

## Mapa da Arquitetura

![Arquitetura do BRX](architecture.png)
