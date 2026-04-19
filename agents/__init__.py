# BRX-AGENT v3.0 - Sistema Multi-Agente
# Catalogo de 100+ agentes especializados

from agents.agent_catalog import (
    get_agent_registry,
    get_agent_by_id,
    get_agents_by_category,
    list_all_agents,
    get_agent_categories_summary,
    create_full_agent_registry,
    reset_agent_registry
)

__all__ = [
    'get_agent_registry',
    'get_agent_by_id', 
    'get_agents_by_category',
    'list_all_agents',
    'get_agent_categories_summary',
    'create_full_agent_registry',
    'reset_agent_registry'
]
