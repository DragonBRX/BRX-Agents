"""
BRX-AGENT v3.0
==============
Sistema de Processamento de Linguagem Natural 100% Offline

Processamento em 8 camadas:
1. Caracteres    2. Léxico      3. Sintática   4. Semântica
5. Lógica        6. Memória     7. Geração     8. Validação

Uso:
    from core import BRXCoreV3
    
    brx = BRXCoreV3()
    response = brx.chat("Qual estado não tem a letra A?")
    print(response)
"""

__version__ = "3.0.0"
__author__ = "DragonBRX"

from core import BRXCoreV3, get_brx_core_v3
from core.knowledge_base import BRXKnowledgeBase
from core.text_processor import GranularTextProcessor

__all__ = [
    'BRXCoreV3',
    'get_brx_core_v3',
    'BRXKnowledgeBase',
    'GranularTextProcessor',
]
