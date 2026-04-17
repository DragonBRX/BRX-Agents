# BRX-AGENT v3.0 - Núcleo Principal
# Integra todas as camadas: conhecimento, processamento, mentes e parâmetros

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from core.knowledge_base import BRXKnowledgeBase
from core.text_processor import GranularTextProcessor
from minds.eight_minds_v3 import EightMindsSystemV3
from parameters.parameter_generator_v3 import BRXParameterGeneratorV3


class BRXCoreV3:
    """
    Núcleo do BRX-Agent v3.0
    Sistema completo de processamento de linguagem natural offline
    """
    
    def __init__(self, storage_path: str = "./storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              BRX-AGENT v3.0 - SISTEMA INICIADO                   ║
║                                                                  ║
║         Processamento de Linguagem Natural 100% Offline          ║
║                    8 Mentes em Camadas                           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        
        # Inicializa componentes
        print("[BRX Core] Inicializando componentes...")
        
        # 1. Banco de Conhecimento
        print("[BRX Core]  1. Carregando banco de conhecimento...")
        self.knowledge_base = BRXKnowledgeBase()
        kb_stats = self.knowledge_base.get_stats()
        print(f"[BRX Core]     ✓ {kb_stats['total_entries']} entradas")
        
        # 2. Processador de Texto
        print("[BRX Core]  2. Inicializando processador de texto...")
        self.text_processor = GranularTextProcessor()
        print("[BRX Core]     ✓ Processador granular ativo")
        
        # 3. Sistema de 8 Mentes
        print("[BRX Core]  3. Ativando sistema de 8 mentes...")
        self.minds_system = EightMindsSystemV3(self.knowledge_base)
        print("[BRX Core]     ✓ 8 mentes em camadas ativas")
        
        # 4. Gerador de Parâmetros
        print("[BRX Core]  4. Inicializando gerador de parâmetros...")
        self.param_generator = BRXParameterGeneratorV3(str(self.storage_path))
        param_stats = self.param_generator.get_stats()
        print(f"[BRX Core]     ✓ {param_stats['letters']} letras, {param_stats['vocabulary']} palavras")
        
        print("\n[BRX Core] ✓ Sistema pronto para operação!")
        print("=" * 66)
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        Processa texto através de todo o sistema
        
        Returns:
            Dict com resposta e metadados do processamento
        """
        start_time = time.time()
        
        # Processa através das 8 mentes
        result = self.minds_system.process(text)
        
        processing_time = time.time() - start_time
        
        return {
            "input": text,
            "response": result.final_answer,
            "confidence": result.confidence,
            "processing_time": processing_time,
            "thoughts": [
                {
                    "mind": t.mind_name,
                    "reasoning": t.reasoning,
                    "confidence": t.confidence
                }
                for t in result.thoughts
            ]
        }
    
    def chat(self, message: str) -> str:
        """Interface simples de chat"""
        result = self.process(message)
        return result["response"]
    
    def get_knowledge_stats(self) -> Dict:
        """Retorna estatísticas do banco de conhecimento"""
        return self.knowledge_base.get_stats()
    
    def get_parameter_stats(self) -> Dict:
        """Retorna estatísticas dos parâmetros"""
        return self.param_generator.get_stats()
    
    def query_by_letter(self, letter: str) -> List[str]:
        """Consulta itens que contêm uma letra"""
        results = self.knowledge_base.query_by_letter(letter)
        return [r.value for r in results if r.attributes.get("tipo") == "estado"]
    
    def query_without_letter(self, letter: str) -> List[str]:
        """Consulta estados que NÃO contêm uma letra"""
        return self.knowledge_base.query_states_without_letter(letter)
    
    def get_all_states(self) -> List[str]:
        """Retorna todos os estados do Brasil"""
        return self.knowledge_base.get_all_states()
    
    def demonstrate_processing(self, text: str) -> str:
        """Demonstra o processamento em todas as camadas"""
        processed = self.text_processor.process(text)
        
        output = []
        output.append("=" * 60)
        output.append("DEMONSTRAÇÃO DE PROCESSAMENTO GRANULAR")
        output.append("=" * 60)
        
        # Camada 1: Caracteres
        output.append(f"\n📌 Camada 1 - CARACTERES ({len(processed.characters)} total):")
        letters = [c.char for c in processed.characters if c.is_alpha]
        output.append(f"   Letras: {''.join(letters)}")
        output.append(f"   Únicas: {', '.join(sorted(processed.letter_frequency.keys()))}")
        
        # Camada 2: Palavras
        output.append(f"\n📌 Camada 2 - PALAVRAS ({len(processed.words)} total):")
        for word in processed.words[:5]:  # Primeiras 5
            output.append(f"   '{word.text}' ({word.word_type.value}) - letras: {''.join(word.letters)}")
        
        # Camada 3: Frases
        output.append(f"\n📌 Camada 3 - FRASES ({len(processed.phrases)} total):")
        for phrase in processed.phrases:
            output.append(f"   [{phrase.phrase_type}] {phrase.text[:50]}...")
        
        # Processamento das mentes
        output.append("\n" + "=" * 60)
        output.append("PROCESSAMENTO DAS 8 MENTES")
        output.append("=" * 60)
        
        result = self.minds_system.process(text)
        
        for thought in result.thoughts:
            output.append(f"\n🧠 {thought.mind_name} (confiança: {thought.confidence:.2f})")
            output.append(f"   {thought.reasoning[:80]}...")
        
        output.append("\n" + "=" * 60)
        output.append("RESPOSTA FINAL")
        output.append("=" * 60)
        output.append(f"\n🤖 {result.final_answer}")
        output.append(f"\n[Processado em {result.processing_time:.3f}s]")
        
        return "\n".join(output)


# Instância singleton
_brx_core_v3: Optional[BRXCoreV3] = None


def get_brx_core_v3(storage_path: str = "./storage") -> BRXCoreV3:
    """Retorna instância singleton do núcleo BRX v3.0"""
    global _brx_core_v3
    if _brx_core_v3 is None:
        _brx_core_v3 = BRXCoreV3(storage_path)
    return _brx_core_v3
