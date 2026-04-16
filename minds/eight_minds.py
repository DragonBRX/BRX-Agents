# BRX-AGENT v2.0 - Sistema de 8 Mentes
# Arquitetura de múltiplos cérebros funcionando como 8 funcionários
# Cada mente tem raciocínio independente mas comunicam em roda de conversas

import random
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field

from core.types import (
    MindRole, MindState, DebateRound, CircularDebate,
    AgentParameter, ParameterType, ThoughtHandler
)


class Mind:
    """
    Representa uma mente individual do BRX
    Cada mente tem sua própria personalidade, especialidade e forma de raciocinar
    """
    
    def __init__(self, state: MindState):
        self.state = state
        self.thought_history: List[str] = []
        self.parameters_generated: List[AgentParameter] = []
        self.reasoning_chain: List[str] = []
    
    def think(self, topic: str, context: str, previous_thoughts: List[str] = None) -> str:
        """
        Realiza o processamento único desta mente
        Considera pensamentos anteriores das outras mentes (roda de conversas)
        """
        # Gera pensamento base
        thought = self.state.think(topic, context)
        
        # Se há pensamentos anteriores, reage a eles
        if previous_thoughts:
            reaction = self._react_to_others(previous_thoughts, topic)
            thought = f"{thought}\n   Reação: {reaction}"
        
        self.thought_history.append(thought)
        self.reasoning_chain.append(f"{self.state.name}: {thought}")
        
        return thought
    
    def _react_to_others(self, others_thoughts: List[str], topic: str) -> str:
        """Reage aos pensamentos das outras mentes"""
        reactions = {
            MindRole.DESIGNER: f"Considerando a estrutura proposta, vou organizar os dados de forma mais eficiente.",
            MindRole.ANALYST: f"Analisando os pontos levantados para verificar consistência lógica.",
            MindRole.INNOVATOR: f"Inspirado pelas ideias anteriores, vejo uma conexão inovadora!",
            MindRole.CRITIC: f"Vejo pontos válidos, mas preciso identificar possíveis falhas.",
            MindRole.REVISER: f"Vou refinar a comunicação para maior clareza baseado no contexto.",
            MindRole.VALIDATOR: f"Validando a coerência do que foi discutido até agora.",
            MindRole.STRATEGIST: f"Estruturando uma estratégia coerente com todas as contribuições.",
            MindRole.MEMORY_KEEPER: f"Integrando este conhecimento com experiências anteriores."
        }
        
        return reactions.get(self.state.role, "Processando contribuições das outras mentes...")
    
    def generate_parameters(self, topic: str, context: str) -> List[AgentParameter]:
        """Gera parâmetros específicos do domínio desta mente"""
        params = []
        timestamp = datetime.now().timestamp()
        
        # Cada mente gera parâmetros diferentes baseados em sua especialidade
        param_generators = {
            MindRole.DESIGNER: self._generate_designer_params,
            MindRole.ANALYST: self._generate_analyst_params,
            MindRole.INNOVATOR: self._generate_innovator_params,
            MindRole.CRITIC: self._generate_critic_params,
            MindRole.REVISER: self._generate_reviser_params,
            MindRole.VALIDATOR: self._generate_validator_params,
            MindRole.STRATEGIST: self._generate_strategist_params,
            MindRole.MEMORY_KEEPER: self._generate_memory_params
        }
        
        generator = param_generators.get(self.state.role)
        if generator:
            params = generator(topic, context, timestamp)
        
        self.parameters_generated.extend(params)
        return params
    
    def _generate_designer_params(self, topic: str, context: str, timestamp: float) -> List[AgentParameter]:
        """Designer: Gera parâmetros de estrutura e padrões"""
        return [
            AgentParameter(
                id=f"design_struct_{uuid.uuid4().hex[:8]}",
                name=f"structure_quality_{topic[:10].replace(' ', '_')}",
                value=random.uniform(0.7, 0.95),
                param_type=ParameterType.PATTERN,
                confidence=random.uniform(0.8, 0.95),
                source=self.state.name,
                timestamp=timestamp,
                context=f"Estrutura para: {topic}"
            ),
            AgentParameter(
                id=f"design_hier_{uuid.uuid4().hex[:8]}",
                name=f"hierarchy_level_{topic[:10].replace(' ', '_')}",
                value=random.randint(1, 5),
                param_type=ParameterType.CONCEPT,
                confidence=0.85,
                source=self.state.name,
                timestamp=timestamp,
                context=f"Hierarquia de dados"
            )
        ]
    
    def _generate_analyst_params(self, topic: str, context: str, timestamp: float) -> List[AgentParameter]:
        """Analista: Gera parâmetros de lógica e consistência"""
        return [
            AgentParameter(
                id=f"anal_logic_{uuid.uuid4().hex[:8]}",
                name=f"logical_consistency_{topic[:10].replace(' ', '_')}",
                value=random.uniform(0.75, 0.98),
                param_type=ParameterType.RULE,
                confidence=random.uniform(0.85, 0.98),
                source=self.state.name,
                timestamp=timestamp,
                context=f"Análise lógica de: {topic}"
            ),
            AgentParameter(
                id=f"anal_fact_{uuid.uuid4().hex[:8]}",
                name=f"factual_accuracy",
                value=random.uniform(0.8, 1.0),
                param_type=ParameterType.CONCEPT,
                confidence=0.9,
                source=self.state.name,
                timestamp=timestamp,
                context=f"Precisão factual"
            )
        ]
    
    def _generate_innovator_params(self, topic: str, context: str, timestamp: float) -> List[AgentParameter]:
        """Inovador: Gera parâmetros criativos"""
        return [
            AgentParameter(
                id=f"inov_creat_{uuid.uuid4().hex[:8]}",
                name=f"creativity_score_{topic[:10].replace(' ', '_')}",
                value=random.uniform(0.6, 0.95),
                param_type=ParameterType.CONCEPT,
                confidence=random.uniform(0.7, 0.9),
                source=self.state.name,
                timestamp=timestamp,
                context=f"Inovação para: {topic}"
            ),
            AgentParameter(
                id=f"inov_novel_{uuid.uuid4().hex[:8]}",
                name=f"novelty_factor",
                value=random.uniform(0.5, 0.9),
                param_type=ParameterType.PATTERN,
                confidence=0.75,
                source=self.state.name,
                timestamp=timestamp,
                context=f"Fator de novidade"
            )
        ]
    
    def _generate_critic_params(self, topic: str, context: str, timestamp: float) -> List[AgentParameter]:
        """Crítico: Gera parâmetros de identificação de riscos"""
        return [
            AgentParameter(
                id=f"crit_risk_{uuid.uuid4().hex[:8]}",
                name=f"risk_level_{topic[:10].replace(' ', '_')}",
                value=random.uniform(0.0, 0.4),
                param_type=ParameterType.RULE,
                confidence=random.uniform(0.75, 0.9),
                source=self.state.name,
                timestamp=timestamp,
                context=f"Análise de risco para: {topic}"
            ),
            AgentParameter(
                id=f"crit_bias_{uuid.uuid4().hex[:8]}",
                name=f"bias_detection",
                value=random.uniform(0.0, 0.3),
                param_type=ParameterType.PATTERN,
                confidence=0.8,
                source=self.state.name,
                timestamp=timestamp,
                context=f"Detecção de vieses"
            )
        ]
    
    def _generate_reviser_params(self, topic: str, context: str, timestamp: float) -> List[AgentParameter]:
        """Revisor: Gera parâmetros de qualidade textual"""
        return [
            AgentParameter(
                id=f"rev_clarity_{uuid.uuid4().hex[:8]}",
                name=f"clarity_score_{topic[:10].replace(' ', '_')}",
                value=random.uniform(0.75, 0.95),
                param_type=ParameterType.WORD,
                confidence=random.uniform(0.8, 0.92),
                source=self.state.name,
                timestamp=timestamp,
                context=f"Clareza para: {topic}"
            ),
            AgentParameter(
                id=f"rev_cohesion_{uuid.uuid4().hex[:8]}",
                name=f"textual_cohesion",
                value=random.uniform(0.7, 0.95),
                param_type=ParameterType.PHRASE,
                confidence=0.85,
                source=self.state.name,
                timestamp=timestamp,
                context=f"Coesão textual"
            )
        ]
    
    def _generate_validator_params(self, topic: str, context: str, timestamp: float) -> List[AgentParameter]:
        """Validador: Gera parâmetros de validação"""
        return [
            AgentParameter(
                id=f"val_acc_{uuid.uuid4().hex[:8]}",
                name=f"accuracy_score_{topic[:10].replace(' ', '_')}",
                value=random.uniform(0.8, 0.98),
                param_type=ParameterType.CONCEPT,
                confidence=random.uniform(0.85, 0.98),
                source=self.state.name,
                timestamp=timestamp,
                context=f"Validação de: {topic}"
            ),
            AgentParameter(
                id=f"val_align_{uuid.uuid4().hex[:8]}",
                name=f"thematic_alignment",
                value=random.uniform(0.75, 0.95),
                param_type=ParameterType.PATTERN,
                confidence=0.88,
                source=self.state.name,
                timestamp=timestamp,
                context=f"Alinhamento temático"
            )
        ]
    
    def _generate_strategist_params(self, topic: str, context: str, timestamp: float) -> List[AgentParameter]:
        """Estrategista: Gera parâmetros estratégicos"""
        return [
            AgentParameter(
                id=f"est_strat_{uuid.uuid4().hex[:8]}",
                name=f"strategic_value_{topic[:10].replace(' ', '_')}",
                value=random.uniform(0.7, 0.95),
                param_type=ParameterType.STRATEGY,
                confidence=random.uniform(0.8, 0.93),
                source=self.state.name,
                timestamp=timestamp,
                context=f"Valor estratégico de: {topic}"
            ),
            AgentParameter(
                id=f"est_scal_{uuid.uuid4().hex[:8]}",
                name=f"scalability_factor",
                value=random.uniform(0.6, 0.9),
                param_type=ParameterType.CONCEPT,
                confidence=0.82,
                source=self.state.name,
                timestamp=timestamp,
                context=f"Fator de escalabilidade"
            )
        ]
    
    def _generate_memory_params(self, topic: str, context: str, timestamp: float) -> List[AgentParameter]:
        """Memória: Gera parâmetros de contexto histórico"""
        return [
            AgentParameter(
                id=f"mem_context_{uuid.uuid4().hex[:8]}",
                name=f"context_preservation_{topic[:10].replace(' ', '_')}",
                value=random.uniform(0.8, 0.98),
                param_type=ParameterType.MEMORY,
                confidence=random.uniform(0.85, 0.95),
                source=self.state.name,
                timestamp=timestamp,
                context=f"Preservação de contexto para: {topic}"
            ),
            AgentParameter(
                id=f"mem_ref_{uuid.uuid4().hex[:8]}",
                name=f"cross_reference_value",
                value=random.uniform(0.7, 0.95),
                param_type=ParameterType.MEMORY,
                confidence=0.8,
                source=self.state.name,
                timestamp=timestamp,
                context=f"Valor de referência cruzada"
            )
        ]


