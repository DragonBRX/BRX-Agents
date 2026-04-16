# Guia de Instalação e Execução - BRX-Agent v2.0

Este guia foi testado e validado em ambiente Ubuntu 22.04 LTS. Siga os blocos de comandos abaixo para configurar o BRX-Agent de forma isolada e segura.

## 1. Instalação do Zero (Ambiente Zerado)

Copie e cole este bloco no seu terminal para instalar todas as dependências necessárias e configurar o ambiente virtual:

```bash
# 1. Atualizar sistema e instalar dependências base
sudo apt update && sudo apt install -y python3-pip python3-venv git curl

# 2. Clonar o repositório
git clone https://github.com/DragonBRX/BRX-Agents.git
cd BRX-Agents

# 3. Criar e ativar ambiente virtual (Isolamento Total)
python3 -m venv venv
source venv/bin/activate

# 4. Instalar dependências do Python (Validadas)
pip install --upgrade pip
pip install psutil requests
# Caso o arquivo requirements.txt exista, instale também:
[ -f requirements.txt ] && pip install -r requirements.txt
```

---

## 2. Modo de Execução 1: Geração Autônoma (Treinamento)

Este modo faz o BRX gerar parâmetros, pesquisar na web e evoluir sozinho. Ideal para deixar rodando em background.

```bash
# Ative o ambiente (se já não estiver ativo)
source venv/bin/activate

# Iniciar o modo autônomo (intervalo de 30 segundos entre ciclos)
python3 brx_autonomous.py --interval 30 --verbose
```

---

## 3. Modo de Execução 2: Chat Interativo

Use este modo para conversar com o BRX e usar o conhecimento que ele já adquiriu no modo de geração.

```bash
# Ative o ambiente (se já não estiver ativo)
source venv/bin/activate

# Iniciar o chat interativo
python3 brx_chat.py
```

No chat, você pode usar comandos como:
- `/status` : Ver o nível de evolução e hardware detectado.
- `/search <termo>` : Forçar uma pesquisa web.
- `/evolve` : Forçar um ciclo de evolução imediato.
- `/quit` : Sair do chat.

---

## 4. Visualização (Dashboard)

Para rodar o Dashboard visual (requer Node.js):

```bash
cd dashboard
npm install
npm run dev
```

---

## 🔍 Estrutura do Modelo (Mapa)

![Arquitetura do BRX](architecture.png)

O BRX detecta automaticamente seu hardware (CPU, Memória, GPU) e adapta o número de mentes ativas para otimizar a performance no seu dispositivo.
