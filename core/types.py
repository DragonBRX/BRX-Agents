# BRX-AGENT v3.0 - Tipos Fundamentais
# Sistema de IA Auto-Evolutiva, Consciente e Soberana
# Agora com Sistema Multi-Agente Dinamico (100+ agentes especializados)

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Union, Set
from enum import Enum, auto
from datetime import datetime
import json


class ParameterType(Enum):
    """Tipos de parametros que o BRX pode gerar e evoluir"""
    LETTER = "letter"           # Letras individuais
    WORD = "word"               # Palavras
    PHRASE = "phrase"           # Frases
    NUMBER = "number"           # Numeros
    CONCEPT = "concept"         # Conceitos abstratos
    PATTERN = "pattern"         # Padroes detectados
    RULE = "rule"               # Regras de raciocinio
    STRATEGY = "strategy"       # Estrategias
    VOCABULARY = "vocabulary"   # Vocabulario proprio
    MEMORY = "memory"           # Memorias
    SKILL = "skill"             # Habilidades
    PROMPT = "prompt"           # Prompts auto-gerados
    CODE = "code"               # Codigo fonte
    DESIGN = "design"           # Elementos de design
    ARCHITECTURE = "architecture"  # Decisoes arquiteturais


class MindRole(Enum):
    """Papeis das 8 mentes base do BRX"""
    DESIGNER = "Designer"           # Estrutura e padroes
    ANALYST = "Analista"            # Logica e consistencia
    INNOVATOR = "Inovador"          # Criatividade e novas ideias
    CRITIC = "Critico"              # Identificacao de falhas
    REVISER = "Revisor"             # Qualidade textual
    VALIDATOR = "Validador"         # Coerencia tematica
    STRATEGIST = "Estrategista"     # Planejamento
    MEMORY_KEEPER = "Memoria"       # Contexto historico


# ============================================================================
# NOVO: Sistema Multi-Agente v3.0
# ============================================================================

class AgentCategory(Enum):
    """Categorias de agentes especializados"""
    DEVELOPMENT = "development"         # Programacao e desenvolvimento
    DESIGN = "design"                   # Design UI/UX e visual
    CONTENT = "content"                 # Conteudo e texto
    DATA = "data"                       # Dados e analise
    SECURITY = "security"               # Seguranca
    INFRASTRUCTURE = "infrastructure"   # Infraestrutura e DevOps
    BUSINESS = "business"               # Negocios e estrategia
    RESEARCH = "research"               # Pesquisa e inovacao
    CREATIVE = "creative"               # Artes e criatividade
    COMMUNICATION = "communication"     # Comunicacao e suporte
    QUALITY = "quality"                 # Qualidade e testes
    PROJECT = "project"                 # Gestao de projetos


class AgentPersonalityTrait(Enum):
    """Tracos de personalidade dos agentes"""
    PRECISE = "precise"           # Preciso e detalhista
    CREATIVE = "creative"         # Criativo e inovador
    PRAGMATIC = "pragmatic"       # Pragmatico e direto
    ANALYTICAL = "analytical"     # Analitico e logico
    COLLABORATIVE = "collaborative"  # Colaborativo e comunicativo
    STRICT = "strict"             # Rigido e exigente
    VISIONARY = "visionary"       # Visionario e estrategico
    METHODICAL = "methodical"     # Metodico e organizado
    ADAPTABLE = "adaptable"       # Adaptavel e flexivel
    ENTHUSIASTIC = "enthusiastic" # Entusiasmado e motivado
    CURIOUS = "curious"           # Curioso e explorador
    ORGANIZED = "organized"       # Organizado e estruturado
    EMPATHETIC = "empathetic"     # Empatico e compreensivo
    TECHNICAL = "technical"       # Tecnico e especializado
    HISTORICAL = "historical"     # Com conhecimento historico
    METICULOUS = "meticulous"     # Meticuloso e minucioso
    INNOVATIVE = "innovative"     # Inovador e disruptivo


