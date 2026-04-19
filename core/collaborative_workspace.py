# BRX-AGENT v3.0 - Workspace Colaborativo
# Espaco compartilhado onde todos os agentes veem e reagem ao trabalho dos outros

import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from core.types import SpecializedAgent, CollaborativeTask


@dataclass
class WorkspaceEntry:
    """Uma entrada no workspace compartilhado"""
    id: str
    agent_id: str
    agent_name: str
    entry_type: str  # thought, code, design, decision, question, feedback
    content: str
    timestamp: float
    tags: List[str] = field(default_factory=list)
    reactions: Dict[str, str] = field(default_factory=dict)  # agent_id -> reaction
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "agent": self.agent_name,
            "type": self.entry_type,
            "content": self.content[:500] if len(self.content) > 500 else self.content,
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
            "tags": self.tags,
            "reactions": self.reactions
        }


class CollaborativeWorkspace:
    """
    Workspace colaborativo onde todos os agentes trabalham juntos
    - Todos podem ver o que os outros estao fazendo em tempo real
    - Agentes podem reagir ao trabalho dos outros
    - Decisoes sao tomadas colaborativamente
    - Progresso e rastreado visualmente
    """
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.entries: List[WorkspaceEntry] = []
        self.agent_status: Dict[str, Dict] = {}  # agent_id -> status
        self.shared_decisions: List[Dict] = []
        self.progress_percentage: float = 0.0
        self.created_at = time.time()
        self.last_update = time.time()
    
    def add_entry(self, agent: SpecializedAgent, entry_type: str, 
                  content: str, tags: List[str] = None) -> WorkspaceEntry:
        """Adiciona uma entrada ao workspace"""
        entry = WorkspaceEntry(
            id=f"entry_{len(self.entries)}_{int(time.time())}",
            agent_id=agent.id,
            agent_name=agent.name,
            entry_type=entry_type,
            content=content,
            timestamp=time.time(),
            tags=tags or []
        )
        
        self.entries.append(entry)
        self.last_update = time.time()
        
        # Atualiza status do agente
        self._update_agent_status(agent, entry_type, content)
        
        return entry
    
    def add_reaction(self, entry_id: str, agent: SpecializedAgent, reaction: str):
        """Um agente reage a uma entrada do workspace"""
        for entry in self.entries:
            if entry.id == entry_id:
                entry.reactions[agent.name] = reaction
                self.last_update = time.time()
                return True
        return False
    
    def add_decision(self, agent: SpecializedAgent, decision: str, rationale: str):
        """Registra uma decisao tomada colaborativamente"""
        decision_entry = {
            "id": f"decision_{len(self.shared_decisions)}",
            "agent": agent.name,
            "decision": decision,
            "rationale": rationale,
            "timestamp": time.time(),
            "approved_by": [agent.name]
        }
        
        self.shared_decisions.append(decision_entry)
        self.last_update = time.time()
    
    def approve_decision(self, decision_id: str, agent: SpecializedAgent):
        """Um agente aprova uma decisao"""
        for decision in self.shared_decisions:
            if decision["id"] == decision_id:
                if agent.name not in decision["approved_by"]:
                    decision["approved_by"].append(agent.name)
                self.last_update = time.time()
                return True
        return False
    
    def get_visible_entries_for_agent(self, agent_id: str, 
                                       entry_types: List[str] = None) -> List[WorkspaceEntry]:
        """Retorna entradas visiveis para um agente especifico"""
        if entry_types:
            return [e for e in self.entries if e.entry_type in entry_types]
        return self.entries
    
    def get_recent_entries(self, count: int = 10) -> List[WorkspaceEntry]:
        """Retorna as entradas mais recentes"""
        return sorted(self.entries, key=lambda e: e.timestamp, reverse=True)[:count]
    
    def get_entries_by_agent(self, agent_id: str) -> List[WorkspaceEntry]:
        """Retorna entradas de um agente especifico"""
        return [e for e in self.entries if e.agent_id == agent_id]
    
    def get_entries_by_type(self, entry_type: str) -> List[WorkspaceEntry]:
        """Retorna entradas por tipo"""
        return [e for e in self.entries if e.entry_type == entry_type]
    
    def update_progress(self, percentage: float):
        """Atualiza progresso geral do workspace"""
        self.progress_percentage = min(100.0, max(0.0, percentage))
        self.last_update = time.time()
    
    def _update_agent_status(self, agent: SpecializedAgent, entry_type: str, content: str):
        """Atualiza o status de um agente no workspace"""
        self.agent_status[agent.id] = {
            "name": agent.name,
            "role": agent.role,
            "last_activity": time.time(),
            "last_entry_type": entry_type,
            "status": "active",
            "contributions_count": self.agent_status.get(agent.id, {}).get("contributions_count", 0) + 1
        }
    
    def get_workspace_summary(self) -> Dict[str, Any]:
        """Retorna resumo do workspace"""
        # Conta entradas por tipo
        entries_by_type = {}
        for entry in self.entries:
            entries_by_type[entry.entry_type] = entries_by_type.get(entry.entry_type, 0) + 1
        
        # Conta contribuicoes por agente
        contributions_by_agent = {}
        for entry in self.entries:
            agent_name = entry.agent_name
            contributions_by_agent[agent_name] = contributions_by_agent.get(agent_name, 0) + 1
        
        return {
            "task_id": self.task_id,
            "total_entries": len(self.entries),
            "entries_by_type": entries_by_type,
            "active_agents": len(self.agent_status),
            "agent_status": {
                name: {
                    "status": info["status"],
                    "contributions": info["contributions_count"],
                    "last_activity": datetime.fromtimestamp(info["last_activity"]).isoformat()
                }
                for name, info in self.agent_status.items()
            },
            "decisions": len(self.shared_decisions),
            "decisions_approved": len([d for d in self.shared_decisions if len(d["approved_by"]) > 1]),
            "progress": f"{self.progress_percentage:.0f}%",
            "created": datetime.fromtimestamp(self.created_at).isoformat(),
            "last_update": datetime.fromtimestamp(self.last_update).isoformat()
        }
    
    def render_workspace_view(self) -> str:
        """Renderiza uma visualizacao textual do workspace"""
        summary = self.get_workspace_summary()
        
        view = f"""
{'='*70}
WORKSPACE COLABORATIVO - {self.task_id}
{'='*70}

Progresso: {summary['progress']} | Entradas: {summary['total_entries']} | Agentes: {summary['active_agents']}
Decisoes: {summary['decisions']} ({summary['decisions_approved']} aprovadas)

ULTIMAS ATIVIDADES:
{'-'*70}
"""
        
        for entry in self.get_recent_entries(5):
            reactions = ", ".join([f"{k}: {v}" for k, v in entry.reactions.items()]) if entry.reactions else ""
            view += f"\n[{entry.agent_name}] {entry.entry_type.upper()}\n"
            view += f"  {entry.content[:150]}...\n"
            if reactions:
                view += f"  Reacoes: {reactions}\n"
            view += f"  {datetime.fromtimestamp(entry.timestamp).strftime('%H:%M:%S')}\n"
        
        view += f"\n{'-'*70}\n"
        view += "STATUS DOS AGENTES:\n"
        view += f"{'-'*70}\n"
        
        for agent_id, status in self.agent_status.items():
            view += f"  {status['name']} ({status['role']}): {status['status']} - "
            view += f"{status['contributions']} contribuicoes\n"
        
        view += f"\n{'='*70}\n"
        
        return view
    
    def to_dict(self) -> Dict:
        """Serializa o workspace"""
        return {
            "task_id": self.task_id,
            "entries": [e.to_dict() for e in self.entries],
            "agent_status": self.agent_status,
            "decisions": self.shared_decisions,
            "progress": self.progress_percentage,
            "created": self.created_at,
            "last_update": self.last_update
        }


