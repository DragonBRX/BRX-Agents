# BRX-AGENT v3.0 - Orquestrador de Agentes
# Gerencia a ativacao, execucao e colaboracao dos agentes especializados

import uuid
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.types import (
    SpecializedAgent, CollaborativeTask, AgentRegistry,
    TaskAnalysis, AgentCategory
)
from core.task_analyzer import TaskAnalyzer
from agents.agent_catalog import get_agent_registry


class AgentOrchestrator:
    """
    Orquestrador do Sistema Multi-Agente
    - Analisa a tarefa
    - Seleciona e ativa os agentes adequados
    - Coordena a execucao colaborativa
    - Permite que todos os agentes vejam o trabalho dos outros
    """
    
    def __init__(self, max_agents: int = 8, max_workers: int = 8):
        self.max_agents = max_agents
        self.max_workers = max_workers
        self.registry = get_agent_registry()
        self.analyzer = TaskAnalyzer(max_agents=max_agents)
        
        # Tarefas em andamento
        self.active_tasks: Dict[str, CollaborativeTask] = {}
        self.completed_tasks: List[CollaborativeTask] = []
        
        # Callbacks
        self.task_start_callbacks: List[Callable] = []
        self.task_complete_callbacks: List[Callable] = []
        self.agent_thought_callbacks: List[Callable] = []
        
        # Contadores
        self.tasks_created = 0
        self.tasks_completed = 0
    
    def process_task(self, task_description: str, context: str = "") -> CollaborativeTask:
        """
        Processa uma tarefa completa:
        1. Analisa a tarefa
        2. Seleciona agentes
        3. Ativa e executa colaborativamente
        4. Retorna resultado consolidado
        """
        # 1. Analisa a tarefa
        print(f"\n[Orquestrador] Analisando tarefa: '{task_description[:60]}...'")
        analysis = self.analyzer.analyze(task_description)
        
        print(self.analyzer.get_suggested_team_summary(analysis))
        
        # 2. Cria tarefa colaborativa
        task = self._create_task(task_description, analysis)
        
        # 3. Ativa e atribui agentes
        self._assign_agents_to_task(task, analysis.recommended_agents)
        
        # 4. Executa colaborativamente
        print(f"\n[Orquestrador] Iniciando trabalho colaborativo com {len(task.assigned_agents)} agentes...")
        self._execute_collaborative_work(task, analysis, context)
        
        # 5. Consolida resultado
        self._consolidate_results(task)
        
        return task
    
    def _create_task(self, description: str, analysis: TaskAnalysis) -> CollaborativeTask:
        """Cria uma nova tarefa colaborativa"""
        self.tasks_created += 1
        
        task = CollaborativeTask(
            id=f"task_{uuid.uuid4().hex[:8]}_{self.tasks_created}",
            description=description,
            status="active",
            max_rounds=analysis.estimated_rounds,
            created_at=time.time(),
            workspace={
                "analysis": analysis.to_dict(),
                "shared_notes": [],
                "artifacts": {},
                "decisions": [],
                "progress_log": []
            }
        )
        
        self.active_tasks[task.id] = task
        
        # Notifica callbacks
        for callback in self.task_start_callbacks:
            try:
                callback(task)
            except Exception as e:
                print(f"[Orquestrador] Erro em callback de inicio: {e}")
        
        return task
    
    def _assign_agents_to_task(self, task: CollaborativeTask, agent_ids: List[str]):
        """Ativa e atribui agentes a uma tarefa"""
        agents = []
        
        for agent_id in agent_ids:
            if agent_id in self.registry.agents:
                agent = self.registry.agents[agent_id]
                # Cria copia do agente para esta tarefa
                agent_copy = self._clone_agent_for_task(agent, task.id)
                agents.append(agent_copy)
                print(f"  [Agente Ativado] {agent_copy.name} ({agent_copy.role})")
        
        task.assigned_agents = agents
    
    def _clone_agent_for_task(self, agent: SpecializedAgent, task_id: str) -> SpecializedAgent:
        """Cria uma copia do agente para trabalhar em uma tarefa especifica"""
        return SpecializedAgent(
            id=f"{agent.id}_{task_id}",
            name=agent.name,
            role=agent.role,
            category=agent.category,
            specialty=agent.specialty,
            objective=agent.objective,
            focus=agent.focus,
            personality_traits=agent.personality_traits.copy(),
            skills=agent.skills.copy(),
            languages=agent.languages.copy(),
            tools=agent.tools.copy(),
            weight=agent.weight,
            active=True,
            current_task=task_id,
            workspace_output="",
            collaboration_notes=[],
            task_history=agent.task_history.copy(),
            tasks_completed=agent.tasks_completed,
            contribution_score=agent.contribution_score
        )
    
    def _execute_collaborative_work(self, task: CollaborativeTask, analysis: TaskAnalysis, context: str = ""):
        """
        Executa o trabalho colaborativo entre os agentes
        Todos os agentes trabalham em paralelo e veem o progresso dos outros
        """
        shared_workspace = task.workspace
        
        for round_num in range(task.max_rounds):
            print(f"\n  [Rodada {round_num + 1}/{task.max_rounds}]")
            
            # Todos os agentes contribuem em paralelo
            round_results = self._execute_round_parallel(task, analysis, context, shared_workspace)
            
            # Atualiza workspace compartilhado (todos veem)
            self._update_shared_workspace(task, round_results)
            
            task.rounds_completed += 1
            
            # Verifica se atingiu consenso ou conclusao
            if self._check_completion(task, round_results):
                print(f"  [Orquestrador] Consenso atingido na rodada {round_num + 1}")
                break
        
        # Finaliza
        task.status = "completed"
        task.completed_at = time.time()
        self.tasks_completed += 1
        
        # Move para completadas
        if task.id in self.active_tasks:
            del self.active_tasks[task.id]
        self.completed_tasks.append(task)
    
    def _execute_round_parallel(self, task: CollaborativeTask, analysis: TaskAnalysis, 
                                 context: str, workspace: Dict) -> Dict[str, str]:
        """Executa uma rodada com todos os agentes em paralelo usando threads"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submete tarefas para cada agente
            future_to_agent = {}
            
            for agent in task.assigned_agents:
                future = executor.submit(
                    self._agent_work_unit,
                    agent,
                    task,
                    analysis,
                    context,
                    workspace
                )
                future_to_agent[future] = agent
            
            # Coleta resultados conforme completam
            for future in as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    output = future.result(timeout=30)
                    results[agent.id] = output
                    
                    # Atualiza output do agente
                    agent.workspace_output = output
                    
                    print(f"    [{agent.name}] Contribuicao recebida ({len(output)} chars)")
                    
                except Exception as e:
                    print(f"    [{agent.name}] Erro: {e}")
                    results[agent.id] = f"[Erro na contribuicao de {agent.name}: {str(e)}]"
        
        return results
    
    def _agent_work_unit(self, agent: SpecializedAgent, task: CollaborativeTask,
                         analysis: TaskAnalysis, context: str, 
                         workspace: Dict) -> str:
        """
        Unidade de trabalho de um agente
        Cada agente processa a tarefa com sua especialidade unica
        e pode ver o que os outros ja fizeram
        """
        # Personalidade influencia o estilo de trabalho
        personality_modifier = self._get_personality_modifier(agent)
        
        # Ve o que os outros agentes ja fizeram (workspace compartilhado)
        other_outputs = self._get_other_agent_outputs(task, agent.id)
        
        # Gera contribuicao baseada na especialidade
        contribution = self._generate_agent_contribution(
            agent, task, analysis, context, workspace, other_outputs
        )
        
        # Adiciona nota de colaboracao
        collaboration_note = self._generate_collaboration_note(agent, other_outputs)
        agent.collaboration_notes.append(collaboration_note)
        
        # Notifica callbacks de pensamento
        for callback in self.agent_thought_callbacks:
            try:
                callback(agent, contribution, task.id)
            except Exception:
                pass
        
        return contribution
    
    def _get_personality_modifier(self, agent: SpecializedAgent) -> str:
        """Gera um modificador baseado na personalidade do agente"""
        trait_modifiers = {
            "precise": "com precisao tecnica rigorosa",
            "creative": "com abordagem criativa e inovadora",
            "pragmatic": "com foco pratico e solucoes viaveis",
            "analytical": "com analise detalhada e fundamentada",
            "collaborative": "considerando todas as perspectivas da equipe",
            "strict": "seguindo padroes rigidos de qualidade",
            "visionary": "com visao de longo prazo e inovacao",
            "methodical": "de forma metodica e organizada",
            "adaptable": "adaptando-se ao contexto do projeto",
            "enthusiastic": "com entusiasmo e energia criativa",
            "curious": "com curiosidade exploradora",
            "organized": "de forma organizada e estruturada",
            "empathetic": "com empatia e foco humano",
            "technical": "com profundidade tecnica",
            "historical": "com base em conhecimento historico",
            "meticulous": "com atencao meticulosa aos detalhes",
            "innovative": "com abordagem inovadora e disruptiva"
        }
        
        modifiers = []
        for trait in agent.personality_traits:
            if trait.value in trait_modifiers:
                modifiers.append(trait_modifiers[trait.value])
        
        return ", ".join(modifiers) if modifiers else "com sua expertise"
    
    def _get_other_agent_outputs(self, task: CollaborativeTask, current_agent_id: str) -> List[str]:
        """Pega os outputs dos outros agentes para visibilidade cruzada"""
        outputs = []
        for agent in task.assigned_agents:
            if agent.id != current_agent_id and agent.workspace_output:
                outputs.append(f"[{agent.name}]: {agent.workspace_output[:200]}...")
        return outputs
    
    def _generate_agent_contribution(self, agent: SpecializedAgent, task: CollaborativeTask,
                                     analysis: TaskAnalysis, context: str,
                                     workspace: Dict, other_outputs: List[str]) -> str:
        """Gera a contribuicao unica de cada agente baseada em sua especialidade"""
        
        personality = self._get_personality_modifier(agent)
        task_desc = task.description
        
        # Base da contribuicao
        contribution = f"""