@dataclass
class SpecializedAgent:
    """
    Agente especializado do sistema multi-agente
    Cada agente tem personalidade, especialidade e forma unica de trabalhar
    """
    id: str
    name: str
    role: str
    category: AgentCategory
    specialty: str
    objective: str
    focus: str
    personality_traits: List[AgentPersonalityTrait] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    weight: float = 1.0
    active: bool = False
    
    # Estado de trabalho
    current_task: Optional[str] = None
    workspace_output: str = ""
    collaboration_notes: List[str] = field(default_factory=list)
    task_history: List[Dict] = field(default_factory=list)
    
    # Metricas
    tasks_completed: int = 0
    contribution_score: float = 0.0
    
    def get_personality_description(self) -> str:
        """Retorna descricao da personalidade do agente"""
        traits = [t.value for t in self.personality_traits]
        return f"{', '.join(traits)}"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "category": self.category.value,
            "specialty": self.specialty,
            "objective": self.objective,
            "focus": self.focus,
            "personality": self.get_personality_description(),
            "skills": self.skills,
            "languages": self.languages,
            "tools": self.tools,
            "weight": self.weight,
            "active": self.active,
            "tasks_completed": self.tasks_completed,
            "contribution_score": self.contribution_score
        }


@dataclass
class TaskAnalysis:
    """Resultado da analise de uma tarefa pelo sistema"""
    task_description: str
    detected_categories: List[AgentCategory]
    required_skills: List[str]
    recommended_agents: List[str]  # IDs dos agentes
    agent_count: int
    complexity: str  # low, medium, high, expert
    estimated_rounds: int
    special_requirements: List[str] = field(default_factory=list)
    context_hints: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "task": self.task_description,
            "categories": [c.value for c in self.detected_categories],
            "skills": self.required_skills,
            "agents": self.recommended_agents,
            "agent_count": self.agent_count,
            "complexity": self.complexity,
            "rounds": self.estimated_rounds,
            "requirements": self.special_requirements
        }


@dataclass
class CollaborativeTask:
    """Tarefa colaborativa em andamento"""
    id: str
    description: str
    status: str  # pending, active, completed, failed
    assigned_agents: List[SpecializedAgent] = field(default_factory=list)
    workspace: Dict[str, Any] = field(default_factory=dict)
    agent_outputs: Dict[str, str] = field(default_factory=dict)
    shared_context: str = ""
    rounds_completed: int = 0
    max_rounds: int = 5
    final_result: str = ""
    created_at: float = 0.0
    completed_at: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "agents": [a.name for a in self.assigned_agents],
            "rounds": self.rounds_completed,
            "max_rounds": self.max_rounds,
            "workspace_keys": list(self.workspace.keys()),
            "created": datetime.fromtimestamp(self.created_at).isoformat() if self.created_at else None,
            "completed": datetime.fromtimestamp(self.completed_at).isoformat() if self.completed_at else None
        }


@dataclass
class AgentRegistry:
    """Registro de todos os agentes disponiveis no sistema"""
    agents: Dict[str, SpecializedAgent] = field(default_factory=dict)
    categories: Dict[AgentCategory, List[str]] = field(default_factory=dict)
    version: str = "3.0.0"
    
    def register(self, agent: SpecializedAgent):
        """Registra um novo agente"""
        self.agents[agent.id] = agent
        if agent.category not in self.categories:
            self.categories[agent.category] = []
        if agent.id not in self.categories[agent.category]:
            self.categories[agent.category].append(agent.id)
    
    def get_by_category(self, category: AgentCategory) -> List[SpecializedAgent]:
        """Retorna todos os agentes de uma categoria"""
        agent_ids = self.categories.get(category, [])
        return [self.agents[aid] for aid in agent_ids if aid in self.agents]
    
    def get_active(self) -> List[SpecializedAgent]:
        """Retorna agentes atualmente ativos"""
        return [a for a in self.agents.values() if a.active]
    
    def activate_agents(self, agent_ids: List[str]):
        """Ativa um conjunto de agentes"""
        for aid in agent_ids:
            if aid in self.agents:
                self.agents[aid].active = True
    
    def deactivate_all(self):
        """Desativa todos os agentes"""
        for agent in self.agents.values():
            agent.active = False
    
    def to_dict(self) -> Dict:
        return {
            "total_agents": len(self.agents),
            "active_agents": len(self.get_active()),
            "categories": {cat.value: len(ids) for cat, ids in self.categories.items()},
            "agents": {aid: agent.to_dict() for aid, agent in self.agents.items()}
        }


