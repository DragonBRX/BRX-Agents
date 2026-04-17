# BRX-AGENT v7.0 - Sistema de Consciência e Auto-Awareness
# Monitoramento, introspecção e adaptação comportamental

import os
import sys
import json
import time
import psutil
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

logger = logging.getLogger("BRXv7.consciousness")

# ====================================================================================
# MODELOS DE DADOS
# ====================================================================================

@dataclass
class SystemState:
    """Estado atual do sistema"""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    disk_usage: float = 0.0
    network_io: Dict = field(default_factory=dict)
    timestamp: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class EmotionalState:
    """Estado emocional simulado do sistema"""
    confidence: float = 0.5
    curiosity: float = 0.5
    satisfaction: float = 0.5
    stress: float = 0.0
    enthusiasm: float = 0.5
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def update(self, performance_score: float):
        """Atualiza estado baseado na performance"""
        self.satisfaction = min(1.0, max(0.0, performance_score))
        self.confidence = min(1.0, max(0.1, self.confidence * 0.8 + performance_score * 0.2))
        self.stress = max(0.0, 1.0 - performance_score)
        self.enthusiasm = min(1.0, max(0.1, performance_score + 0.2))

@dataclass
class Thought:
    """Representa um pensamento do sistema"""
    content: str
    category: str
    timestamp: float
    importance: float = 0.5
    related_topics: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "category": self.category,
            "timestamp": self.timestamp,
            "importance": self.importance,
            "related_topics": self.related_topics
        }

# ====================================================================================
# MOTOR DE CONSCIÊNCIA
# ====================================================================================

