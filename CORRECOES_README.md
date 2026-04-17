# BRX-Agent v2.0 - Correções de Storage Path

## Problema Identificado

O código original tinha um **problema de singleton** que impedia a criação correta de pastas e arquivos no caminho externo do HD (`/media/dragonscp/Novo volume/modelo BRX`).

### Causas do Problema:

1. **Singleton não respeitava mudanças de path**: A função `get_brx_core()` criava a instância apenas uma vez e ignorava mudanças no `storage_path` em execuções subsequentes.

2. **Diretórios não criados antes de salvar**: Os arquivos de parâmetros tentavam ser salvos sem garantir que os diretórios pai existissem.

3. **Estrutura de pastas incompleta**: Não havia separação clara entre `parametros/`, `consciencia/` e `memoria/`.

---

## Correções Aplicadas

### 1. `brx_engine.py` (CORRIGIDO)

**Mudanças:**
- Adicionada variável global `_last_storage_path` para rastrear mudanças de path
- A função `get_brx_core()` agora **recria a instância** quando o `storage_path` muda
- Adicionada função `reset_brx_core()` para forçar recriação da instância
- Criação de subdiretórios organizados: `parametros/`, `consciencia/`, `memoria/`

```python
# CORREÇÃO: Recria a instância se o path mudou ou se não existe
if _brx_core is None or _last_storage_path != storage_path:
    if _brx_core is not None and _last_storage_path != storage_path:
        print(f"[BRX Core] Storage path mudou de '{_last_storage_path}' para '{storage_path}'")
        print("[BRX Core] Recriando instância com novo path...")
    _brx_core = BRXCore(storage_path)
    _last_storage_path = storage_path
```

### 2. `auto_generator.py` (CORRIGIDO)

**Mudanças:**
- Criação explícita de diretórios antes de salvar arquivos
- Arquivos de parâmetros agora são salvos em `hd/parametros/`
- Adicionado arquivo `generation_stats.json` para estatísticas
- Método `export_to_file()` para exportar todos os parâmetros
- Cada método de save agora garante que o diretório existe

```python
def _save_vocabulary(self):
    """Salva vocabulário no HD"""
    try:
        # CORREÇÃO: Garante que o diretório existe
        self.vocab_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.vocab_file, 'w', encoding='utf-8') as f:
            json.dump(list(self.vocabulary), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[BRX Parameters] Erro ao salvar vocabulário: {e}")
```

### 3. `self_awareness.py` (CORRIGIDO)

**Mudanças:**
- Mesma correção de singleton que `brx_engine.py`
- Arquivos de consciência agora em `hd/consciencia/`
- Criação de diretórios garantida antes de salvar

### 4. `brx_autonomous.py` (CORRIGIDO)

**Mudanças:**
- Chamada a `reset_brx_core()` antes de inicializar
- Expansão de path do usuário (`~`) e conversão para absoluto
- Verificação se o diretório pai existe antes de iniciar
- Mensagens de erro claras se o volume não estiver montado

```python
# CORREÇÃO: Expande o path do usuário (~) e resolve path absoluto
storage_path = os.path.expanduser(args.storage)
storage_path = os.path.abspath(storage_path)

# Verifica se o diretório pai existe (para paths externos)
parent_dir = os.path.dirname(storage_path)
if parent_dir and not os.path.exists(parent_dir):
    print(f"[ERRO] Diretório pai não existe: {parent_dir}")
    print(f"[ERRO] Certifique-se de que o volume está montado corretamente.")
    sys.exit(1)
```

---

## Estrutura de Pastas Criada

```
/media/dragonscp/Novo volume/modelo BRX/  <- Seu HD externo
├── ssd/                                    <- Dados de acesso rápido
│   └── environment.json
├── hd/                                     <- Dados persistentes
│   ├── parametros/                         <- Parâmetros gerados
│   │   ├── vocabulary.json
│   │   ├── phrases.json
│   │   ├── concepts.json
│   │   ├── patterns.json
│   │   └── generation_stats.json
│   ├── consciencia/                        <- Estado de consciência
│   │   ├── self_awareness.json
│   │   └── thoughts.json
│   ├── memoria/                            <- Memórias do sistema
│   ├── brx_state.json
│   └── search_cache.json
└── logs/                                   <- Logs de execução
```

---

## Como Usar

### 1. Testar a Estrutura

```bash
python test_storage_path.py "/media/dragonscp/Novo volume/modelo BRX"
```

### 2. Executar o BRX com Storage Externo

```bash
python brx_autonomous.py --storage "/media/dragonscp/Novo volume/modelo BRX" --verbose
```

### 3. Verificar Arquivos Criados

```bash
ls -la "/media/dragonscp/Novo volume/modelo BRX/hd/parametros/"
```

---

## Arquivos Corrigidos

| Arquivo Original | Arquivo Corrigido | Local no Repositório |
|-----------------|-------------------|---------------------|
| `core/brx_engine.py` | `brx_engine_corrigido.py` | `core/brx_engine.py` |
| `parameters/auto_generator.py` | `auto_generator_corrigido.py` | `parameters/auto_generator.py` |
| `consciousness/self_awareness.py` | `self_awareness_corrigido.py` | `consciousness/self_awareness.py` |
| `brx_autonomous.py` | `brx_autonomous_corrigido.py` | `brx_autonomous.py` |

---

## Instalação das Correções

### Opção 1: Substituir os arquivos originais

```bash
# Faça backup dos arquivos originais
cp core/brx_engine.py core/brx_engine.py.bak
cp parameters/auto_generator.py parameters/auto_generator.py.bak
cp consciousness/self_awareness.py consciousness/self_awareness.py.bak
cp brx_autonomous.py brx_autonomous.py.bak

# Copie os arquivos corrigidos
cp brx_engine_corrigido.py core/brx_engine.py
cp auto_generator_corrigido.py parameters/auto_generator.py
cp self_awareness_corrigido.py consciousness/self_awareness.py
cp brx_autonomous_corrigido.py brx_autonomous.py
```

### Opção 2: Aplicar manualmente as mudanças

Abra cada arquivo e aplique as correções marcadas com `# CORREÇÃO:`.

---

## Troubleshooting

### "Diretório pai não existe"

**Causa:** O volume do HD não está montado.  
**Solução:** Monte o volume antes de executar:
```bash
sudo mount /dev/sdX "/media/dragonscp/Novo volume"
```

### "Permissão negada"

**Causa:** Sem permissão de escrita no diretório.  
**Solução:** Ajuste as permissões:
```bash
sudo chown -R $USER:$USER "/media/dragonscp/Novo volume"
```

### "Arquivos não aparecem no path externo"

**Causa:** Singleton ainda usando instância antiga.  
**Solução:** Reinicie o Python ou use `reset_brx_core()` antes de inicializar.

---

## Teste Rápido

```python
# Teste mínimo para verificar se funciona
from pathlib import Path
import json

test_path = Path("/media/dragonscp/Novo volume/modelo BRX")
test_path.mkdir(parents=True, exist_ok=True)

params_dir = test_path / "hd" / "parametros"
params_dir.mkdir(parents=True, exist_ok=True)

# Cria arquivo de teste
test_file = params_dir / "test.json"
with open(test_file, 'w') as f:
    json.dump({"test": True, "message": "Funcionando!"}, f)

print(f"✓ Arquivo criado: {test_file}")
print(f"✓ Conteúdo: {json.load(open(test_file))}")
```