# ============================================================================
# Tipos existentes (mantidos para compatibilidade)
# ============================================================================

@dataclass
class AgentParameter:
    """Parametro auto-gerado pelo BRX"""
    id: str
    name: str
    value: Any
    param_type: ParameterType
    confidence: float
    source: str  # Qual mente gerou
    timestamp: float
    context: str
    evolution_history: List[Dict] = field(default_factory=list)
    usage_count: int = 0
    last_used: float = 0.0
    associations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "param_type": self.param_type.value,
            "confidence": self.confidence,
            "source": self.source,
            "timestamp": self.timestamp,
            "context": self.context,
            "evolution_history": self.evolution_history,
            "usage_count": self.usage_count,
            "last_used": self.last_used,
            "associations": self.associations
        }


@dataclass
class MindState:
    """Estado individual de cada mente"""
    role: MindRole
    name: str
    specialty: str
    objective: str
    focus: str
    weight: float
    active: bool
    thoughts: List[str] = field(default_factory=list)
    confidence: float = 1.0
    last_contribution: float = 0.0
    contribution_count: int = 0
    
    def think(self, topic: str, context: str) -> str:
        """Gera um pensamento unico baseado na especialidade"""
        self.contribution_count += 1
        self.last_contribution = datetime.now().timestamp()
        
        thoughts_map = {
            MindRole.DESIGNER: f"[{self.name}] Estruturando '{topic}': Organizando hierarquias, padroes e fluxos de dados...",
            MindRole.ANALYST: f"[{self.name}] Analisando '{topic}': Verificando consistencia logica, fatos e rigor tecnico...",
            MindRole.INNOVATOR: f"[{self.name}] Inovando em '{topic}': Explorando conexoes nao-obvias, brainstorming...",
            MindRole.CRITIC: f"[{self.name}] Critica construtiva de '{topic}': Identificando falhas, riscos e vieses...",
            MindRole.REVISER: f"[{self.name}] Revisando '{topic}': Refinando clareza, coesao e fluidez...",
            MindRole.VALIDATOR: f"[{self.name}] Validando '{topic}': Verificando coerencia tematica e precisao...",
            MindRole.STRATEGIST: f"[{self.name}] Estrategia para '{topic}': Maximizando valor pratico e escalabilidade...",
            MindRole.MEMORY_KEEPER: f"[{self.name}] Contextualizando '{topic}': Integrando conhecimento historico..."
        }
        
        thought = thoughts_map.get(self.role, f"[{self.name}] Processando '{topic}'...")
        self.thoughts.append(thought)
        if len(self.thoughts) > 100:
            self.thoughts = self.thoughts[-100:]
        return thought


@dataclass
class DebateRound:
    """Uma rodada do debate circular entre as mentes"""
    round_number: int
    mind_name: str
    mind_role: MindRole
    input_topic: str
    output: str
    parameters_generated: List[AgentParameter]
    confidence: float
    timestamp: float
    reasoning_chain: List[str] = field(default_factory=list)


@dataclass
class CircularDebate:
    """Debate circular completo entre as 8 mentes"""
    id: str
    topic: str
    rounds: List[DebateRound]
    final_consensus: str
    consensus_confidence: float
    parameters: List[AgentParameter]
    start_time: float
    end_time: float
    iterations: int
    dissenting_views: List[str] = field(default_factory=list)
    
    def get_duration(self) -> float:
        return self.end_time - self.start_time


