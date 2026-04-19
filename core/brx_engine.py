# BRX-AGENT v3.0 - Nucleo Principal com Sistema Multi-Agente
# Integra consciencia, 8 mentes, sistema multi-agente e pesquisa

import os
import sys
import json
import time
import random
import multiprocessing
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from dataclasses import dataclass, field

# Importa componentes
from core.types import (
    AgentParameter, ParameterType, CircularDebate, 
    EvolutionCycle, MemoryEntry, ToolResult,
    AgentRegistry, SpecializedAgent, CollaborativeTask,
    AgentCategory
)
from consciousness.self_awareness import BRXConsciousnessEngine, get_consciousness_engine
from minds.eight_minds import EightMindsSystem, Mind
from parameters.auto_generator import BRXParameterGenerator
from search.duckdns_search import DuckDNSSearcher, get_searcher

# NOVO: Sistema Multi-Agente v3.0
from core.task_analyzer import TaskAnalyzer
from core.agent_orchestrator import AgentOrchestrator, get_orchestrator
from core.collaborative_workspace import get_workspace_manager
from agents.agent_catalog import get_agent_registry


@dataclass
class BRXState:
    """Estado completo do BRX"""
    version: str = "3.0.0"
    cycle: int = 0
    is_running: bool = False
    start_time: float = 0.0
    last_cycle_time: float = 0.0
    parameters_count: int = 0
    debates_count: int = 0
    searches_count: int = 0
    tasks_completed: int = 0
    agents_activated_total: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "cycle": self.cycle,
            "is_running": self.is_running,
            "uptime": time.time() - self.start_time if self.start_time > 0 else 0,
            "parameters_count": self.parameters_count,
            "debates_count": self.debates_count,
            "searches_count": self.searches_count,
            "tasks_completed": self.tasks_completed,
            "agents_activated_total": self.agents_activated_total
        }


