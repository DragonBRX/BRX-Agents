#!/usr/bin/env python3
"""
Script de teste para verificar se o BRX está criando pastas e parâmetros
no caminho correto do HD externo.

Uso:
    python test_storage_path.py "/media/dragonscp/Novo volume/modelo BRX"
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def test_storage_structure(storage_path: str):
    """Testa a criação da estrutura de pastas"""
    print("=" * 60)
    print("TESTE: Estrutura de Storage BRX")
    print("=" * 60)
    print(f"\nStorage path: {storage_path}")
    print(f"Path absoluto: {os.path.abspath(storage_path)}")
    
    path = Path(storage_path)
    
    # Testa criação do diretório principal
    print("\n[1] Criando diretório principal...")
    try:
        path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ Diretório criado: {path}")
        print(f"   ✓ Existe: {path.exists()}")
        print(f"   ✓ É diretório: {path.is_dir()}")
    except Exception as e:
        print(f"   ✗ ERRO: {e}")
        return False
    
    # Cria subdiretórios
    subdirs = ["ssd", "hd", "logs", "hd/parametros", "hd/consciencia", "hd/memoria"]
    
    print("\n[2] Criando subdiretórios...")
    for subdir in subdirs:
        try:
            (path / subdir).mkdir(parents=True, exist_ok=True)
            print(f"   ✓ {subdir}/")
        except Exception as e:
            print(f"   ✗ {subdir}/ - ERRO: {e}")
    
    # Testa criação de arquivo de parâmetros
    print("\n[3] Criando arquivo de teste de parâmetros...")
    params_dir = path / "hd" / "parametros"
    test_file = params_dir / "test_params.json"
    
    test_data = {
        "test": True,
        "timestamp": datetime.now().isoformat(),
        "message": "Arquivo de teste BRX - Estrutura funcionando!",
        "storage_path": str(path),
        "parameters": {
            "letras": ["a", "b", "c"],
            "numeros": [1, 2, 3],
            "conceitos": ["teste", "estrutura", "funcionamento"]
        }
    }
    
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        print(f"   ✓ Arquivo criado: {test_file}")
        
        # Lê de volta para confirmar
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        print(f"   ✓ Arquivo lido com sucesso")
        print(f"   ✓ Conteúdo: {loaded['message']}")
    except Exception as e:
        print(f"   ✗ ERRO: {e}")
        return False
    
    # Lista todos os arquivos criados
    print("\n[4] Estrutura final criada:")
    print_directory_tree(path)
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DO TESTE")
    print("=" * 60)
    print(f"✓ Diretório principal: {path}")
    print(f"✓ Subdiretórios criados: {len(subdirs)}")
    print(f"✓ Arquivo de teste: {test_file}")
    print(f"\n✓ TESTE CONCLUÍDO COM SUCESSO!")
    print(f"\nAgora você pode executar o BRX com:")
    print(f'  python brx_autonomous.py --storage "{storage_path}"')
    
    return True


def print_directory_tree(path: Path, prefix: str = ""):
    """Imprime a árvore de diretórios"""
    if not path.exists():
        return
    
    items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "
        
        if item.is_dir():
            print(f"{prefix}{connector}{item.name}/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_directory_tree(item, new_prefix)
        else:
            size = item.stat().st_size
            print(f"{prefix}{connector}{item.name} ({size} bytes)")


def main():
    """Função principal"""
    # Pega o path da linha de comando ou usa o padrão
    if len(sys.argv) > 1:
        storage_path = sys.argv[1]
    else:
        # Tenta detectar o HD externo automaticamente
        possible_paths = [
            "/media/dragonscp/Novo volume/modelo BRX",
            "/media/dragonscp/Novo volume/BRX",
            "/mnt/dragonscp/modelo BRX",
            "./storage"
        ]
        
        print("Procurando path de storage...")
        for path in possible_paths:
            expanded = os.path.expanduser(path)
            parent = os.path.dirname(expanded)
            
            if os.path.exists(parent):
                print(f"  Encontrado: {path}")
                storage_path = path
                break
        else:
            storage_path = "./storage"
            print(f"  Usando padrão: {storage_path}")
    
    # Expande ~ e converte para absoluto
    storage_path = os.path.expanduser(storage_path)
    storage_path = os.path.abspath(storage_path)
    
    # Executa o teste
    success = test_storage_structure(storage_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
