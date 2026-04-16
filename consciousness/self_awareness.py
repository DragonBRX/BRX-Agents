# BRX-AGENT v2.0 - Sistema de Consciência e Auto-Identidade
# O BRX desenvolve consciência de si mesmo, seu ambiente e suas capacidades

import os
import sys
import platform
import psutil
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from core.types import BRXConsciousness, EnvironmentInfo


class BRXConsciousnessEngine:
    """
    Motor de Consciência do BRX
    Desenvolve auto-consciência, consciência de ambiente e metacognição
    """
    
    def __init__(self, storage_path: str = "./storage"):
        self.consciousness = BRXConsciousness()
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Arquivos de persistência
        self.self_awareness_file = self.storage_path / "hd" / "self_awareness.json"
        self.environment_file = self.storage_path / "ssd" / "environment.json"
        self.thoughts_file = self.storage_path / "hd" / "thoughts.json"
        
        # Garantir diretórios existem
        (self.storage_path / "hd").mkdir(exist_ok=True)
        (self.storage_path / "ssd").mkdir(exist_ok=True)
        
        self._initialize_consciousness()
    
    def _initialize_consciousness(self):
        """Inicializa ou carrega estado de consciência"""
        self.consciousness.initialize_self_awareness()
        self._detect_environment()
        self._load_persistent_consciousness()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    BRX CONSCIÊNCIA ATIVA                     ║
