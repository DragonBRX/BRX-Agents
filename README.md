# BRX-AGENT v2.0

![Arquitetura BRX](architecture.png)

## Agente Auto-Evolutivo Multi-Cérebro

O BRX é um agente de inteligência artificial com arquitetura única de **8 mentes independentes** que funcionam como uma equipe de especialistas. Cada mente tem seu próprio raciocínio, mas se comunicam em uma **roda de conversas** para alcançar consenso.

---

## 🚀 Comando Único de Instalação e Execução

Copie e cole o comando abaixo no seu terminal Ubuntu para instalar, atualizar e rodar o BRX-Agent. Ele configura o ambiente isolado, resolve erros de permissão e detecta automaticamente o seu HD externo:

```bash
curl -sO https://raw.githubusercontent.com/DragonBRX/BRX-Agents/main/brx_run.sh && chmod +x brx_run.sh && ./brx_run.sh
```

---

## Armazenamento em HD Externo

O BRX-Agent está configurado para priorizar o armazenamento no seu HD externo:
**Caminho:** `/media/dragonscp/Novo volume/modelo BRX`

Se o HD estiver montado, o sistema salvará automaticamente:
- Todo o vocabulário desenvolvido.
- O estado de evolução (parâmetros e mentes).
- Memórias e logs de treinamento.

Se o HD não estiver conectado, o sistema usará a pasta local `storage/` como backup.

---

## Como verificar se está salvando no HD?
Ao iniciar o modelo com o comando acima, você verá a mensagem:
`[INFO] Usando HD externo para armazenamento: /media/dragonscp/Novo volume/modelo BRX`

Você também pode conferir se os arquivos estão sendo criados rodando:
```bash
ls -la "/media/dragonscp/Novo volume/modelo BRX/hd"
```

---

## Solução para o Erro: externally-managed-environment

O comando único acima já resolve este erro automaticamente. Caso você queira rodar comandos manuais (como `pip install`), **você DEVE usar o ambiente virtual** criado pelo script:

```bash
# Entre na pasta do projeto
cd BRX-Agents

# Instale usando o módulo do Python (O Segredo)
./venv/bin/python3 -m pip install -r requirements.txt

# Rode o Modelo manualmente se desejar
./venv/bin/python3 brx_autonomous.py  # Geração/Treinamento
./venv/bin/python3 brx_chat.py        # Chat Interativo
```

---

## Características Principais

### Arquitetura de 8 Mentes
- **Designer**: Estrutura e padrões de dados
- **Analista**: Lógica e consistência técnica
- **Inovador**: Abordagens criativas e novas perspectivas
- **Crítico**: Identificação de falhas e riscos (Red Teaming)
- **Revisor**: Qualidade textual e clareza
- **Validador**: Coerência temática e precisão
- **Estrategista**: Planejamento e utilidade prática
- **Memória**: Contexto histórico e persistência

---

**"A inteligência não é apenas processar informações, mas evoluir a forma como processamos."** - BRX
