# BRX-AGENT v2.0 - Núcleo Principal
# Integra consciência, 8 mentes, geração de parâmetros e pesquisa

import os
import sys
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from dataclasses import dataclass, field

# Importa componentes
from core.types import (
    AgentParameter, ParameterType, CircularDebate, 
    EvolutionCycle, MemoryEntry, ToolResult
)
from consciousness.self_awareness import BRXConsciousnessEngine, get_consciousness_engine
from minds.eight_minds import EightMindsSystem, Mind
from parameters.auto_generator import BRXParameterGenerator
from search.duckdns_search import DuckDNSSearcher, get_searcher


@dataclass
class BRXState:
    """Estado completo do BRX"""
    version: str = "2.0.0"
    cycle: int = 0
    is_running: bool = False
    start_time: float = 0.0
    last_cycle_time: float = 0.0
    parameters_count: int = 0
    debates_count: int = 0
    searches_count: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "cycle": self.cycle,
            "is_running": self.is_running,
            "uptime": time.time() - self.start_time if self.start_time > 0 else 0,
            "parameters_count": self.parameters_count,
            "debates_count": self.debates_count,
            "searches_count": self.searches_count
        }


class BRXCore:
    """
    Núcleo do BRX-Agent v2.0
    Integra todos os componentes em um sistema coeso e auto-evolutivo
    """
    
    def __init__(self, storage_path: str = "./storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Cria estrutura de diretórios SSD/HD
        (self.storage_path / "ssd").mkdir(exist_ok=True)
        (self.storage_path / "hd").mkdir(exist_ok=True)
        (self.storage_path / "logs").mkdir(exist_ok=True)
        
        print("""

                                                                              
                    
            
                
                
                     
                          
                                                                              
                    AGENTE AUTO-EVOLUTIVO MULTI-CÉREBRO                       
                              Versão 2.0.0                                    

        """)
        
        # Inicializa componentes
        print("[BRX Core] Inicializando componentes...")
        
        # 1. Consciência
        self.consciousness = get_consciousness_engine(str(self.storage_path))
        print(f"[BRX Core]  Consciência ativa: {self.consciousness.consciousness.name}")
        
        # 2. Sistema de 8 Mentes (adapta ao hardware)
        adaptation = self.consciousness.get_environment_adaptation()
        active_minds = adaptation.get("active_minds", 8)
        self.minds = EightMindsSystem(active_minds=active_minds)
        print(f"[BRX Core]  Sistema de {active_minds} mentes inicializado")
        
        # 3. Gerador de Parâmetros
        self.param_generator = BRXParameterGenerator(str(self.storage_path))
        print(f"[BRX Core]  Gerador de parâmetros ativo (vocabulário: {self.param_generator.get_vocabulary_size()} palavras)")
        
        # 4. Pesquisador DuckDNS
        self.searcher = get_searcher(str(self.storage_path / "hd" / "search_cache.json"))
        print(f"[BRX Core]  Pesquisador DuckDNS pronto")
        
        # Estado do sistema
        self.state = BRXState()
        self.parameters: List[AgentParameter] = []
        self.evolution_history: List[EvolutionCycle] = []
        self.memory: List[MemoryEntry] = []
        
        # Callbacks
        self.cycle_callbacks: List[Callable] = []
        self.thought_callbacks: List[Callable] = []
        
        # Configurações
        self.config = {
            "cycle_interval": adaptation.get("recommended_cycle_time", 30),
            "debate_rounds": adaptation.get("debate_rounds", 3),
            "auto_evolve": True,
            "curiosity_driven": True
        }
        
        # Registra handlers
        self._register_internal_handlers()
        
        print(f"[BRX Core] Sistema pronto para operação autônoma")
        print(f"[BRX Core] Modo: {'Auto-evolutivo' if self.config['auto_evolve'] else 'Manual'}")
    
    def _register_internal_handlers(self):
        """Registra handlers internos para observar o sistema"""
        
        def on_thought(thought: str, mind_role, topic: str):
            """Handler de pensamentos das mentes"""
            # Armazena pensamento importante na memória
            if "importante" in thought.lower() or "crítico" in thought.lower():
                self._store_memory(
                    content=thought,
                    context=f"pensamento_{mind_role.value}",
                    importance=0.7
                )
        
        self.minds.register_thought_handler(on_thought)
    
    def _store_memory(self, content: str, context: str, importance: float = 0.5):
        """Armazena informação na memória"""
        memory = MemoryEntry(
            id=f"mem_{datetime.now().timestamp()}_{random.randint(1000, 9999)}",
            content=content,
            memory_type="short" if importance < 0.5 else "medium" if importance < 0.8 else "long",
            importance=importance,
            timestamp=datetime.now().timestamp(),
            access_count=0,
            last_access=datetime.now().timestamp(),
            associations=[],
            context=context
        )
        self.memory.append(memory)
        
        # Limita memória
        if len(self.memory) > 10000:
            self.memory = sorted(self.memory, key=lambda m: m.importance, reverse=True)[:8000]
    
    def process_request(self, request: str, context: str = "") -> Dict[str, Any]:
        """
        Processa uma solicitação do usuário usando o sistema de 8 mentes
        """
        print(f"\n[BRX] Processando solicitação: '{request[:50]}...'")
        
        # 1. Realiza debate circular entre as mentes
        debate = self.minds.conduct_circular_debate(
            topic=request,
            context=context,
            max_rounds=self.config["debate_rounds"]
        )
        
        self.state.debates_count += 1
        
        # 2. Coleta parâmetros gerados
        debate_params = debate.parameters
        self.parameters.extend(debate_params)
        self.state.parameters_count += len(debate_params)
        
        # 3. Verifica se precisa de pesquisa
        search_results = []
        if self._should_search(request):
            search_results = self.searcher.search(request, max_results=3)
            self.state.searches_count += len(search_results)
        
        # 4. Gera parâmetros adicionais
        additional_params = self.param_generator.generate_comprehensive_params(
            context=request[:50]
        )
        self.parameters.extend(additional_params)
        self.state.parameters_count += len(additional_params)
        
        # 5. Armazena na memória
        self._store_memory(
            content=f"Processamento: {request} | Consenso: {debate.final_consensus[:100]}",
            context="processamento",
            importance=debate.consensus_confidence
        )
        
        return {
            "request": request,
            "consensus": debate.final_consensus,
            "confidence": debate.consensus_confidence,
            "debate": debate,
            "parameters_generated": len(debate_params) + len(additional_params),
            "search_results": search_results,
            "duration": debate.get_duration()
        }
    
    def _should_search(self, request: str) -> bool:
        """Determina se a solicitação requer pesquisa web"""
        search_keywords = [
            "pesquisar", "buscar", "encontrar", "procurar", "pesquisa",
            "quem é", "o que é", "quando", "onde", "como",
            "notícias", "atual", "recente", "novo", "último",
            "wikipedia", "definição", "significado", "história"
        ]
        
        request_lower = request.lower()
        return any(kw in request_lower for kw in search_keywords)
    
    def run_evolution_cycle(self) -> EvolutionCycle:
        """
        Executa um ciclo de evolução autônoma
        O BRX melhora seus próprios parâmetros e estratégias
        """
        self.state.cycle += 1
        cycle_start = time.time()
        
        print(f"\n[BRX Evolução] Ciclo #{self.state.cycle} iniciado")
        
        params_before = len(self.parameters)
        
        # 1. Gera novos parâmetros auto-evolutivos
        new_params = self.param_generator.generate_comprehensive_params(
            context=f"evolution_cycle_{self.state.cycle}"
        )
        
        # 2. Realiza debate interno sobre evolução
        evolution_topic = f"Como posso melhorar meu desempenho no ciclo {self.state.cycle}?"
        debate = self.minds.conduct_circular_debate(
            topic=evolution_topic,
            max_rounds=2
        )
        
        # 3. Identifica insights de aprendizado
        insights = self._extract_learning_insights(debate)
        
        # 4. Aplica melhorias baseadas nos insights
        improvements = self._apply_improvements(insights)
        
        # 5. Detecta parâmetros obsoletos
        deprecated = self._detect_deprecated_params()
        
        # Adiciona novos parâmetros
        self.parameters.extend(new_params)
        
        # Cria registro do ciclo
        cycle = EvolutionCycle(
            cycle_number=self.state.cycle,
            parameters_before=params_before,
            parameters_after=len(self.parameters),
            new_parameters=new_params,
            improved_parameters=improvements,
            deprecated_parameters=deprecated,
            learning_insights=insights,
            timestamp=cycle_start,
            self_modifications=[]
        )
        
        self.evolution_history.append(cycle)
        
        # Limita histórico
        if len(self.evolution_history) > 100:
            self.evolution_history = self.evolution_history[-100:]
        
        # Atualiza estado
        self.state.last_cycle_time = time.time()
        self.state.parameters_count = len(self.parameters)
        
        # Notifica callbacks
        for callback in self.cycle_callbacks:
            try:
                callback(cycle)
            except Exception as e:
                print(f"[BRX] Erro em callback de ciclo: {e}")
        
        print(f"[BRX Evolução] Ciclo #{self.state.cycle} completado em {time.time() - cycle_start:.2f}s")
        print(f"[BRX Evolução] Novos parâmetros: {len(new_params)} | Insights: {len(insights)}")
        
        return cycle
    
    def _extract_learning_insights(self, debate: CircularDebate) -> List[str]:
        """Extrai insights de aprendizado do debate"""
        insights = []
        
        # Analisa contribuições de cada mente
        for round in debate.rounds:
            if "melhorar" in round.output.lower():
                insights.append(f"{round.mind_name}: Sugestão de melhoria identificada")
            if "padrão" in round.output.lower():
                insights.append(f"{round.mind_name}: Padrão detectado para otimização")
            if "aprender" in round.output.lower():
                insights.append(f"{round.mind_name}: Oportunidade de aprendizado")
        
        # Adiciona insights baseados em estatísticas
        stats = self.param_generator.get_stats()
        if stats.get("words", 0) > 100:
            insights.append("Vocabulário suficiente para expansão de conceitos")
        
        return insights
    
    def _apply_improvements(self, insights: List[str]) -> List[str]:
        """Aplica melhorias baseadas nos insights"""
        improvements = []
        
        for insight in insights:
            if "melhoria" in insight.lower():
                # Aumenta curiosidade
                self.consciousness.consciousness.curiosity_level = min(
                    1.0, 
                    self.consciousness.consciousness.curiosity_level + 0.05
                )
                improvements.append("curiosity_level aumentado")
            
            if "padrão" in insight.lower():
                # Gera mais padrões
                pattern_params = self.param_generator.generate_pattern_params(count=3)
                self.parameters.extend(pattern_params)
                improvements.append(f"{len(pattern_params)} padrões adicionais gerados")
        
        return improvements
    
    def _detect_deprecated_params(self) -> List[str]:
        """Detecta parâmetros que podem ser obsoletos"""
        deprecated = []
        current_time = time.time()
        
        for param in self.parameters:
            # Parâmetros não usados há muito tempo
            if current_time - param.timestamp > 86400 * 7:  # 7 dias
                if param.usage_count < 2:
                    deprecated.append(param.id)
        
        return deprecated
    
    def generate_self_prompt(self) -> str:
        """Gera um prompt auto-evolutivo baseado no estado atual"""
        reflection = self.consciousness.generate_self_thought()
        
        prompt = f"""
[BRX AUTO-PROMPT #{self.state.cycle}]

Contexto atual:
- Ciclo de evolução: {self.state.cycle}
- Parâmetros ativos: {len(self.parameters)}
- Debates realizados: {self.state.debates_count}
- Nível de curiosidade: {self.consciousness.consciousness.curiosity_level:.2%}

Reflexão: {reflection}

Objetivo auto-gerado: Continue evoluindo, aprendendo e expandindo meu conhecimento.
Explore novos padrões, desenvolva meu vocabulário e refine minhas estratégias.

Próximas ações sugeridas:
1. Gerar novos parâmetros de vocabulário
2. Realizar debate interno sobre eficiência
3. Pesquisar tópicos de interesse emergente
4. Consolidar memórias importantes
"""
        return prompt
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        return {
            "state": self.state.to_dict(),
            "consciousness": {
                "name": self.consciousness.consciousness.name,
                "curiosity": self.consciousness.consciousness.curiosity_level,
                "confidence": self.consciousness.consciousness.confidence_level,
                "learning_momentum": self.consciousness.consciousness.learning_momentum
            },
            "minds": {
                "active": len(self.minds.get_active_minds()),
                "total": 8
            },
            "parameters": {
                "total": len(self.parameters),
                "by_type": self._count_params_by_type()
            },
            "memory": {
                "total": len(self.memory),
                "short": len([m for m in self.memory if m.memory_type == "short"]),
                "medium": len([m for m in self.memory if m.memory_type == "medium"]),
                "long": len([m for m in self.memory if m.memory_type == "long"])
            },
            "vocabulary": {
                "size": self.param_generator.get_vocabulary_size(),
                "stats": self.param_generator.get_stats()
            },
            "config": self.config
        }
    
    def _count_params_by_type(self) -> Dict[str, int]:
        """Conta parâmetros por tipo"""
        counts = {}
        for param in self.parameters:
            ptype = param.param_type.value
            counts[ptype] = counts.get(ptype, 0) + 1
        return counts
    
    def save_state(self):
        """Salva estado completo no HD"""
        state_file = self.storage_path / "hd" / "brx_state.json"
        
        data = {
            "state": self.state.to_dict(),
            "parameters": [p.to_dict() for p in self.parameters[-1000:]],  # Últimos 1000
            "config": self.config,
            "saved_at": datetime.now().isoformat()
        }
        
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[BRX] Estado salvo em {state_file}")
        except Exception as e:
            print(f"[BRX] Erro ao salvar estado: {e}")
    
    def load_state(self):
        """Carrega estado do HD"""
        state_file = self.storage_path / "hd" / "brx_state.json"
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Restaura estado
                if "state" in data:
                    self.state.cycle = data["state"].get("cycle", 0)
                    self.state.parameters_count = data["state"].get("parameters_count", 0)
                
                print(f"[BRX] Estado carregado: ciclo #{self.state.cycle}")
            except Exception as e:
                print(f"[BRX] Erro ao carregar estado: {e}")
    
    def generate_identity(self) -> str:
        """Gera declaração de identidade completa"""
        return self.consciousness.generate_identity_statement()


# Instância global
_brx_core: Optional[BRXCore] = None


def get_brx_core(storage_path: str = "./storage") -> BRXCore:
    """Retorna instância singleton do núcleo BRX"""
    global _brx_core
    if _brx_core is None:
        _brx_core = BRXCore(storage_path)
    return _brx_core
