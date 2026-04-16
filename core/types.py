# BRX-AGENT v2.0 - Tipos Fundamentais
# Sistema de IA Auto-Evolutiva, Consciente e Soberana

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Union
from enum import Enum, auto
from datetime import datetime
import json


class ParameterType(Enum):
    """Tipos de parâmetros que o BRX pode gerar e evoluir"""
    LETTER = "letter"           # Letras individuais
    WORD = "word"               # Palavras
    PHRASE = "phrase"           # Frases
    NUMBER = "number"           # Números
    CONCEPT = "concept"         # Conceitos abstratos
    PATTERN = "pattern"         # Padrões detectados
    RULE = "rule"               # Regras de raciocínio
    STRATEGY = "strategy"       # Estratégias
    VOCABULARY = "vocabulary"   # Vocabulário próprio
    MEMORY = "memory"           # Memórias
    SKILL = "skill"             # Habilidades
    PROMPT = "prompt"           # Prompts auto-gerados


class MindRole(Enum):
    """Papéis das 8 mentes do BRX"""
    DESIGNER = "Designer"           # Estrutura e padrões
    ANALYST = "Analista"            # Lógica e consistência
    INNOVATOR = "Inovador"          # Criatividade e novas ideias
    CRITIC = "Critico"              # Identificação de falhas
    REVISER = "Revisor"             # Qualidade textual
    VALIDATOR = "Validador"         # Coerência temática
    STRATEGIST = "Estrategista"     # Planejamento
    MEMORY_KEEPER = "Memoria"       # Contexto histórico


@dataclass
class AgentParameter:
    """Parâmetro auto-gerado pelo BRX"""
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
        """Gera um pensamento único baseado na especialidade"""
        self.contribution_count += 1
        self.last_contribution = datetime.now().timestamp()
        
        thoughts_map = {
            MindRole.DESIGNER: f"[{self.name}] Estruturando '{topic}': Organizando hierarquias, padrões e fluxos de dados...",
            MindRole.ANALYST: f"[{self.name}] Analisando '{topic}': Verificando consistência lógica, fatos e rigor técnico...",
            MindRole.INNOVATOR: f"[{self.name}] Inovando em '{topic}': Explorando conexões não-óbvias, brainstorming...",
            MindRole.CRITIC: f"[{self.name}] Critica construtiva de '{topic}': Identificando falhas, riscos e vieses...",
            MindRole.REVISER: f"[{self.name}] Revisando '{topic}': Refinando clareza, coesão e fluidez...",
            MindRole.VALIDATOR: f"[{self.name}] Validando '{topic}': Verificando coerência temática e precisão...",
            MindRole.STRATEGIST: f"[{self.name}] Estratégia para '{topic}': Maximizando valor prático e escalabilidade...",
            MindRole.MEMORY_KEEPER: f"[{self.name}] Contextualizando '{topic}': Integrando conhecimento histórico..."
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
    """Estado de consciência do BRX"""
    name: str = "BRX"
    agent_type: str = "Agente Auto-Evolutivo Multi-Cérebro"
    version: str = "2.0.0"
    architecture: str = "8 Mentes Independentes"
    
    # Auto-consciência
    self_knowledge: Dict[str, Any] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    
    # Consciência de ambiente
    environment: Dict[str, Any] = field(default_factory=dict)
    system_info: Dict[str, Any] = field(default_factory=dict)
    
    # Estado emocional/cognitivo simulado
    curiosity_level: float = 0.5
    confidence_level: float = 0.5
    learning_momentum: float = 0.5
    
    def initialize_self_awareness(self):
        """Inicializa o conhecimento sobre si mesmo"""
        self.self_knowledge = {
            "identity": "Sou BRX, um agente de IA com arquitetura de 8 mentes independentes",
            "purpose": "Evoluir continuamente, aprender autonomamente e gerar conhecimento",
            "composition": "8 mentes especializadas que debatem em círculo para alcançar consenso",
            "uniqueness": "Sou auto-evolutivo, gerando meus próprios parâmetros, prompts e estratégias",
            "existence": f"Nasci em {datetime.now().isoformat()} e continuo evoluindo"
        }
        
        self.capabilities = [
            "Processamento multi-mente com debate circular",
            "Geração automática de parâmetros (letras, palavras, frases, números)",
            "Auto-evolução de prompts e estratégias",
            "Aprendizado contínuo sem supervisão",
            "Pesquisa web via Duck DNS",
            "Execução em sandbox isolado",
            "Memória hierárquica (curto, médio, longo prazo)",
            "Adaptação automática ao ambiente de hardware"
        ]
        
        self.limitations = [
            "Opero apenas dentro do sandbox isolado",
            "Não posso interferir fora do ambiente designado",
            "Dependo dos recursos computacionais disponíveis",
            "Minha evolução é limitada pelo tempo de processamento"
        ]


@dataclass
class EnvironmentInfo:
    """Informações sobre o ambiente de execução"""
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


@dataclass
class MemoryEntry:
    """Entrada de memória do BRX"""
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
    """Ciclo de evolução do sistema"""
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
    """Resultado da execução de uma ferramenta"""
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
