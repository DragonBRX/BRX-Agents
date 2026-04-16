#!/bin/bash

# Script de Inicialização Única do BRX-Agent v2.0 (Versão Blindada)
# Este script automatiza: Atualização, Instalação em VENV e Execução Interativa.

set -e

REPO_URL="https://github.com/DragonBRX/BRX-Agents.git"
REPO_DIR="BRX-Agents"
# Caminho padrao para o HD externo do usuario
EXTERNAL_STORAGE="/media/dragonscp/Novo volume/modelo BRX"
MOUNT_POINT="/media/dragonscp/Novo volume"

# Tenta criar a pasta no HD externo se o disco estiver montado
if [ -d "$MOUNT_POINT" ]; then
    echo "[INFO] Detectado ponto de montagem: $MOUNT_POINT"
    # Tenta criar a pasta e verifica se temos permissao de escrita
    if mkdir -p "$EXTERNAL_STORAGE" 2>/dev/null && [ -w "$EXTERNAL_STORAGE" ]; then
        echo "[INFO] Pasta de armazenamento preparada no HD externo."
    else
        echo "[AVISO] Nao foi possivel criar ou escrever na pasta do HD externo. Verifique as permissoes."
    fi
fi

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

# 2. Configuração do Ambiente Virtual (Obrigatório no Ubuntu Moderno)
echo "[2/4] Configurando ambiente isolado (venv)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Definir caminhos para o executável do venv de forma absoluta
PIP_EXEC="./venv/bin/pip"
PYTHON_EXEC="./venv/bin/python3"

# 3. Instalação de Dependências (Usando o PIP do venv diretamente)
echo "[3/4] Instalando/Atualizando dependências dentro do venv..."
$PIP_EXEC install --upgrade pip > /dev/null 2>&1
$PIP_EXEC install psutil requests > /dev/null 2>&1

if [ -f "requirements.txt" ]; then
    $PIP_EXEC install -r requirements.txt > /dev/null 2>&1
fi

# 4. Execução do Modelo
echo "[4/4] Preparando execução..."
echo "----------------------------------------------------------------"
echo "Selecione o modo de execução:"
echo "1) Modo Autônomo (Geração de Parâmetros e Evolução)"
echo "2) Modo Chat (Conversação Direta)"
echo "----------------------------------------------------------------"

# Tenta ler do terminal (/dev/tty) ou da entrada padrão (stdin) se o terminal não estiver disponível
if [ -t 0 ]; then
    read -p "Opção (1 ou 2): " choice
else
    # Se estiver vindo via pipe (curl | bash), tenta ler do terminal diretamente
    read -p "Opção (1 ou 2): " choice < /dev/tty || read -p "Opção (1 ou 2): " choice
fi

case $choice in
    1)
        echo "Iniciando Modo Autônomo..."
        # Verifica se o HD externo esta montado, caso contrario usa o padrao local
        if [ -d "$EXTERNAL_STORAGE" ]; then
            echo "[INFO] Usando HD externo para armazenamento: $EXTERNAL_STORAGE"
            $PYTHON_EXEC brx_autonomous.py --interval 30 --verbose --storage "$EXTERNAL_STORAGE"
        else
            echo "[AVISO] HD externo nao encontrado. Usando armazenamento local."
            $PYTHON_EXEC brx_autonomous.py --interval 30 --verbose
        fi
        ;;
    2)
        echo "Iniciando Modo Chat..."
        if [ -d "$EXTERNAL_STORAGE" ]; then
            echo "[INFO] Usando HD externo para carregar dados: $EXTERNAL_STORAGE"
            $PYTHON_EXEC brx_chat.py --storage "$EXTERNAL_STORAGE"
        else
            echo "[AVISO] HD externo nao encontrado. Usando armazenamento local."
            $PYTHON_EXEC brx_chat.py
        fi
        ;;
    *)
        echo "Opção inválida ($choice). Encerrando."
        exit 1
        ;;
esac