class WorkspaceManager:
    """
    Gerenciador de workspaces colaborativos
    Mantem todos os workspaces ativos e fornece acesso global
    """
    
    def __init__(self):
        self.workspaces: Dict[str, CollaborativeWorkspace] = {}
    
    def create_workspace(self, task_id: str) -> CollaborativeWorkspace:
        """Cria um novo workspace para uma tarefa"""
        workspace = CollaborativeWorkspace(task_id)
        self.workspaces[task_id] = workspace
        return workspace
    
    def get_workspace(self, task_id: str) -> Optional[CollaborativeWorkspace]:
        """Retorna um workspace pelo ID da tarefa"""
        return self.workspaces.get(task_id)
    
    def get_or_create(self, task_id: str) -> CollaborativeWorkspace:
        """Retorna workspace existente ou cria novo"""
        if task_id not in self.workspaces:
            return self.create_workspace(task_id)
        return self.workspaces[task_id]
    
    def list_workspaces(self) -> List[Dict]:
        """Lista todos os workspaces"""
        return [
            {
                "task_id": ws.task_id,
                "entries": len(ws.entries),
                "agents": len(ws.agent_status),
                "progress": ws.progress_percentage,
                "last_update": ws.last_update
            }
            for ws in self.workspaces.values()
        ]
    
    def cleanup_old_workspaces(self, max_age_hours: float = 24):
        """Remove workspaces antigos"""
        current_time = time.time()
        to_remove = []
        
        for task_id, workspace in self.workspaces.items():
            age_hours = (current_time - workspace.last_update) / 3600
            if age_hours > max_age_hours:
                to_remove.append(task_id)
        
        for task_id in to_remove:
            del self.workspaces[task_id]
        
        return len(to_remove)


# Singleton
_workspace_manager: Optional[WorkspaceManager] = None

def get_workspace_manager() -> WorkspaceManager:
    """Retorna instancia singleton do gerenciador"""
    global _workspace_manager
    if _workspace_manager is None:
        _workspace_manager = WorkspaceManager()
    return _workspace_manager

def reset_workspace_manager():
    """Reseta o gerenciador"""
    global _workspace_manager
    _workspace_manager = None
