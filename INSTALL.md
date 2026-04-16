# Guia de Instalação Rápida - BRX-Agent v2.0

Este guia explica como configurar e rodar o BRX-Agent em um único comando, resolvendo o bloqueio de instalação de pacotes do sistema e integrando seu HD externo.

## 🚀 Método Único (Recomendado)

Use o comando mestre abaixo. Ele baixa o script, configura o ambiente virtual e abre o menu para você escolher entre **Treinamento (Geração)** ou **Chat Interativo**:

```bash
curl -sO https://raw.githubusercontent.com/DragonBRX/BRX-Agents/main/brx_run.sh && chmod +x brx_run.sh && ./brx_run.sh
```

---

## 🛠️ O que este comando faz:
1. **Sincroniza o Repositório**: Se você já tem a pasta `BRX-Agents`, ele atualiza. Se não tem, ele clona.
2. **Configura o Ambiente**: Cria um ambiente isolado (`venv`) para evitar o erro `externally-managed-environment`.
3. **Instala Dependências**: Instala tudo o que é necessário (incluindo as correções de hardware).
4. **Detecta HD Externo**: Tenta localizar automaticamente seu HD em `/media/dragonscp/Novo volume/modelo BRX`.
5. **Menu Interativo**: Permite que você escolha o modo de execução na hora.

---

## 🏗️ Execução Manual (Se preferir)

Se você quiser rodar os comandos separadamente, use sempre o Python do ambiente virtual:

### Geração de Parâmetros (Treinamento)
```bash
cd BRX-Agents
./venv/bin/python3 brx_autonomous.py --interval 30 --verbose --storage "/media/dragonscp/Novo volume/modelo BRX"
```

### Chat Interativo
```bash
cd BRX-Agents
./venv/bin/python3 brx_chat.py --storage "/media/dragonscp/Novo volume/modelo BRX"
```

---

## ❌ Solução de Problemas

### Erro: `externally-managed-environment`
**Causa:** Você tentou usar o `pip` do sistema.
**Solução:** Use o comando mestre acima ou `./venv/bin/python3 -m pip install`.

### Erro: `Opção inválida` no script
**Causa:** O script não conseguiu ler seu teclado.
**Solução:** Rode o comando `./brx_run.sh` diretamente no seu terminal após baixá-lo.

---

## 🔍 Mapa da Arquitetura

![Arquitetura do BRX](architecture.png)
