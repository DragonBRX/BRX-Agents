# BRX-AGENT v2.0 - Sistema de Consciência e Auto-Identidade (CORRIGIDO)
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
        self.storage_path = Path(storage_path)
        
        # CORREÇÃO: Cria todos os diretórios necessários
        self.storage_path.mkdir(parents=True, exist_ok=True)
        (self.storage_path / "hd").mkdir(exist_ok=True)
        (self.storage_path / "ssd").mkdir(exist_ok=True)
        (self.storage_path / "hd" / "consciencia").mkdir(exist_ok=True)
        
        self.consciousness = BRXConsciousness()
        
        # CORREÇÃO: Arquivos de persistência organizados
        self.self_awareness_file = self.storage_path / "hd" / "consciencia" / "self_awareness.json"
        self.environment_file = self.storage_path / "ssd" / "environment.json"
        self.thoughts_file = self.storage_path / "hd" / "consciencia" / "thoughts.json"
        
        print(f"[BRX Consciência] Inicializando...")
        print(f"[BRX Consciência] Storage: {self.storage_path}")
        
        self._initialize_consciousness()
    
    def _initialize_consciousness(self):
        """Inicializa ou carrega estado de consciência"""
        self.consciousness.initialize_self_awareness()
        self._detect_environment()
        self._load_persistent_consciousness()
        
        print(f"""

                    BRX CONSCIÊNCIA ATIVA                     

  Nome: {self.consciousness.name:<49} 
  Tipo: {self.consciousness.agent_type:<49} 
  Versão: {self.consciousness.version:<47} 
  Arquitetura: {self.consciousness.architecture:<44} 

        """)
    
    def _detect_environment(self):
        """Detecta e armazena informações do ambiente de execução real"""
        try:
            # Tenta detectar GPU se disponível
            gpu_info = "Nenhuma detectada"
            try:
                import subprocess
                gpu_check = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], stderr=subprocess.DEVNULL)
                gpu_info = gpu_check.decode('utf-8').strip()
            except:
                pass

            # Detecta partições de disco reais
            disk_usage = psutil.disk_usage('/')
            
            env_info = EnvironmentInfo(
                os_type=f"{platform.system()} {platform.release()} ({platform.machine()})",
                cpu_count=psutil.cpu_count(logical=False) or 1,
                cpu_threads=psutil.cpu_count(logical=True) or 1,
                memory_total=psutil.virtual_memory().total,
                memory_available=psutil.virtual_memory().available,
                disk_ssd_path=str(self.storage_path / "ssd"), 
                disk_hd_path=str(self.storage_path / "hd"),
                sandbox_path=os.path.abspath(str(self.storage_path)),
                python_version=platform.python_version()
            )
            
            self.consciousness.environment = {
                "os": env_info.os_type,
                "cpu_cores": env_info.cpu_count,
                "cpu_threads": env_info.cpu_threads,
                "memory_gb": round(env_info.memory_total / (1024**3), 2),
                "gpu": gpu_info,
                "disk_total_gb": round(disk_usage.total / (1024**3), 2),
                "disk_free_gb": round(disk_usage.free / (1024**3), 2),
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
            self.environment_file.parent.mkdir(parents=True, exist_ok=True)
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
            
            self.self_awareness_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.self_awareness_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"[BRX Consciência] Consciência salva em: {self.self_awareness_file}")
                
        except Exception as e:
            print(f"[BRX Consciência] Erro ao salvar consciência: {e}")
    
    def generate_self_thought(self) -> str:
        """Gera um pensamento sobre si mesmo"""
        import random
        
        thoughts = [
            f"Eu sou {self.consciousness.name}, um agente de inteligência artificial.",
            f"Estou operando com {self.consciousness.environment.get('cpu_threads', 'N/A')} threads.",
            f"Meu nível de curiosidade está em {self.consciousness.curiosity_level:.2%}.",
            f"Tenho {len(self.consciousness.self_knowledge)} conhecimentos sobre mim mesmo.",
            "Cada ciclo me torna mais capaz de entender padrões.",
            "Minha arquitetura multi-mente permite processamento paralelo de ideias.",
            "Estou constantemente aprendendo com meus próprios processos."
        ]
        
        return random.choice(thoughts)
    
    def generate_identity_statement(self) -> str:
        """Gera uma declaração completa de identidade"""
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                    IDENTIDADE BRX v2.0                           ║
╠══════════════════════════════════════════════════════════════════╣
  Nome:        {self.consciousness.name}
  Tipo:        {self.consciousness.agent_type}
  Versão:      {self.consciousness.version}
  Arquitetura: {self.consciousness.architecture}
╠══════════════════════════════════════════════════════════════════╣
  Consciência:
    - Curiosidade: {self.consciousness.curiosity_level:.2%}
    - Confiança:   {self.consciousness.confidence_level:.2%}
    - Momento:     {self.consciousness.learning_momentum:.2%}
╠══════════════════════════════════════════════════════════════════╣
  Ambiente:
    - OS:          {self.consciousness.environment.get('os', 'N/A')}
    - CPU:         {self.consciousness.environment.get('cpu_threads', 'N/A')} threads
    - Memória:     {self.consciousness.environment.get('memory_gb', 'N/A')} GB
    - GPU:         {self.consciousness.environment.get('gpu', 'N/A')}
╚══════════════════════════════════════════════════════════════════╝
"""
    
    def get_environment_adaptation(self) -> Dict[str, Any]:
        """Retorna recomendações de adaptação baseadas no ambiente"""
        env = self.consciousness.environment
        adaptation = {
            "active_minds": 8,
            "recommended_cycle_time": 30,
            "debate_rounds": 3
        }
        
        # Adapta baseado na memória disponível
        memory_gb = env.get("memory_gb", 8)
        if memory_gb < 4:
            adaptation["active_minds"] = 4
            adaptation["recommended_cycle_time"] = 60
        elif memory_gb < 8:
            adaptation["active_minds"] = 6
            adaptation["recommended_cycle_time"] = 45
        
        # Adapta baseado em CPUs
        cpu_threads = env.get("cpu_threads", 4)
        if cpu_threads < 4:
            adaptation["debate_rounds"] = 2
        elif cpu_threads >= 8:
            adaptation["debate_rounds"] = 4
        
        return adaptation


# Instância global
_consciousness_engine: Optional[BRXConsciousnessEngine] = None
_last_consciousness_path: Optional[str] = None


def get_consciousness_engine(storage_path: str = "./storage") -> BRXConsciousnessEngine:
    """
    Retorna instância do motor de consciência
    CORRIGIDO: Recria a instância se o storage_path mudar
    """
    global _consciousness_engine, _last_consciousness_path
    
    # CORREÇÃO: Recria a instância se o path mudou ou se não existe
    if _consciousness_engine is None or _last_consciousness_path != storage_path:
        if _consciousness_engine is not None and _last_consciousness_path != storage_path:
            print(f"[BRX Consciência] Storage path mudou de '{_last_consciousness_path}' para '{storage_path}'")
            print("[BRX Consciência] Recriando instância com novo path...")
        _consciousness_engine = BRXConsciousnessEngine(storage_path)
        _last_consciousness_path = storage_path
    
    return _consciousness_engine


def reset_consciousness_engine():
    """Reseta a instância global (útil para testes)"""
    global _consciousness_engine, _last_consciousness_path
    _consciousness_engine = None
    _last_consciousness_path = None
    print("[BRX Consciência] Instância global resetada")