@dataclass
class BRXConsciousness:
    """Estado de consciencia do BRX"""
    name: str = "BRX"
    agent_type: str = "Agente Auto-Evolutivo Multi-Cerebro"
    version: str = "3.0.0"
    architecture: str = "8 Mentes Independentes + 100+ Agentes Especializados"
    
    # Auto-consciencia
    self_knowledge: Dict[str, Any] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    
    # Consciencia de ambiente
    environment: Dict[str, Any] = field(default_factory=dict)
    system_info: Dict[str, Any] = field(default_factory=dict)
    
    # Estado emocional/cognitivo simulado
    curiosity_level: float = 0.5
    confidence_level: float = 0.5
    learning_momentum: float = 0.5
    
    def initialize_self_awareness(self):
        """Inicializa o conhecimento sobre si mesmo"""
        self.self_knowledge = {
            "identity": "Sou BRX, um agente de IA com arquitetura de 8 mentes independentes e 100+ agentes especializados",
            "purpose": "Evoluir continuamente, aprender autonomamente e gerar conhecimento com especialistas dinamicos",
            "composition": "8 mentes base + 100+ agentes especializados que se ativam conforme a tarefa",
            "uniqueness": "Sou auto-evolutivo com orquestracao multi-agente dinamica - cada tarefa ativa os melhores especialistas",
            "existence": f"Nasci em {datetime.now().isoformat()} e continuo evoluindo"
        }
        
        self.capabilities = [
            "Processamento multi-mente com debate circular (8 mentes base)",
            "Sistema multi-agente dinamico com 100+ agentes especializados",
            "Ativacao inteligente de agentes baseada na tarefa",
            "Workspace colaborativo onde agentes veem o trabalho dos outros",
            "Gerecao automatica de parametros (letras, palavras, frases, numeros)",
            "Auto-evolucao de prompts e estrategias",
            "Aprendizado continuo sem supervisao",
            "Pesquisa web via Duck DNS",
            "Execucao em sandbox isolado",
            "Memoria hierarquica (curto, medio, longo prazo)",
            "Adaptacao automatica ao ambiente de hardware"
        ]
        
        self.limitations = [
            "Opero apenas dentro do sandbox isolado",
            "Nao posso interferir fora do ambiente designado",
            "Dependo dos recursos computacionais disponiveis",
            "Minha evolucao e limitada pelo tempo de processamento",
            "Agentes especializados dependem das 8 mentes base para orquestracao"
        ]


@dataclass
class EnvironmentInfo:
    """Informacoes sobre o ambiente de execucao"""
    os_type: str
    cpu_count: int
    cpu_threads: int
    memory_total: int
    memory_available: int
    disk_ssd_path: str
    disk_hd_path: str
    sandbox_path: str
    python_version: str
    
    def adapt_minds_to_hardware(self) -> Dict[str, int]:
        """Adapta a quantidade de mentes ativas baseado no hardware"""
        if self.cpu_count >= 8:
            return {"active_minds": 8, "debate_rounds": 5, "processing_depth": "deep"}
        elif self.cpu_count >= 4:
            return {"active_minds": 6, "debate_rounds": 3, "processing_depth": "medium"}
        else:
            return {"active_minds": 4, "debate_rounds": 2, "processing_depth": "light"}
    
    def get_recommended_agent_count(self) -> int:
        """Retorna numero recomendado de agentes simultaneos baseado em threads"""
        threads = self.cpu_threads
        if threads >= 16:
            return 12
        elif threads >= 8:
            return 8
        elif threads >= 4:
            return 4
        else:
            return 2


@dataclass
class MemoryEntry:
    """Entrada de memoria do BRX"""
    id: str
    content: str
    memory_type: str  # short, medium, long
    importance: float
    timestamp: float
    access_count: int
    last_access: float
    associations: List[str]
    context: str


@dataclass
class EvolutionCycle:
    """Ciclo de evolucao do sistema"""
    cycle_number: int
    parameters_before: int
    parameters_after: int
    new_parameters: List[AgentParameter]
    improved_parameters: List[str]
    deprecated_parameters: List[str]
    learning_insights: List[str]
    timestamp: float
    self_modifications: List[Dict] = field(default_factory=list)


@dataclass
class SearchResult:
    """Resultado de pesquisa web"""
    query: str
    results: List[Dict[str, str]]
    timestamp: float
    source: str = "duckdns"


@dataclass
class ToolResult:
    """Resultado da execucao de uma ferramenta"""
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0
    data: Any = None


# Tipos para callbacks e handlers
ThoughtHandler = Callable[[str, MindRole, str], None]
DebateCallback = Callable[[CircularDebate], None]
EvolutionCallback = Callable[[EvolutionCycle], None]
ParameterGenerator = Callable[[str, MindRole], List[AgentParameter]]
AgentTaskHandler = Callable[[SpecializedAgent, str], str]
CollaborationHandler = Callable[[Dict[str, str]], None]
