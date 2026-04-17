# BRX-AGENT v3.0 - Core Module

from .brx_engine_v3 import BRXCoreV3, get_brx_core_v3
from .knowledge_base import BRXKnowledgeBase, KnowledgeCategory
from .text_processor import GranularTextProcessor, ProcessedText

__all__ = [
    'BRXCoreV3',
    'get_brx_core_v3',
    'BRXKnowledgeBase',
    'KnowledgeCategory',
    'GranularTextProcessor',
    'ProcessedText',
]