[{agent.name} - {agent.role}] trabalhando {personality}

Analise da tarefa: '{task_desc[:80]}...'

Perspectiva especializada ({agent.specialty}):
"""
        
        # Adiciona perspectiva baseada na categoria
        if agent.category == AgentCategory.DEVELOPMENT:
            contribution += self._dev_perspective(agent, task_desc)
        elif agent.category == AgentCategory.DESIGN:
            contribution += self._design_perspective(agent, task_desc)
        elif agent.category == AgentCategory.CONTENT:
            contribution += self._content_perspective(agent, task_desc)
        elif agent.category == AgentCategory.DATA:
            contribution += self._data_perspective(agent, task_desc)
        elif agent.category == AgentCategory.SECURITY:
            contribution += self._security_perspective(agent, task_desc)
        elif agent.category == AgentCategory.INFRASTRUCTURE:
            contribution += self._infra_perspective(agent, task_desc)
        elif agent.category == AgentCategory.BUSINESS:
            contribution += self._business_perspective(agent, task_desc)
        elif agent.category == AgentCategory.RESEARCH:
            contribution += self._research_perspective(agent, task_desc)
        elif agent.category == AgentCategory.CREATIVE:
            contribution += self._creative_perspective(agent, task_desc)
        elif agent.category == AgentCategory.QUALITY:
            contribution += self._quality_perspective(agent, task_desc)
        elif agent.category == AgentCategory.PROJECT:
            contribution += self._project_perspective(agent, task_desc)
        elif agent.category == AgentCategory.COMMUNICATION:
            contribution += self._communication_perspective(agent, task_desc)
        else:
            contribution += self._generic_perspective(agent, task_desc)
        
        # Adiciona reacoes ao trabalho dos outros (se houver)
        if other_outputs:
            contribution += "\n\nReacao ao trabalho da equipe:\n"
            for output in other_outputs[:3]:  # Max 3 para nao ficar muito longo
                contribution += f"  - {output}\n"
            contribution += self._generate_cross_feedback(agent)
        
        # Adiciona sugestoes especificas
        contribution += f"\n\nSugestoes de {agent.name}:\n"
        contribution += self._generate_suggestions(agent, task_desc)
        
        return contribution
    
    def _dev_perspective(self, agent: SpecializedAgent, task: str) -> str:
        perspectives = {
            "Backend Developer": f"Analisando arquitetura de servidor e APIs para: '{task[:50]}...'\nConsiderando escalabilidade, padroes RESTful, e eficiencia de banco de dados.\nSugestao de stack: Python/FastAPI ou Node.js/Express com PostgreSQL.",
            "Frontend Developer": f"Avaliando experiencia de usuario e componentes para: '{task[:50]}...'\nFoco em responsividade, acessibilidade e performance de renderizacao.\nSugestao: React/TypeScript com Tailwind CSS e Vite.",
            "Fullstack Developer": f"Visao completa de frontend a backend para: '{task[:50]}...'\nBalanceando UX com arquitetura de dados.\nSugestao: Next.js com Prisma e PostgreSQL.",
            "Mobile Developer": f"Otimizando para dispositivos moveis: '{task[:50]}...'\nConsiderando touch targets, performance offline e integracao nativa.\nSugestao: React Native ou Flutter.",
            "AI/ML Engineer": f"Modelando solucao inteligente para: '{task[:50]}...'\nAvaliando algoritmos, features e pipeline de treinamento.\nSugestao: PyTorch com FastAPI para serving.",
            "Game Developer": f"Projetando game mechanics e arquitetura para: '{task[:50]}...'\nConsiderando game loop, physics e rendering pipeline.\nSugestao: Unity (C#) ou Godot para 2D.",
            "Blockchain Developer": f"Avaliando descentralizacao e smart contracts para: '{task[:50]}...'\nConsiderando gas optimization e seguranca.\nSugestao: Solidity com Hardhat/Foundry.",
        }
        return perspectives.get(agent.role, f"Analisando requisitos tecnicos para: '{task[:50]}...'")
    
    def _design_perspective(self, agent: SpecializedAgent, task: str) -> str:
        perspectives = {
            "UI Designer": f"Criando sistema de componentes visual para: '{task[:50]}...'\nFoco em consistencia, tokens de design e estados de componentes.\nEntregavel: Design system com variants e auto-layout.",
            "UX Designer": f"Mapeando jornada do usuario para: '{task[:50]}...'\nConsiderando pain points, mental models e fluxos de navegacao.\nEntregavel: User flow, wireframes e teste de usabilidade.",
            "Graphic Designer": f"Desenvolvendo identidade visual para: '{task[:50]}...'\nCriando sistema visual coeso com paleta, tipografia e iconografia.\nEntregavel: Logo, guidelines e aplicacoes.",
            "Motion Designer": f"Projetando microinteracoes e transicoes para: '{task[:50]}...'\nFoco em feedback visual e delight moments.\nEntregavel: Lottie files e especificacoes de easing.",
            "3D Artist": f"Modelando assets tridimensionais para: '{task[:50]}...'\nConsiderando topology, UV mapping e optimization.\nEntregavel: Modelos 3D otimizados para web.",
        }
        return perspectives.get(agent.role, f"Criando solucao de design para: '{task[:50]}...'")
    
    def _content_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Estruturando conteudo e narrativa para: '{task[:50]}...'\nConsiderando persona do publico, SEO e clareza.\nEntregavel: Conteudo otimizado e bem estruturado."
    
    def _data_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Analisando requisitos de dados para: '{task[:50]}...'\nConsiderando fontes, transformacoes e modelagem.\nEntregavel: Schema, queries e pipeline de dados."
    
    def _security_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Avaliando ameacas e vulnerabilidades para: '{task[:50]}...'\nConsiderando OWASP Top 10, autenticacao e autorizacao.\nEntregavel: Threat model e recomendacoes de seguranca."
    
    def _infra_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Planejando infraestrutura para: '{task[:50]}...'\nConsiderando escalabilidade, custos e observabilidade.\nEntregavel: Arquitetura cloud e pipeline CI/CD."
    
    def _business_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Avaliando viabilidade e estrategia para: '{task[:50]}...'\nConsiderando mercado, concorrencia e monetizacao.\nEntregavel: Analise de negocio e recomendacoes estrategicas."
    
    def _research_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Pesquisando estado da arte para: '{task[:50]}...'\nConsiderando tecnologias emergentes e best practices.\nEntregavel: Tech radar e proof of concept."
    
    def _creative_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Criando conceito artistico para: '{task[:50]}...'\nExplorando estilos, mood e narrativa visual.\nEntregavel: Mood board, conceitos e direcao artistica."
    
    def _quality_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Definindo estrategia de qualidade para: '{task[:50]}...'\nConsiderando cobertura de testes e criterios de aceitacao.\nEntregavel: Plano de testes e casos de teste."
    
    def _project_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Estruturando gestao do projeto para: '{task[:50]}...'\nConsiderando cronograma, riscos e stakeholders.\nEntregavel: Plano de projeto e roadmap."
    
    def _communication_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Planejando comunicacao para: '{task[:50]}...'\nConsiderando canais, mensagens e engajamento.\nEntregavel: Plano de comunicacao e conteudo."
    
    def _generic_perspective(self, agent: SpecializedAgent, task: str) -> str:
        return f"Contribuindo com expertise em {agent.specialty} para: '{task[:50]}...'"
    
    def _generate_cross_feedback(self, agent: SpecializedAgent) -> str:
        """Gera feedback cruzado baseado na personalidade do agente"""
        feedback_templates = {
            "precise": "\nPontos que precisam de maior precisao foram identificados. Sugiro revisar as especificacoes tecnicas.",
            "creative": "\nVejo oportunidades para inovar nas abordagens propostas. Vamos explorar alternativas criativas.",
            "pragmatic": "\nFocando no que e viavel de entregar. Priorizo solucoes que funcionam no mundo real.",
            "analytical": "\nAnalisando os dados e trade-offs apresentados. A decisao deve ser baseada em evidencias.",
            "collaborative": "\nExcelente trabalho em equipe! Vamos integrar as melhores ideias de cada especialista.",
            "strict": "\nIdentifiquei pontos que nao atendem aos padroes exigidos. Necessario revisao.",
            "visionary": "\nVejo o potencial de longo prazo desta solucao. Vamos alinhar com a visao estrategica.",
            "methodical": "\nSeguindo o processo passo a passo. Cada etapa esta sendo documentada adequadamente.",
            "adaptable": "\nAdaptando minha abordagem conforme o projeto evolui. Flexibilidade e chave.",
            "enthusiastic": "\nOtima energia da equipe! Vamos manter o momentum e entregar algo excepcional.",
            "curious": "\nExplorando novas abordagens e tecnologias. A curiosidade leva a solucoes inovadoras.",
            "organized": "\nMantendo a estrutura e organizacao do projeto. Documentacao e planejamento sao essenciais.",
            "empathetic": "\nConsiderando a experiencia do usuario e as necessidades das partes interessadas.",
            "technical": "\nAprofundando nos detalhes tecnicos. A solucao deve ser robusta e bem implementada.",
            "historical": "\nConsiderando aprendizados e padroes do passado. Historia informa boas decisoes.",
            "meticulous": "\nRevisando cada detalhe minuciosamente. A qualidade esta nos pequenos detalhes.",
            "innovative": "\nPropondo abordagens disruptivas e inovadoras. Vamos pensar fora da caixa."
        }
        
        feedbacks = []
        for trait in agent.personality_traits:
            if trait.value in feedback_templates:
                feedbacks.append(feedback_templates[trait.value])
        
        return "\n".join(feedbacks[:2]) if feedbacks else "\nContribuicao integrada com a equipe."
    
    def _generate_suggestions(self, agent: SpecializedAgent, task: str) -> str:
        """Gera sugestoes especificas do agente"""
        suggestions = []
        
        # Sugestoes baseadas em skills
        for skill in agent.skills[:3]:
            suggestions.append(f"  - Aplicar {skill} para otimizar a solucao")
        
        # Sugestoes baseadas em tools
        for tool in agent.tools[:2]:
            suggestions.append(f"  - Usar {tool} para acelerar o desenvolvimento")
        
        # Sugestao de linguagem
        if agent.languages:
            suggestions.append(f"  - Stack recomendada: {', '.join(agent.languages[:3])}")
        
        return "\n".join(suggestions)
    
    def _generate_collaboration_note(self, agent: SpecializedAgent, other_outputs: List[str]) -> str:
        """Gera uma nota sobre a colaboracao"""
        note = f"[{agent.name}] colaborou na rodada. "
        if other_outputs:
            note += f"Vi as contribuicoes de {len(other_outputs)} colegas e adaptei meu trabalho."
        else:
            note += "Primeira contribuicao da equipe."
        return note
    
    def _update_shared_workspace(self, task: CollaborativeTask, round_results: Dict[str, str]):
        """Atualiza o workspace compartilhado para que todos os agentes vejam"""
        task.workspace["progress_log"].append({
            "round": task.rounds_completed + 1,
            "timestamp": time.time(),
            "contributions": {k: v[:200] for k, v in round_results.items()}
        })
        
        # Atualiza outputs dos agentes
        for agent_id, output in round_results.items():
            task.agent_outputs[agent_id] = output
        
        # Atualiza notas compartilhadas
        for agent in task.assigned_agents:
            if agent.collaboration_notes:
                task.workspace["shared_notes"].append(agent.collaboration_notes[-1])
    
    def _check_completion(self, task: CollaborativeTask, round_results: Dict[str, str]) -> bool:
        """Verifica se a tarefa atingiu condicoes de conclusao"""
        # Verifica se todos os agentes contribuiram significativamente
        all_contributed = all(len(output) > 50 for output in round_results.values())
        
        # Na ultima rodada, sempre completa
        if task.rounds_completed >= task.max_rounds - 1:
            return True
        
        # Se todos contribuiram bem, pode terminar mais cedo
        if all_contributed and task.rounds_completed >= 2:
            return True
        
        return False
    
    def _consolidate_results(self, task: CollaborativeTask):
        """Consolida os resultados de todos os agentes em um resultado final"""
        consolidated = f"""
{'='*70}
RESULTADO COLABORATIVO - TAREFA: {task.description[:60]}
{'='*70}

