#!/bin/bash

# Script de Inicialização Única do BRX-Agent v2.0
# Este script automatiza: Atualização, Instalação, Ambiente Virtual e Execução.

set -e

REPO_URL="https://github.com/DragonBRX/BRX-Agents.git"
REPO_DIR="BRX-Agents"

echo "----------------------------------------------------------------"
echo "        INICIALIZADOR AUTOMÁTICO BRX-AGENT v2.0"
echo "----------------------------------------------------------------"

# 1. Sincronização do Repositório
if [ -d ".git" ] && [ "$(basename $(git rev-parse --show-toplevel))" == "BRX-Agents" ]; then
    echo "[1/4] Já estamos dentro de BRX-Agents. Atualizando..."
    git fetch origin
    git reset --hard origin/main
elif [ -d "$REPO_DIR" ]; then
    echo "[1/4] Atualizando repositório existente na pasta $REPO_DIR..."
    cd "$REPO_DIR"
    git fetch origin
    git reset --hard origin/main
else
    echo "[1/4] Clonando repositório pela primeira vez..."
    git clone "$REPO_URL"
    cd "$REPO_DIR"
fi

# 2. Configuração do Ambiente Virtual
echo "[2/4] Configurando ambiente isolado (venv)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 3. Instalar Dependências
echo "[3/4] Instalando/Atualizando dependências..."
pip install --upgrade pip > /dev/null
pip install psutil requests > /dev/null
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null
fi

# 4. Execução do Modelo
echo "[4/4] Iniciando BRX-Agent..."
echo "----------------------------------------------------------------"
echo "Selecione o modo de execução:"
echo "1) Modo Autônomo (Geração de Parâmetros e Evolução)"
echo "2) Modo Chat (Conversação Direta)"
echo "----------------------------------------------------------------"
read -p "Opção (1 ou 2): " choice

case $choice in
    1)
        echo "Iniciando Modo Autônomo..."
        python3 brx_autonomous.py --interval 30 --verbose
        ;;
    2)
        echo "Iniciando Modo Chat..."
        python3 brx_chat.py
        ;;
    *)
        echo "Opção inválida. Encerrando."
        exit 1
        ;;
esac
