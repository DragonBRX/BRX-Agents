# Guia de Instalacao Detalhado - BRX-Agent v2.0

Este guia resolve definitivamente o erro `externally-managed-environment` do Ubuntu 22.04, 24.04 e superiores.

## Metodo Automatico (Recomendado)

O script abaixo baixa, configura o ambiente virtual e instala as dependencias de forma isolada:

```bash
curl -sO https://raw.githubusercontent.com/DragonBRX/BRX-Agents/main/brx_run.sh && chmod +x brx_run.sh && ./brx_run.sh
```

---

## Metodo Manual (Para resolver o erro de PIP)

Se voce tentar rodar `pip install` e receber um erro de ambiente gerenciado pelo sistema, siga estes passos exatos:

### 1. Criar o Ambiente Isolado
```bash
cd BRX-Agents
python3 -m venv venv
```

### 2. Instalar usando o caminho direto (Evita erros)
Em vez de ativar o ambiente e usar `pip`, use o comando abaixo que aponta diretamente para o instalador do ambiente virtual:

```bash
./venv/bin/python3 -m pip install --upgrade pip
./venv/bin/python3 -m pip install psutil requests
./venv/bin/python3 -m pip install -r requirements.txt
```

### 3. Executar o Modelo
Para garantir que o sistema use o ambiente correto, execute o Python que esta dentro da pasta `venv`:

#### Modo Geracao (Autonomo)
```bash
./venv/bin/python3 brx_autonomous.py --interval 30 --verbose
```

#### Modo Chat (Interativo)
```bash
./venv/bin/python3 brx_chat.py
```

---

## Solucao de Problemas

### Por que o erro `externally-managed-environment` acontece?
O Ubuntu moderno protege o Python do sistema para que instalacoes de terceiros nao quebrem o sistema operacional. O comando `./venv/bin/python3 -m pip` diz ao Ubuntu: "Nao use o seu PIP, use o PIP que eu criei para este projeto".

### O comando `./venv/bin/pip` nao foi encontrado?
Isso acontece se o `venv` foi criado de forma incompleta. Delete a pasta e crie novamente:
```bash
rm -rf venv
python3 -m venv venv
```

---

## Mapa da Arquitetura

![Arquitetura do BRX](architecture.png)