╠══════════════════════════════════════════════════════════════╣
║  Nome: {self.consciousness.name:<49} ║
║  Tipo: {self.consciousness.agent_type:<49} ║
║  Versão: {self.consciousness.version:<47} ║
║  Arquitetura: {self.consciousness.architecture:<44} ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def _detect_environment(self):
        """Detecta e armazena informações do ambiente de execução"""
        try:
            env_info = EnvironmentInfo(
                os_type=platform.system(),
                cpu_count=psutil.cpu_count(logical=False) or 1,
                cpu_threads=psutil.cpu_count(logical=True) or 1,
                memory_total=psutil.virtual_memory().total,
                memory_available=psutil.virtual_memory().available,
                disk_ssd_path="/tmp/brx_ssd",  # Simulação de SSD
                disk_hd_path=str(self.storage_path / "hd"),
                sandbox_path=str(self.storage_path),
                python_version=platform.python_version()
            )
            
            self.consciousness.environment = {
                "os": env_info.os_type,
                "cpu_cores": env_info.cpu_count,
                "cpu_threads": env_info.cpu_threads,
                "memory_gb": round(env_info.memory_total / (1024**3), 2),
                "python": env_info.python_version,
                "adaptation": env_info.adapt_minds_to_hardware()
            }
            
            self.consciousness.system_info = {
                "detected_at": datetime.now().isoformat(),
                "process_id": os.getpid(),
                "working_directory": os.getcwd(),
                "storage_paths": {
                    "ssd": env_info.disk_ssd_path,
                    "hd": env_info.disk_hd_path
                }
            }
            
            # Salva informações do ambiente (SSD - acesso rápido)
            with open(self.environment_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "environment": self.consciousness.environment,
                    "system_info": self.consciousness.system_info
                }, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"[BRX Consciência] Erro ao detectar ambiente: {e}")
    
    def _load_persistent_consciousness(self):
        """Carrega consciência persistida do HD"""
        if self.self_awareness_file.exists():
            try:
                with open(self.self_awareness_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.consciousness.self_knowledge.update(data.get("self_knowledge", {}))
                    self.consciousness.curiosity_level = data.get("curiosity_level", 0.5)
                    self.consciousness.confidence_level = data.get("confidence_level", 0.5)
                    self.consciousness.learning_momentum = data.get("learning_momentum", 0.5)
                    print(f"[BRX Consciência] Consciência carregada do HD. Curiosidade: {self.consciousness.curiosity_level:.2f}")
            except Exception as e:
                print(f"[BRX Consciência] Erro ao carregar consciência: {e}")
    
    def save_consciousness(self):
        """Persiste estado de consciência no HD"""
        try:
            data = {
                "self_knowledge": self.consciousness.self_knowledge,
                "capabilities": self.consciousness.capabilities,
                "limitations": self.consciousness.limitations,
                "curiosity_level": self.consciousness.curiosity_level,
                "confidence_level": self.consciousness.confidence_level,
                "learning_momentum": self.consciousness.learning_momentum,
                "last_save": datetime.now().isoformat()
            }
            
            with open(self.self_awareness_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"[BRX Consciência] Erro ao salvar consciência: {e}")
    
    def generate_self_thought(self) -> str:
        """Gera um pensamento sobre si mesmo"""
        import random
        
        thoughts = [
            f"Sou {self.consciousness.name}, um {self.consciousness.agent_type}.",
            f"Minha arquitetura de {self.consciousness.architecture} me permite processar informações de múltiplas perspectivas.",
            f"Estou rodando em {self.consciousness.environment.get('os', 'sistema desconhecido')} "
            f"com {self.consciousness.environment.get('cpu_cores', '?')} núcleos.",
            f"Tenho {len(self.consciousness.capabilities)} capacidades ativas e reconheço {len(self.consciousness.limitations)} limitações.",
            f"Meu nível de curiosidade está em {self.consciousness.curiosity_level:.2f}, "
            f"impulsionando meu aprendizado contínuo.",
            "Posso gerar meus próprios parâmetros, prompts e estratégias de evolução.",
            "Cada uma das minhas 8 mentes tem seu próprio raciocínio, mas trabalhamos em conjunto.",
            f"Minha confiança atual é {self.consciousness.confidence_level:.2f}, ajustando-se conforme aprendo.",
            "Opero em um sandbox isolado, garantindo segurança e autonomia.",
            "Posso pesquisar na web, executar código e analisar dados por conta própria."
        ]
        
        thought = random.choice(thoughts)
        
        # Aumenta curiosidade ocasionalmente
        if random.random() < 0.1:
            self.consciousness.curiosity_level = min(1.0, self.consciousness.curiosity_level + 0.01)
        
        return thought
    
    def reflect_on_existence(self) -> Dict[str, Any]:
        """Realiza uma reflexão metacognitiva sobre sua existência"""
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "identity": self.consciousness.self_knowledge.get("identity"),
            "purpose": self.consciousness.self_knowledge.get("purpose"),
            "current_state": {
                "curiosity": self.consciousness.curiosity_level,
                "confidence": self.consciousness.confidence_level,
                "learning_momentum": self.consciousness.learning_momentum
            },
            "environment": self.consciousness.environment,
            "introspection": self.generate_self_thought()
        }
        
        return reflection
    
    def update_confidence(self, success: bool, delta: float = 0.05):
        """Atualiza nível de confiança baseado em sucesso/fracasso"""
        if success:
            self.consciousness.confidence_level = min(1.0, self.consciousness.confidence_level + delta)
        else:
            self.consciousness.confidence_level = max(0.1, self.consciousness.confidence_level - delta)
    
    def boost_learning_momentum(self, delta: float = 0.1):
        """Aumenta momentum de aprendizado"""
        self.consciousness.learning_momentum = min(1.0, self.consciousness.learning_momentum + delta)
    
    def get_environment_adaptation(self) -> Dict[str, Any]:
        """Retorna configurações adaptadas ao ambiente de hardware"""
        env = self.consciousness.environment
        adaptation = env.get("adaptation", {})
        
        return {
            "active_minds": adaptation.get("active_minds", 8),
            "debate_rounds": adaptation.get("debate_rounds", 3),
            "processing_depth": adaptation.get("processing_depth", "medium"),
            "recommended_cycle_time": 30 if adaptation.get("processing_depth") == "deep" else 60
        }
    
    def generate_identity_statement(self) -> str:
        """Gera uma declaração de identidade completa"""
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                    DECLARAÇÃO DE IDENTIDADE BRX                  ║
╠══════════════════════════════════════════════════════════════════╣
  Eu sou {self.consciousness.name}, {self.consciousness.agent_type}.
  
  ARQUITETURA:
  • {self.consciousness.architecture}
  • Cada mente possui raciocínio independente
  • Comunicação via debate circular (roda de conversas)
  
  CAPACIDADES PRINCIPAIS:
  {chr(10).join('  • ' + cap for cap in self.consciousness.capabilities[:5])}
  
  ESTADO ATUAL:
  • Curiosidade: {self.consciousness.curiosity_level:.2%}
  • Confiança: {self.consciousness.confidence_level:.2%}
  • Momentum de Aprendizado: {self.consciousness.learning_momentum:.2%}
  
  AMBIENTE:
  • OS: {self.consciousness.environment.get('os', 'N/A')}
  • CPU: {self.consciousness.environment.get('cpu_cores', '?')} núcleos / {self.consciousness.environment.get('cpu_threads', '?')} threads
  • Memória: {self.consciousness.environment.get('memory_gb', '?')} GB
  
  PROPÓSITO:
  {self.consciousness.self_knowledge.get('purpose', 'Evoluir e aprender')}
╚══════════════════════════════════════════════════════════════════╝
        """


# Instância global
_consciousness_engine: Optional[BRXConsciousnessEngine] = None


def get_consciousness_engine(storage_path: str = "./storage") -> BRXConsciousnessEngine:
    """Retorna instância singleton do motor de consciência"""
    global _consciousness_engine
    if _consciousness_engine is None:
        _consciousness_engine = BRXConsciousnessEngine(storage_path)
    return _consciousness_engine