Equipe ({len(task.assigned_agents)} agentes):
"""
        
        for agent in task.assigned_agents:
            consolidated += f"  - {agent.name} ({agent.role}) - {agent.specialty}\n"
        
        consolidated += f"\nRodadas de colaboracao: {task.rounds_completed}\n"
        consolidated += f"Tempo total: {task.completed_at - task.created_at:.1f}s\n"
        consolidated += f"\n{'='*70}\n"
        consolidated += "CONTRIBUICOES POR AGENTE:\n"
        consolidated += f"{'='*70}\n"
        
        for agent in task.assigned_agents:
            if agent.id in task.agent_outputs:
                output = task.agent_outputs[agent.id]
                consolidated += f"\n[{agent.name} - {agent.role}]\n"
                consolidated += f"Personalidade: {agent.get_personality_description()}\n"
                consolidated += f"-{ '-'*50 }\n"
                consolidated += f"{output}\n"
        
        consolidated += f"\n{'='*70}\n"
        consolidated += "SINTESE DAS COLABORACOES:\n"
        consolidated += f"{'='*70}\n"
        
        for note in task.workspace.get("shared_notes", []):
            consolidated += f"  {note}\n"
        
        consolidated += f"\n{'='*70}\n"
        
        task.final_result = consolidated
        
        # Notifica callbacks
        for callback in self.task_complete_callbacks:
            try:
                callback(task)
            except Exception as e:
                print(f"[Orquestrador] Erro em callback de conclusao: {e}")
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Retorna status de uma tarefa"""
        if task_id in self.active_tasks:
            return self.active_tasks[task_id].to_dict()
        for task in self.completed_tasks:
            if task.id == task_id:
                return task.to_dict()
        return None
    
    def get_all_tasks(self) -> List[Dict]:
        """Retorna todas as tarefas"""
        all_tasks = list(self.active_tasks.values()) + self.completed_tasks
        return [t.to_dict() for t in sorted(all_tasks, key=lambda x: x.created_at, reverse=True)]
    
    def get_active_agents_summary(self) -> Dict[str, Any]:
        """Retorna resumo dos agentes ativos"""
        active = self.registry.get_active()
        by_category = {}
        for agent in active:
            cat = agent.category.value
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append({
                "id": agent.id,
                "name": agent.name,
                "role": agent.role,
                "task": agent.current_task
            })
        
        return {
            "total_active": len(active),
            "by_category": by_category,
            "max_agents": self.max_agents,
            "tasks_in_progress": len(self.active_tasks),
            "tasks_completed": self.tasks_completed
        }
    
    def deactivate_all_agents(self):
        """Desativa todos os agentes"""
        self.registry.deactivate_all()
        print("[Orquestrador] Todos os agentes desativados")
    
    def register_task_start_callback(self, callback: Callable):
        """Registra callback para inicio de tarefa"""
        self.task_start_callbacks.append(callback)
    
    def register_task_complete_callback(self, callback: Callable):
        """Registra callback para conclusao de tarefa"""
        self.task_complete_callbacks.append(callback)
    
    def register_agent_thought_callback(self, callback: Callable):
        """Registra callback para pensamentos de agentes"""
        self.agent_thought_callbacks.append(callback)


# Singleton
_orchestrator: Optional[AgentOrchestrator] = None

def get_orchestrator(max_agents: int = 8, max_workers: int = 8) -> AgentOrchestrator:
    """Retorna instancia singleton do orquestrador"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator(max_agents=max_agents, max_workers=max_workers)
    return _orchestrator

def reset_orchestrator():
    """Reseta o orquestrador"""
    global _orchestrator
    _orchestrator = None