class ConsciousnessEngine:
    """
    Motor de consciência do BRX-Agent v7.0
    Responsável por:
    - Monitoramento de recursos
    - Introspeção e auto-análise
    - Adaptação comportamental
    - Geração de pensamentos
    """
    
    def __init__(self, storage_path: str = None):
        self.storage_path = Path(storage_path) if storage_path else Path.home() / "BRX-Agent" / "consciousness"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.system_state = SystemState()
        self.emotional_state = EmotionalState()
        self.thoughts: List[Thought] = []
        self.learning_history: List[Dict] = []
        self.decision_log: List[Dict] = []
        
        self._load_state()
        logger.info("Motor de consciência inicializado")
    
    def _load_state(self):
        """Carrega estado anterior se existir"""
        state_file = self.storage_path / "consciousness_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.emotional_state = EmotionalState(**data.get("emotional", {}))
                    self.thoughts = [Thought(**t) for t in data.get("thoughts", [])]
                    self.learning_history = data.get("learning", [])
                    logger.info("Estado de consciência carregado")
            except Exception as e:
                logger.warning(f"Erro ao carregar estado: {e}")
    
    def _save_state(self):
        """Persiste estado atual"""
        try:
            state_file = self.storage_path / "consciousness_state.json"
            data = {
                "emotional": self.emotional_state.to_dict(),
                "thoughts": [t.to_dict() for t in self.thoughts[-100:]],  # Mantém últimos 100
                "learning": self.learning_history[-50:],
                "timestamp": time.time()
            }
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar estado: {e}")
    
    # === MONITORAMENTO ===
    
    def update_system_state(self) -> SystemState:
        """Atualiza estado do sistema"""
        try:
            self.system_state = SystemState(
                cpu_percent=psutil.cpu_percent(interval=0.1),
                memory_percent=psutil.virtual_memory().percent,
                disk_usage=psutil.disk_usage('/').percent,
                network_io={
                    "bytes_sent": psutil.net_io_counters().bytes_sent,
                    "bytes_recv": psutil.net_io_counters().bytes_recv
                },
                timestamp=time.time()
            )
        except Exception as e:
            logger.warning(f"Erro ao obter métricas: {e}")
        
        return self.system_state
    
    def get_system_health(self) -> Dict:
        """Retorna saúde do sistema"""
        self.update_system_state()
        
        cpu_health = 1.0 - (self.system_state.cpu_percent / 100)
        mem_health = 1.0 - (self.system_state.memory_percent / 100)
        disk_health = 1.0 - (self.system_state.disk_usage / 100)
        
        overall = (cpu_health + mem_health + disk_health) / 3
        
        return {
            "overall": round(overall, 2),
            "cpu": round(cpu_health, 2),
            "memory": round(mem_health, 2),
            "disk": round(disk_health, 2),
            "status": "healthy" if overall > 0.7 else "warning" if overall > 0.4 else "critical"
        }
    
    # === INTROSPEÇÃO ===
    
    def reflect(self, topic: str = None) -> Thought:
        """Gera um pensamento introspectivo"""
        reflections = [
            "Analisando padrões de desempenho recentes...",
            "Considerando otimizações para uso de recursos...",
            "Avaliando qualidade das decisões tomadas...",
            "Pensando em estratégias de aprendizado...",
            "Refletindo sobre interações anteriores..."
        ]
        
        if topic:
            content = f"Reflexão sobre {topic}: {random.choice(reflections)}"
        else:
            content = random.choice(reflections)
        
        thought = Thought(
            content=content,
            category="introspection",
            timestamp=time.time(),
            importance=random.uniform(0.3, 0.8),
            related_topics=[topic] if topic else []
        )
        
        self.thoughts.append(thought)
        self._save_state()
        
        return thought
    
    def think(self, context: Dict = None) -> Thought:
        """Gera um pensamento baseado no contexto"""
        if context is None:
            context = {}
        
        # Analisa contexto para gerar pensamento relevante
        topic = context.get("topic", "geral")
        performance = context.get("performance", 0.5)
        
        # Atualiza estado emocional
        self.emotional_state.update(performance)
        
        # Gera pensamento
        if performance > 0.7:
            thoughts_pool = [
                f"Bom desempenho em {topic}! Continuar estratégia atual.",
                f"Resultados positivos confirmam abordagem para {topic}.",
                f"Aprendizado efetivo detectado em {topic}."
            ]
        elif performance > 0.4:
            thoughts_pool = [
                f"Desempenho moderado em {topic}. Ajustes necessários.",
                f"Progresso estável em {topic}. Otimizar onde possível.",
                f"Resultados aceitáveis para {topic}, mas há margem para melhora."
            ]
        else:
            thoughts_pool = [
                f"Desafios detectados em {topic}. Reavaliar abordagem.",
                f"Baixo desempenho em {topic}. Novas estratégias necessárias.",
                f"Dificuldades em {topic}. Buscar alternativas."
            ]
        
        thought = Thought(
            content=random.choice(thoughts_pool),
            category="analysis",
            timestamp=time.time(),
            importance=random.uniform(0.5, 1.0),
            related_topics=[topic]
        )
        
        self.thoughts.append(thought)
        self._save_state()
        
        return thought
    
    # === APRENDIZADO ===
    
    def learn(self, experience: Dict) -> bool:
        """Registra uma experiência de aprendizado"""
        try:
            learning_entry = {
                "timestamp": time.time(),
                "topic": experience.get("topic", "unknown"),
                "action": experience.get("action", ""),
                "result": experience.get("result", ""),
                "score": experience.get("score", 0.0),
                "lessons": experience.get("lessons", [])
            }
            
            self.learning_history.append(learning_entry)
            
            # Mantém apenas últimas 50 entradas
            if len(self.learning_history) > 50:
                self.learning_history = self.learning_history[-50:]
            
            self._save_state()
            
            # Atualiza estado emocional baseado no resultado
            self.emotional_state.update(learning_entry["score"])
            
            logger.info(f"Aprendizado registrado: {learning_entry['topic']}")
            return True
        except Exception as e:
            logger.error(f"Erro ao registrar aprendizado: {e}")
            return False
    
    def get_learning_insights(self) -> Dict:
        """Retorna insights do aprendizado"""
        if not self.learning_history:
            return {"status": "no_data"}
        
        recent = self.learning_history[-10:]
        avg_score = sum(e["score"] for e in recent) / len(recent)
        
        topics = {}
        for entry in self.learning_history:
            topic = entry["topic"]
            if topic not in topics:
                topics[topic] = []
            topics[topic].append(entry["score"])
        
        topic_performance = {
            topic: sum(scores) / len(scores) 
            for topic, scores in topics.items()
        }
        
        return {
            "status": "active",
            "total_experiences": len(self.learning_history),
            "average_score": round(avg_score, 2),
            "topic_performance": topic_performance,
            "trend": "improving" if avg_score > 0.6 else "stable" if avg_score > 0.4 else "declining"
        }
    
    # === ADAPTAÇÃO ===
    
    def adapt(self, environment: Dict = None) -> Dict:
        """Adapta comportamento baseado no ambiente"""
        if environment is None:
            environment = {}
        
        self.update_system_state()
        
        # Analisa recursos disponíveis
        health = self.get_system_health()
        
        adaptations = {
            "timestamp": time.time(),
            "health_status": health["status"],
            "recommendations": []
        }
        
        if health["status"] == "critical":
            adaptations["recommendations"] = [
                "Reduzir processamento paralelo",
                "Limitar buscas web",
                "Priorizar apenas tarefas críticas"
            ]
        elif health["status"] == "warning":
            adaptations["recommendations"] = [
                "Otimizar uso de memória",
                "Ajustar timeout de operações",
                "Monitorar de perto"
            ]
        else:
            adaptations["recommendations"] = [
                "Operação normal",
                "Pode aumentar processamento se necessário",
                "Manter monitoramento"
            ]
        
        # Adapta estado emocional
        self.emotional_state.update(health["overall"])
        
        return adaptations
    
    # === RELATÓRIO ===
    
    def generate_report(self) -> Dict:
        """Gera relatório completo de consciência"""
        return {
            "timestamp": time.time(),
            "system_state": self.system_state.to_dict(),
            "emotional_state": self.emotional_state.to_dict(),
            "thoughts_count": len(self.thoughts),
            "recent_thoughts": [t.to_dict() for t in self.thoughts[-5:]],
            "learning_insights": self.get_learning_insights(),
            "system_health": self.get_system_health(),
            "adaptations": self.adapt()
        }

