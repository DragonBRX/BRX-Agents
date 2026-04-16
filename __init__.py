# BRX-AGENT v2.0
# Agente Auto-Evolutivo Multi-Cérebro
# 
# Componentes principais:
# - core: Núcleo do sistema e tipos fundamentais
# - consciousness: Sistema de consciência e auto-identidade
# - minds: Sistema de 8 mentes com debate circular
# - parameters: Gerador automático de parâmetros
# - search: Módulo de pesquisa Duck DNS
#
# Arquivos de execução:
# - brx_autonomous.py: Modo autônomo contínuo (deixe rodando)
# - brx_chat.py: Interface de chat interativa

__version__ = "2.0.0"
__author__ = "BRX-AGENT"
__description__ = "Agente Auto-Evolutivo Multi-Cérebro"

from core.brx_engine import BRXCore, get_brx_core
from consciousness.self_awareness import BRXConsciousnessEngine, get_consciousness_engine
from minds.eight_minds import EightMindsSystem, Mind
from parameters.auto_generator import BRXParameterGenerator
from search.duckdns_search import DuckDNSSearcher, get_searcher

__all__ = [
    "BRXCore",
    "get_brx_core",
    "BRXConsciousnessEngine",
    "get_consciousness_engine",
    "EightMindsSystem",
    "Mind",
    "BRXParameterGenerator",
    "DuckDNSSearcher",
    "get_searcher",
]