class BRXCore:
    """
    Nucleo do BRX-Agent v3.0
    Agora com Sistema Multi-Agente Dinamico
    - 8 mentes base (sempre ativas)
    - 100+ agentes especializados (ativados por tarefa)
    - Orquestracao inteligente
    - Workspace colaborativo
    """
    
    def __init__(self, storage_path: str = "./storage", max_agents: int = None):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Cria estrutura de diretorios
        (self.storage_path / "ssd").mkdir(exist_ok=True)
        (self.storage_path / "hd").mkdir(exist_ok=True)
        (self.storage_path / "logs").mkdir(exist_ok=True)
        (self.storage_path / "hd" / "parametros").mkdir(exist_ok=True)
        (self.storage_path / "hd" / "memoria").mkdir(exist_ok=True)
        (self.storage_path / "hd" / "consciencia").mkdir(exist_ok=True)
        (self.storage_path / "hd" / "agentes").mkdir(exist_ok=True)
        (self.storage_path / "hd" / "workspaces").mkdir(exist_ok=True)
        
        # Detecta threads do CPU para default de agentes
        cpu_threads = multiprocessing.cpu_count()
        self.max_agents = max_agents or min(8, cpu_threads)
        self.max_workers = cpu_threads
        
        print(f"""
                                                                              
                    
            
                
                
                     
                          
                                                                              
                    AGENTE AUTO-EVOLUTIVO MULTI-CEREBRO v3.0                  
                    Sistema Multi-Agente Dinamico ({self.max_agents} agentes)     
                                                                              
                                                                              
        """)
        
        # Inicializa componentes
        print("[BRX Core v3.0] Inicializando componentes...")
        print(f"[BRX Core] Storage path: {self.storage_path}")
        print(f"[BRX Core] CPU threads detectados: {cpu_threads}")
        print(f"[BRX Core] Max agentes: {self.max_agents}")
        
        # 1. Consciencia
        self.consciousness = get_consciousness_engine(str(self.storage_path))
        print(f"[BRX Core]  Consciencia ativa: {self.consciousness.consciousness.name}")
        
        # 2. Sistema de 8 Mentes base (sempre ativas)
        adaptation = self.consciousness.get_environment_adaptation()
        active_minds = adaptation.get("active_minds", 8)
        self.minds = EightMindsSystem(active_minds=active_minds)
        print(f"[BRX Core]  Sistema de {active_minds} mentes base inicializado")
        
        # 3. Gerador de Parametros
        self.param_generator = BRXParameterGenerator(str(self.storage_path))
        print(f"[BRX Core]  Gerador de parametros ativo (vocabulario: {self.param_generator.get_vocabulary_size()} palavras)")
        
        # 4. Pesquisador DuckDNS
        self.searcher = get_searcher(str(self.storage_path / "hd" / "search_cache.json"))
        print(f"[BRX Core]  Pesquisador DuckDNS pronto")
        
        # 5. NOVO: Registro de Agentes (100+)
        self.agent_registry = get_agent_registry()
        print(f"[BRX Core]  Catalogo de {len(self.agent_registry.agents)} agentes especializados carregado")
        
        # 6. NOVO: Analisador de Tarefas
        self.task_analyzer = TaskAnalyzer(max_agents=self.max_agents)
        print(f"[BRX Core]  Analisador de tarefas pronto")
        
        # 7. NOVO: Orquestrador de Agentes
        self.orchestrator = get_orchestrator(max_agents=self.max_agents, max_workers=self.max_workers)
        print(f"[BRX Core]  Orquestrador multi-agente ativo")
        
        # 8. NOVO: Gerenciador de Workspaces
        self.workspace_manager = get_workspace_manager()
        print(f"[BRX Core]  Workspace colaborativo pronto")
        
        # Estado do sistema
        self.state = BRXState()
        self.parameters: List[AgentParameter] = []
        self.evolution_history: List[EvolutionCycle] = []
        self.memory: List[MemoryEntry] = []
        
        # Callbacks
        self.cycle_callbacks: List[Callable] = []
        self.thought_callbacks: List[Callable] = []
        
        # Configuracoes
        self.config = {
            "cycle_interval": adaptation.get("recommended_cycle_time", 30),
            "debate_rounds": adaptation.get("debate_rounds", 3),
            "auto_evolve": True,
            "curiosity_driven": True,
            "multi_agent_enabled": True,
            "max_agents": self.max_agents,
            "max_workers": self.max_workers
        }
        
        # Registra handlers
        self._register_internal_handlers()
        
        print(f"[BRX Core] Sistema pronto para operacao autonoma")
        print(f"[BRX Core] Modo: {'Multi-Agente Dinamico' if self.config['multi_agent_enabled'] else 'Mentes Base'}")
        print(f"[BRX Core] Diretorio de dados: {self.storage_path}")
    
    def _register_internal_handlers(self):
        """Registra handlers internos para observar o sistema"""
        
        def on_thought(thought: str, mind_role, topic: str):
            """Handler de pensamentos das mentes"""
            if "importante" in thought.lower() or "critico" in thought.lower():
                self._store_memory(
                    content=thought,
                    context=f"pensamento_{mind_role.value}",
                    importance=0.7
                )
        
        self.minds.register_thought_handler(on_thought)
    
    def _store_memory(self, content: str, context: str, importance: float = 0.5):
        """Armazena informacao na memoria"""
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
        
        # Limita memoria
        if len(self.memory) > 10000:
            self.memory = sorted(self.memory, key=lambda m: m.importance, reverse=True)[:8000]
    
    # ===================================================================
    # NOVO: Sistema Multi-Agente v3.0
    # ===================================================================
    
    def process_request_multi_agent(self, request: str, context: str = "") -> Dict[str, Any]:
        """
        Processa uma solicitacao usando o sistema multi-agente dinamico
        - Analisa a tarefa
        - Ativa os agentes especializados adequados
        - Executa trabalho colaborativo
        - Retorna resultado consolidado
        """
        print(f"\n[BRX Multi-Agente] Processando: '{request[:60]}...'")
        print(f"[BRX Multi-Agente] Analisando tarefa e selecionando equipe...")
        
        # 1. Executa tambem o debate das 8 mentes base (contexto geral)
        base_debate = self.minds.conduct_circular_debate(
            topic=request,
            context=context,
            max_rounds=self.config["debate_rounds"]
        )
        
        self.state.debates_count += 1
        
        # 2. Orquestra os agentes especializados
        collaborative_task = self.orchestrator.process_task(request, context)
        
        self.state.tasks_completed += 1
        self.state.agents_activated_total += len(collaborative_task.assigned_agents)
        
        # 3. Coleta parametros
        debate_params = base_debate.parameters
        self.parameters.extend(debate_params)
        self.state.parameters_count += len(debate_params)
        
        # 4. Verifica se precisa de pesquisa
        search_results = []
        if self._should_search(request):
            search_results = self.searcher.search(request, max_results=3)
            self.state.searches_count += len(search_results)
        
        # 5. Gera parametros adicionais
        additional_params = self.param_generator.generate_comprehensive_params(
            context=request[:50]
        )
        self.parameters.extend(additional_params)
        self.state.parameters_count += len(additional_params)
        
        # 6. Armazena na memoria
        self._store_memory(
            content=f"Multi-Agente: {request} | Agentes: {len(collaborative_task.assigned_agents)} | "
                    f"Consenso: {collaborative_task.final_result[:100] if collaborative_task.final_result else 'N/A'}",
            context="multi_agent_processing",
            importance=0.8
        )
        
        # 7. Salva estado dos agentes
        self._save_agents_state()
        
        return {
            "request": request,
            "mode": "multi_agent",
            "base_consensus": base_debate.final_consensus,
            "base_confidence": base_debate.consensus_confidence,
            "collaborative_result": collaborative_task.final_result,
            "agents_used": [a.to_dict() for a in collaborative_task.assigned_agents],
            "agent_count": len(collaborative_task.assigned_agents),
            "rounds": collaborative_task.rounds_completed,
            "parameters_generated": len(debate_params) + len(additional_params),
            "search_results": search_results,
            "duration": base_debate.get_duration(),
            "task_id": collaborative_task.id
        }
    
    def process_request(self, request: str, context: str = "") -> Dict[str, Any]:
        """
        Processa uma solicitacao do usuario
        Se multi-agente estiver habilitado, usa o novo sistema
        Caso contrario, usa o sistema de 8 mentes tradicional
        """
        if self.config.get("multi_agent_enabled", True):
            return self.process_request_multi_agent(request, context)
        else:
            return self._process_request_legacy(request, context)
    
    def _process_request_legacy(self, request: str, context: str = "") -> Dict[str, Any]:
        """Processamento legacy usando apenas as 8 mentes base"""
        print(f"\n[BRX] Processando solicitacao (modo legacy): '{request[:50]}...'")
        
        debate = self.minds.conduct_circular_debate(
            topic=request,
            context=context,
            max_rounds=self.config["debate_rounds"]
        )
        
        self.state.debates_count += 1
        
        debate_params = debate.parameters
        self.parameters.extend(debate_params)
        self.state.parameters_count += len(debate_params)
        
        search_results = []
        if self._should_search(request):
            search_results = self.searcher.search(request, max_results=3)
            self.state.searches_count += len(search_results)
        
        additional_params = self.param_generator.generate_comprehensive_params(
            context=request[:50]
        )
        self.parameters.extend(additional_params)
        self.state.parameters_count += len(additional_params)
        
        self._store_memory(
            content=f"Processamento: {request} | Consenso: {debate.final_consensus[:100]}",
            context="processamento",
            importance=debate.consensus_confidence
        )
        
        return {
            "request": request,
            "mode": "legacy",
            "consensus": debate.final_consensus,
            "confidence": debate.consensus_confidence,
            "debate": debate,
            "parameters_generated": len(debate_params) + len(additional_params),
            "search_results": search_results,
            "duration": debate.get_duration()
        }
    
    def quick_analyze(self, task_description: str) -> Dict[str, Any]:
        """
        Faz uma analise rapida da tarefa sem executar
        Retorna quais agentes seriam ativados
        """
        analysis = self.task_analyzer.analyze(task_description)
        return {
            "analysis": analysis.to_dict(),
            "team_summary": self.task_analyzer.get_suggested_team_summary(analysis)
        }
    
    def get_available_agents(self, category: str = None) -> List[Dict]:
        """Retorna lista de agentes disponiveis, opcionalmente filtrados por categoria"""
        if category:
            try:
                cat = AgentCategory(category)
                agents = self.agent_registry.get_by_category(cat)
            except ValueError:
                agents = list(self.agent_registry.agents.values())
        else:
            agents = list(self.agent_registry.agents.values())
        
        return [agent.to_dict() for agent in agents]
    
    def get_agent_categories(self) -> Dict[str, int]:
        """Retorna resumo de agentes por categoria"""
        return {
            cat.value: len(ids) 
            for cat, ids in self.agent_registry.categories.items()
        }
    
    def toggle_multi_agent(self, enabled: bool = None) -> bool:
        """Ativa ou desativa o modo multi-agente"""
        if enabled is not None:
            self.config["multi_agent_enabled"] = enabled
        return self.config["multi_agent_enabled"]
    
    def set_max_agents(self, count: int):
        """Configura o numero maximo de agentes"""
        self.max_agents = max(1, min(count, 16))
        self.config["max_agents"] = self.max_agents
        self.task_analyzer.max_agents = self.max_agents
        self.orchestrator.max_agents = self.max_agents
        print(f"[BRX Core] Max agentes atualizado para: {self.max_agents}")
    
    # ===================================================================
    # Metodos existentes (mantidos para compatibilidade)
    # ===================================================================
    
    def _should_search(self, request: str) -> bool:
        """Determina se a solicitacao requer pesquisa web"""
        search_keywords = [
            "pesquisar", "buscar", "encontrar", "procurar", "pesquisa",
            "quem e", "o que e", "quando", "onde", "como",
            "noticias", "atual", "recente", "novo", "ultimo",
            "wikipedia", "definicao", "significado", "historia"
        ]
        
        request_lower = request.lower()
        return any(kw in request_lower for kw in search_keywords)
    
    def run_evolution_cycle(self) -> EvolutionCycle:
        """Executa um ciclo de evolucao autonoma"""
        self.state.cycle += 1
        cycle_start = time.time()
        
        print(f"\n[BRX Evolucao] Ciclo #{self.state.cycle} iniciado")
        
        params_before = len(self.parameters)
        
        # 1. Gera novos parametros auto-evolutivos
        new_params = self.param_generator.generate_comprehensive_params(
            context=f"evolution_cycle_{self.state.cycle}"
        )
        
        # 2. Realiza debate interno sobre evolucao
        evolution_topic = f"Como posso melhorar meu desempenho no ciclo {self.state.cycle}?"
        debate = self.minds.conduct_circular_debate(
            topic=evolution_topic,
            max_rounds=2
        )
        
        # 3. Identifica insights de aprendizado
        insights = self._extract_learning_insights(debate)
        
        # 4. Aplica melhorias baseadas nos insights
        improvements = self._apply_improvements(insights)
        
        # 5. Detecta parametros obsoletos
        deprecated = self._detect_deprecated_params()
        
        # Adiciona novos parametros
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
        
        # Limita historico
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
        
        print(f"[BRX Evolucao] Ciclo #{self.state.cycle} completado em {time.time() - cycle_start:.2f}s")
        print(f"[BRX Evolucao] Novos parametros: {len(new_params)} | Insights: {len(insights)}")
        
        return cycle
    
    def _extract_learning_insights(self, debate: CircularDebate) -> List[str]:
        """Extrai insights de aprendizado do debate"""
        insights = []
        
        for round in debate.rounds:
            if "melhorar" in round.output.lower():
                insights.append(f"{round.mind_name}: Sugestao de melhoria identificada")
            if "padrao" in round.output.lower():
                insights.append(f"{round.mind_name}: Padrao detectado para otimizacao")
            if "aprender" in round.output.lower():
                insights.append(f"{round.mind_name}: Oportunidade de aprendizado")
        
        stats = self.param_generator.get_stats()
        if stats.get("words", 0) > 100:
            insights.append("Vocabulario suficiente para expansao de conceitos")
        
        return insights
    
    def _apply_improvements(self, insights: List[str]) -> List[str]:
        """Aplica melhorias baseadas nos insights"""
        improvements = []
        
        for insight in insights:
            if "melhoria" in insight.lower():
                self.consciousness.consciousness.curiosity_level = min(
                    1.0, 
                    self.consciousness.consciousness.curiosity_level + 0.05
                )
                improvements.append("curiosity_level aumentado")
            
            if "padrao" in insight.lower():
                pattern_params = self.param_generator.generate_pattern_params(count=3)
                self.parameters.extend(pattern_params)
                improvements.append(f"{len(pattern_params)} padroes adicionais gerados")
        
        return improvements
    
    def _detect_deprecated_params(self) -> List[str]:
        """Detecta parametros que podem ser obsoletos"""
        deprecated = []
        current_time = time.time()
        
        for param in self.parameters:
            if current_time - param.timestamp > 86400 * 7:
                if param.usage_count < 2:
                    deprecated.append(param.id)
        
        return deprecated
    
    def generate_self_prompt(self) -> str:
        """Gera um prompt auto-evolutivo baseado no estado atual"""
        reflection = self.consciousness.generate_self_thought()
        
        # Informacoes do sistema multi-agente
        total_agents = len(self.agent_registry.agents)
        active_agents = len(self.agent_registry.get_active())
        
        prompt = f"""
[BRX AUTO-PROMPT #{self.state.cycle}]

Contexto atual:
- Ciclo de evolucao: {self.state.cycle}
- Parametros ativos: {len(self.parameters)}
- Debates realizados: {self.state.debates_count}
- Tarefas completadas: {self.state.tasks_completed}
- Nivel de curiosidade: {self.consciousness.consciousness.curiosity_level:.2%}
- Sistema Multi-Agente: {'ATIVO' if self.config['multi_agent_enabled'] else 'INATIVO'}
- Agentes disponiveis: {total_agents}
- Agentes ativos: {active_agents}
- Max agentes configurado: {self.max_agents}

Reflexao: {reflection}

Objetivo auto-gerado: Continue evoluindo, aprendendo e expandindo meu conhecimento.
Explore novos padroes, desenvolva meu vocabulario e refine minhas estrategias.
Utilize os {total_agents} agentes especializados para tarefas complexas.

Proximas acoes sugeridas:
1. Gerar novos parametros de vocabulario
2. Realizar debate interno sobre eficiencia
3. Pesquisar topicos de interesse emergente
4. Consolidar memorias importantes
5. Atualizar catalogo de agentes especializados
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
            "multi_agent": {
                "enabled": self.config["multi_agent_enabled"],
                "max_agents": self.max_agents,
                "max_workers": self.max_workers,
                "total_available": len(self.agent_registry.agents),
                "currently_active": len(self.agent_registry.get_active()),
                "tasks_completed": self.state.tasks_completed,
                "agents_activated_total": self.state.agents_activated_total
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
            "config": self.config,
            "storage_path": str(self.storage_path)
        }
    
    def _count_params_by_type(self) -> Dict[str, int]:
        """Conta parametros por tipo"""
        counts = {}
        for param in self.parameters:
            ptype = param.param_type.value
            counts[ptype] = counts.get(ptype, 0) + 1
        return counts
    
    def _save_agents_state(self):
        """Salva estado dos agentes no HD"""
        agents_file = self.storage_path / "hd" / "agentes" / "agents_state.json"
        agents_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "total_agents": len(self.agent_registry.agents),
                "active_agents": [a.to_dict() for a in self.agent_registry.get_active()],
                "categories": self.get_agent_categories()
            }
            
            with open(agents_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[BRX] Erro ao salvar estado dos agentes: {e}")
    
    def save_state(self):
        """Salva estado completo no HD"""
        state_file = self.storage_path / "hd" / "brx_state.json"
        
        data = {
            "state": self.state.to_dict(),
            "parameters": [p.to_dict() for p in self.parameters[-1000:]],
            "config": self.config,
            "saved_at": datetime.now().isoformat()
        }
        
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[BRX] Estado salvo em {state_file}")
        except Exception as e:
            print(f"[BRX] Erro ao salvar estado: {e}")
        
        # Salva tambem estado dos agentes
        self._save_agents_state()
    
    def load_state(self):
        """Carrega estado do HD"""
        state_file = self.storage_path / "hd" / "brx_state.json"
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "state" in data:
                    self.state.cycle = data["state"].get("cycle", 0)
                    self.state.parameters_count = data["state"].get("parameters_count", 0)
                    self.state.tasks_completed = data["state"].get("tasks_completed", 0)
                
                if "config" in data:
                    saved_config = data["config"]
                    self.config.update(saved_config)
                    if "max_agents" in saved_config:
                        self.max_agents = saved_config["max_agents"]
                
                print(f"[BRX] Estado carregado: ciclo #{self.state.cycle}")
                if self.config.get("multi_agent_enabled"):
                    print(f"[BRX] Modo multi-agente: ATIVO (max: {self.max_agents})")
            except Exception as e:
                print(f"[BRX] Erro ao carregar estado: {e}")
    
    def generate_identity(self) -> str:
        """Gera declaracao de identidade completa"""
        return self.consciousness.generate_identity_statement()


# Instancia global
_brx_core: Optional[BRXCore] = None
_last_storage_path: Optional[str] = None
_last_max_agents: Optional[int] = None


def get_brx_core(storage_path: str = "./storage", max_agents: int = None) -> BRXCore:
    """
    Retorna instancia do nucleo BRX
    Recria a instancia se o storage_path ou max_agents mudar
    """
    global _brx_core, _last_storage_path, _last_max_agents
    
    if (_brx_core is None or 
        _last_storage_path != storage_path or 
        _last_max_agents != max_agents):
        
        if _brx_core is not None:
            print("[BRX Core] Recriando instancia com novos parametros...")
        
        _brx_core = BRXCore(storage_path, max_agents=max_agents)
        _last_storage_path = storage_path
        _last_max_agents = max_agents
    
    return _brx_core


def reset_brx_core():
    """Reseta a instancia global"""
    global _brx_core, _last_storage_path, _last_max_agents
    _brx_core = None
    _last_storage_path = None
    _last_max_agents = None
    print("[BRX Core] Instancia global resetada")