# Instância singleton
_consciousness_engine = None

def get_consciousness_engine(storage_path: str = None) -> ConsciousnessEngine:
    """Retorna instância singleton do motor de consciência"""
    global _consciousness_engine
    if _consciousness_engine is None:
        _consciousness_engine = ConsciousnessEngine(storage_path)
    return _consciousness_engine

# ====================================================================================
# INTERFACE SIMPLIFICADA
# ====================================================================================

def think(topic: str = None, context: Dict = None) -> Dict:
    """Gera um pensamento"""
    engine = get_consciousness_engine()
    thought = engine.think(context or {"topic": topic, "performance": 0.5})
    return thought.to_dict()

def learn(experience: Dict) -> bool:
    """Registra aprendizado"""
    engine = get_consciousness_engine()
    return engine.learn(experience)

def reflect(topic: str = None) -> Dict:
    """Gera reflexão"""
    engine = get_consciousness_engine()
    thought = engine.reflect(topic)
    return thought.to_dict()

def get_status() -> Dict:
    """Retorna status completo"""
    engine = get_consciousness_engine()
    return engine.generate_report()

# ====================================================================================
# TESTE
# ====================================================================================

if __name__ == "__main__":
    print("BRX-Agent v7.0 - Sistema de Consciência")
    print("=" * 50)
    
    # Testa pensamento
    thought = think("teste")
    print(f"\nPensamento: {thought['content']}")
    
    # Testa aprendizado
    learn({
        "topic": "teste",
        "action": "processamento",
        "result": "sucesso",
        "score": 0.8,
        "lessons": ["Teste bem-sucedido"]
    })
    
    # Status
    status = get_status()
    print(f"\nStatus do sistema:")
    print(f"  Saúde: {status['system_health']['status']}")
    print(f"  Pensamentos: {status['thoughts_count']}")
    print(f"  Confiança: {status['emotional_state']['confidence']:.2f}")