class EightMindsSystem:
    """
    Sistema de 8 Mentes do BRX
    Funciona como uma empresa com 8 funcionários especializados
    Cada um tem raciocínio independente mas se comunicam em roda de conversas
    """
    
    def __init__(self, active_minds: int = 8):
        self.minds: Dict[MindRole, Mind] = {}
        self.debate_history: List[CircularDebate] = []
        self.thought_handlers: List[ThoughtHandler] = []
        self.active_minds = active_minds
        
        self._initialize_minds()
    
    def _initialize_minds(self):
        """Inicializa as 8 mentes com suas configurações"""
        mind_configs = [
            MindState(
                role=MindRole.DESIGNER,
                name="Designer",
                specialty="Estrutura e Padrões de Dados",
                objective="Garantir que os parâmetros sigam uma arquitetura lógica e escalável",
                focus="Estrutura JSON, esquemas de dados, organização hierárquica",
                weight=1.0,
                active=True
            ),
            MindState(
                role=MindRole.ANALYST,
                name="Analista",
                specialty="Lógica e Consistência Técnica",
                objective="Validar a precisão técnica e a fundamentação lógica das informações",
                focus="Cálculos, fatos científicos, rigor lógico, consistência interna",
                weight=1.0,
                active=True
            ),
            MindState(
                role=MindRole.INNOVATOR,
                name="Inovador",
                specialty="Abordagens Criativas e Novas Perspectivas",
                objective="Expandir o conhecimento para além do óbvio, sugerindo novas conexões",
                focus="Brainstorming, associações não óbvias, originalidade, tendências futuras",
                weight=1.0,
                active=True
            ),
            MindState(
                role=MindRole.CRITIC,
                name="Critico",
                specialty="Identificação de Falhas e Riscos (Red Teaming)",
                objective="Atuar como o advogado do diabo, encontrando erros e pontos fracos",
                focus="Contradições, vieses, erros de segurança, exceções não tratadas",
                weight=1.0,
                active=True
            ),
            MindState(
                role=MindRole.REVISER,
                name="Revisor",
                specialty="Qualidade Textual e Clareza de Comunicação",
                objective="Refinar a linguagem para que seja clara, profissional e sem ambiguidades",
                focus="Gramática, tom de voz, coesão, fluidez textual, terminologia",
                weight=1.0,
                active=True
            ),
            MindState(
                role=MindRole.VALIDATOR,
                name="Validador",
                specialty="Coerência Temática e Precisão de Dados",
                objective="Garantir que o conteúdo esteja alinhado com o tópico central e objetivos",
                focus="Relevância, veracidade, alinhamento com a meta, utilidade prática",
                weight=1.0,
                active=True
            ),
            MindState(
                role=MindRole.STRATEGIST,
                name="Estrategista",
                specialty="Planejamento e Utilidade dos Parâmetros",
                objective="Garantir que o parâmetro gerado tenha valor estratégico para o modelo",
                focus="Aplicação prática, escalabilidade, impacto no treinamento, visão macro",
                weight=1.0,
                active=True
            ),
            MindState(
                role=MindRole.MEMORY_KEEPER,
                name="Memoria",
                specialty="Contexto Histórico e Persistência de Dados",
                objective="Manter a continuidade do conhecimento entre os ciclos de debate",
                focus="Histórico de parâmetros, referências cruzadas, armazenamento, recuperação",
                weight=1.0,
                active=True
            )
        ]
        
        # Cria apenas o número de mentes ativas (adaptativo ao hardware)
        for i, config in enumerate(mind_configs[:self.active_minds]):
            self.minds[config.role] = Mind(config)
    
    def conduct_circular_debate(
        self, 
        topic: str, 
        context: str = "", 
        max_rounds: int = 3,
        consensus_threshold: float = 0.75
    ) -> CircularDebate:
        """
        Conduz um debate circular entre as mentes
        Cada mente contribui, reage às contribuições anteriores, formando uma roda de conversas
        """
        debate_id = f"debate_{datetime.now().timestamp()}"
        start_time = datetime.now().timestamp()
        rounds: List[DebateRound] = []
        all_parameters: List[AgentParameter] = []
        
        # Histórico de pensamentos para a roda de conversas
        conversation_history: List[str] = []
        
        for round_num in range(max_rounds):
            round_parameters: List[AgentParameter] = []
            
            # Cada mente contribui na rodada
            for role, mind in self.minds.items():
                if not mind.state.active:
                    continue
                
                # A mente pensa, considerando o histórico da conversa
                thought = mind.think(topic, context, conversation_history)
                conversation_history.append(thought)
                
                # Notifica handlers de pensamento
                for handler in self.thought_handlers:
                    handler(thought, role, topic)
                
                # Gera parâmetros específicos desta mente
                params = mind.generate_parameters(topic, context)
                round_parameters.extend(params)
                all_parameters.extend(params)
                
                # Cria registro da rodada
                debate_round = DebateRound(
                    round_number=round_num,
                    mind_name=mind.state.name,
                    mind_role=role,
                    input_topic=topic,
                    output=thought,
                    parameters_generated=params,
                    confidence=mind.state.confidence,
                    timestamp=datetime.now().timestamp(),
                    reasoning_chain=mind.reasoning_chain.copy()
                )
                rounds.append(debate_round)
            
            # Verifica se atingiu consenso
            consensus = self._calculate_consensus(round_parameters)
            if consensus >= consensus_threshold:
                break
        
        end_time = datetime.now().timestamp()
        
        # Gera consenso final
        final_consensus = self._generate_final_consensus(topic, rounds, all_parameters)
        
        debate = CircularDebate(
            id=debate_id,
            topic=topic,
            rounds=rounds,
            final_consensus=final_consensus["text"],
            consensus_confidence=final_consensus["confidence"],
            parameters=all_parameters,
            start_time=start_time,
            end_time=end_time,
            iterations=len(rounds) // len(self.minds),
            dissenting_views=final_consensus.get("dissent", [])
        )
        
        self.debate_history.append(debate)
        
        # Mantém apenas últimos 100 debates no histórico
        if len(self.debate_history) > 100:
            self.debate_history = self.debate_history[-100:]
        
        return debate
    
    def _calculate_consensus(self, parameters: List[AgentParameter]) -> float:
        """Calcula nível de consenso baseado nos parâmetros gerados"""
        if not parameters:
            return 0.0
        
        # Calcula confiança média
        avg_confidence = sum(p.confidence for p in parameters) / len(parameters)
        
        # Verifica consistência de valores
        values = [p.value for p in parameters if isinstance(p.value, (int, float))]
        if values:
            value_variance = sum((v - sum(values)/len(values))**2 for v in values) / len(values)
            consistency = 1.0 / (1.0 + value_variance)
        else:
            consistency = 1.0
        
        return (avg_confidence + consistency) / 2
    
    def _generate_final_consensus(
        self, 
        topic: str, 
        rounds: List[DebateRound], 
        parameters: List[AgentParameter]
    ) -> Dict[str, Any]:
        """Gera o consenso final baseado em todas as contribuições"""
        
        # Coleta contribuições de cada mente
        contributions = {}
        for round in rounds:
            if round.mind_name not in contributions:
                contributions[round.mind_name] = []
            contributions[round.mind_name].append(round.output)
        
        # Gera texto de consenso
        consensus_text = f"""
[CONSENSO BRX - 8 Mentes sobre "{topic}"]

Após debate circular com {len(rounds)} rodadas e {len(parameters)} parâmetros gerados:

Contribuições principais:
"""
        
        for mind_name, outputs in contributions.items():
            consensus_text += f"\n {mind_name}: {outputs[-1][:100]}..."
        
        consensus_text += f"""

Parâmetros-chave identificados:
"""
        
        # Agrupa parâmetros por tipo
        by_type = {}
        for p in parameters:
            pt = p.param_type.value
            if pt not in by_type:
                by_type[pt] = []
            by_type[pt].append(p)
        
        for ptype, params in by_type.items():
            avg_value = sum(p.value for p in params if isinstance(p.value, (int, float))) / len(params) if params else 0
            consensus_text += f"\n {ptype}: {len(params)} parâmetros (valor médio: {avg_value:.3f})"
        
        # Calcula confiança geral
        avg_confidence = sum(p.confidence for p in parameters) / len(parameters) if parameters else 0.5
        
        return {
            "text": consensus_text,
            "confidence": avg_confidence,
            "dissent": []  # Pode ser expandido para incluir visões divergentes
        }
    
    def get_mind(self, role: MindRole) -> Optional[Mind]:
        """Retorna uma mente específica"""
        return self.minds.get(role)
    
    def get_active_minds(self) -> List[Mind]:
        """Retorna todas as mentes ativas"""
        return [m for m in self.minds.values() if m.state.active]
    
    def toggle_mind(self, role: MindRole):
        """Ativa/desativa uma mente"""
        if role in self.minds:
            self.minds[role].state.active = not self.minds[role].state.active
    
    def register_thought_handler(self, handler: ThoughtHandler):
        """Registra um handler para observar pensamentos em tempo real"""
        self.thought_handlers.append(handler)
    
    def get_debate_history(self) -> List[CircularDebate]:
        """Retorna histórico de debates"""
        return self.debate_history
