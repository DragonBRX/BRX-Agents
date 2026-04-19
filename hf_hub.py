#!/usr/bin/env python3
"""
BRX - Hugging Face Hub Integration
==================================
Módulo para carregar parâmetros e tokenizer do Hugging Face Hub automaticamente.

Uso:
    from hf_hub import get_parametros_dir, get_tokenizer_dir, download_parametros
    
    # Baixa todos os parâmetros para uma pasta local
    params_dir = download_parametros("./storage/parametros")
    
    # Ou obtém o caminho dos arquivos específicos
    config_path = get_parametros_dir() / "brx_config.json"
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any

# Constantes
REPO_ID = "DragonBRX/BRX"
PARAMETROS_PREFIX = "parametros"
TOKENIZER_PREFIX = "parametros/tokenizer"


def _get_hf_hub():
    """Lazy import do huggingface_hub"""
    try:
        from huggingface_hub import hf_hub_download, snapshot_download
        return hf_hub_download, snapshot_download
    except ImportError:
        print("[HF Hub] Aviso: huggingface_hub não instalado. Instale com: pip install huggingface_hub")
        return None, None


def download_parametros(local_dir: str = "./storage/parametros", 
                        repo_id: str = REPO_ID,
                        token: Optional[str] = None) -> Path:
    """
    Baixa todos os parâmetros do Hugging Face Hub para uma pasta local.
    
    Args:
        local_dir: Diretório local para salvar os parâmetros
        repo_id: ID do repositório no HF Hub (padrão: DragonBRX/BRX)
        token: Token de acesso ao HF Hub (opcional)
    
    Returns:
        Path do diretório com os parâmetros baixados
    """
    local_path = Path(local_dir)
    
    # Se já existe, retorna direto
    if local_path.exists() and (local_path / "brx_config.json").exists():
        print(f"[HF Hub] Parâmetros já existem em: {local_path}")
        return local_path
    
    hf_hub_download, snapshot_download = _get_hf_hub()
    if snapshot_download is None:
        print("[HF Hub] Erro: não foi possível importar huggingface_hub")
        return local_path
    
    print(f"[HF Hub] Baixando parâmetros de {repo_id}...")
    print(f"[HF Hub] Destino: {local_path}")
    
    try:
        downloaded_path = snapshot_download(
            repo_id=repo_id,
            allow_patterns=[f"{PARAMETROS_PREFIX}/**"],
            local_dir=str(local_path),
            local_dir_use_symlinks=False,
            token=token
        )
        
        # Os arquivos são baixados em local_dir/parametros/, precisamos mover para local_dir/
        parametros_subdir = local_path / "parametros"
        if parametros_subdir.exists():
            print(f"[HF Hub] Reorganizando arquivos...")
            for item in parametros_subdir.iterdir():
                dest = local_path / item.name
                if not dest.exists():
                    item.rename(dest)
            # Remove subdir vazio
            if parametros_subdir.exists():
                parametros_subdir.rmdir()
        
        print(f"[HF Hub] Parâmetros baixados com sucesso!")
        print(f"[HF Hub] Config: {local_path / 'brx_config.json'}")
        
        return local_path
        
    except Exception as e:
        print(f"[HF Hub] Erro ao baixar parâmetros: {e}")
        print(f"[HF Hub] Certifique-se de que o repositório {repo_id} existe e é público")
        return local_path


def download_tokenizer(local_dir: str = "./storage/parametros/tokenizer",
                       repo_id: str = REPO_ID,
                       token: Optional[str] = None) -> Path:
    """
    Baixa o tokenizer do Hugging Face Hub.
    
    Args:
        local_dir: Diretório local para salvar o tokenizer
        repo_id: ID do repositório no HF Hub
        token: Token de acesso ao HF Hub (opcional)
    
    Returns:
        Path do diretório com o tokenizer
    """
    local_path = Path(local_dir)
    
    if local_path.exists() and any(local_path.iterdir()):
        print(f"[HF Hub] Tokenizer já existe em: {local_path}")
        return local_path
    
    hf_hub_download, snapshot_download = _get_hf_hub()
    if snapshot_download is None:
        return local_path
    
    print(f"[HF Hub] Baixando tokenizer de {repo_id}...")
    
    try:
        snapshot_download(
            repo_id=repo_id,
            allow_patterns=[f"{TOKENIZER_PREFIX}/**"],
            local_dir=str(local_path.parent),
            local_dir_use_symlinks=False,
            token=token
        )
        
        # Reorganiza se necessário
        tokenizer_subdir = local_path.parent / "parametros" / "tokenizer"
        if tokenizer_subdir.exists() and not local_path.exists():
            tokenizer_subdir.rename(local_path)
        
        print(f"[HF Hub] Tokenizer baixado com sucesso!")
        return local_path
        
    except Exception as e:
        print(f"[HF Hub] Erro ao baixar tokenizer: {e}")
        return local_path


def get_config(local_dir: str = "./storage/parametros") -> Optional[Dict[str, Any]]:
    """
    Carrega o arquivo brx_config.json dos parâmetros.
    Baixa automaticamente se não existir localmente.
    
    Args:
        local_dir: Diretório local dos parâmetros
    
    Returns:
        Dict com a configuração ou None se houver erro
    """
    config_path = Path(local_dir) / "brx_config.json"
    
    if not config_path.exists():
        download_parametros(local_dir)
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[HF Hub] Erro ao carregar config: {e}")
        return None


def load_brx_parameters(local_dir: str = "./storage/parametros") -> Dict[str, Any]:
    """
    Carrega todos os arquivos JSON de parâmetros do BRX.
    Baixa automaticamente do HF Hub se necessário.
    
    Args:
        local_dir: Diretório local dos parâmetros
    
    Returns:
        Dict com todos os parâmetros carregados
    """
    params_dir = download_parametros(local_dir)
    
    parameters = {
        "config": None,
        "letras": None,
        "palavras": None,
        "frases": None,
        "indice_tensores": None,
    }
    
    # Carrega cada arquivo
    files_map = {
        "config": "brx_config.json",
        "letras": "brx_letras.json",
        "palavras": "brx_palavras.json",
        "frases": "brx_frases.json",
        "indice_tensores": "brx_indice_tensores.json",
    }
    
    for key, filename in files_map.items():
        filepath = params_dir / filename
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    parameters[key] = json.load(f)
                print(f"[HF Hub] Carregado: {filename}")
            except Exception as e:
                print(f"[HF Hub] Erro ao carregar {filename}: {e}")
        else:
            print(f"[HF Hub] Aviso: {filename} não encontrado")
    
    return parameters


def is_parametros_available(local_dir: str = "./storage/parametros") -> bool:
    """
    Verifica se os parâmetros já estão disponíveis localmente.
    
    Args:
        local_dir: Diretório local dos parâmetros
    
    Returns:
        True se os parâmetros principais existem
    """
    path = Path(local_dir)
    required = ["brx_config.json", "brx_palavras.json", "brx_letras.json"]
    return all((path / f).exists() for f in required)


# ============================
# FUNÇÕES DE COMPATIBILIDADE
# ============================

def setup_parametros_from_hub(storage_path: str = "./storage", 
                               token: Optional[str] = None) -> Path:
    """
    Configura os parâmetros do BRX baixando do Hugging Face Hub.
    Função principal de setup - deve ser chamada na inicialização.
    
    Args:
        storage_path: Diretório base de storage do BRX
        token: Token de acesso ao HF Hub (opcional)
    
    Returns:
        Path do diretório com os parâmetros
    """
    params_dir = Path(storage_path) / "parametros"
    params_dir.mkdir(parents=True, exist_ok=True)
    
    print("[HF Hub] Verificando parâmetros do BRX...")
    
    if is_parametros_available(params_dir):
        print(f"[HF Hub] Parâmetros já disponíveis em: {params_dir}")
        return params_dir
    
    print("[HF Hub] Parâmetros não encontrados localmente.")
    print("[HF Hub] Iniciando download do Hugging Face Hub...")
    
    return download_parametros(params_dir, token=token)


if __name__ == "__main__":
    # Teste do módulo
    print("=" * 50)
    print("BRX - Hugging Face Hub Integration")
    print("=" * 50)
    
    # Testa download
    params = download_parametros("./test_parametros")
    print(f"\nParâmetros em: {params}")
    
    if params.exists():
        files = list(params.glob("*.json"))
        print(f"Arquivos JSON: {[f.name for f in files]}")
