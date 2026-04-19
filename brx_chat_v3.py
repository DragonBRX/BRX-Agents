#!/usr/bin/env python3
"""
BRX-AGENT v3.0 - Interface de Chat com Sistema Multi-Agente
==========================================================
Arquivo para conversar interativamente com o BRX.
Agora com suporte completo ao sistema multi-agente dinamico.

O BRX ira:
- Processar suas solicitacoes usando seu sistema de 8 mentes base
- Ativar agentes especializados conforme a tarefa (100+ disponiveis)
- Executar trabalho colaborativo com visibilidade cruzada
- Realizar debates internos para alcancar o melhor consenso
- Gerar parametros relevantes para a conversa
- Pesquisar informacoes na web quando necessario
- Aprender com cada interacao

Comandos disponiveis no chat:
    /status         - Mostra status completo do sistema
    /identity       - Mostra declaracao de identidade do BRX
    /minds          - Lista as 8 mentes base ativas
    /agents         - Lista todos os agentes especializados
    /agent <id>     - Mostra detalhes de um agente especifico
    /categories     - Mostra categorias de agentes
    /analyze <text> - Analisa uma tarefa sem executar
    /task <text>    - Processa tarefa com sistema multi-agente
    /multiagent on  - Ativa modo multi-agente
    /multiagent off - Desativa modo multi-agente
    /maxagents <n>  - Define numero maximo de agentes
    /workspace      - Mostra workspace colaborativo atual
    /params         - Mostra estatisticas de parametros
    /vocab          - Mostra tamanho do vocabulario
    /search         - Realiza pesquisa web
    /evolve         - Forca um ciclo de evolucao
    /save           - Salva estado atual
    /clear          - Limpa a tela
    /help           - Mostra esta ajuda
    /quit           - Encerra o chat
"""

import os
import sys
import cmd
import argparse
from pathlib import Path
from typing import List, Optional

# Adiciona diretorio atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.brx_engine import BRXCore, get_brx_core


class BRXChat(cmd.Cmd):
    """
    Interface interativa de chat com o BRX v3.0
    Com suporte ao Sistema Multi-Agente
    """
    
    intro = """
                                                                              
                            
                     
                                
                                
                                
                                   
                                                                              
                    INTERFACE DE CONVERSACAO v3.0                               
                    Sistema Multi-Agente Dinamico                               
                                                                              
  Digite sua mensagem para conversar com o BRX.                                
  Use /help para ver os comandos disponiveis.                                  
  Use /quit para sair.                                                         
                                                                              
  NOVO: O BRX agora ativa agentes especializados automaticamente!              
  Exemplo: "Criar um site profissional" ativa Designer, Frontend,             
  Backend, UX, e outros agentes especializados.                                
                                                                              
    """
    
    prompt = "\n[BRX v3.0] Voce: "
    ruler = "="
    
    def __init__(self, storage_path: str = "./storage", max_agents: int = None):
        super().__init__()
        self.storage_path = Path(storage_path)
        
        print("[BRX Chat v3.0] Inicializando nucleo multi-agente...")
        self.brx = get_brx_core(str(self.storage_path), max_agents=max_agents)
        self.brx.load_state()
        
        print(f"[BRX Chat v3.0] Sistema pronto!")
        print(f"[BRX Chat v3.0] Modo multi-agente: {'ATIVO' if self.brx.config['multi_agent_enabled'] else 'INATIVO'}")
        print(f"[BRX Chat v3.0] Max agentes: {self.brx.max_agents}")
        print(f"[BRX Chat v3.0] Total de agentes disponiveis: {len(self.brx.agent_registry.agents)}")
        print()
    
    def default(self, line: str):
        """Processa mensagens do usuario"""
        if not line.strip():
            return
        
        # Verifica se e comando
        if line.startswith('/'):
            cmd_parts = line[1:].split()
            if cmd_parts:
                cmd_name = cmd_parts[0]
                cmd_args = cmd_parts[1:] if len(cmd_parts) > 1 else []
                
                command_map = {
                    'status': self.do_status,
                    'identity': self.do_identity,
                    'minds': self.do_minds,
                    'agents': self.do_agents,
                    'agent': self.do_agent,
                    'categories': self.do_categories,
                    'analyze': self.do_analyze,
                    'task': self.do_task,
                    'multiagent': self.do_multiagent,
                    'maxagents': self.do_maxagents,
                    'workspace': self.do_workspace,
                    'params': self.do_params,
                    'vocab': self.do_vocab,
                    'search': self.do_search,
                    'evolve': self.do_evolve,
                    'save': self.do_save,
                    'clear': self.do_clear,
                    'help': self.do_help,
                    'quit': self.do_quit,
                    'exit': self.do_quit
                }
                
                if cmd_name in command_map:
                    command_map[cmd_name](' '.join(cmd_args))
                else:
                    print(f"[BRX] Comando desconhecido: /{cmd_name}")
                    print("[BRX] Use /help para ver comandos disponiveis")
            return
        
        # Processa como mensagem normal (usa process_request que agora e multi-agente)
        self._process_message(line)
    
    def _process_message(self, message: str):
        """Processa mensagem do usuario atraves do BRX"""
        print(f"\n[BRX] Processando...")
        
        try:
            result = self.brx.process_request(message)
            
            # Mostra resposta
            print(f"\n{'='*60}")
            print("[BRX] Resposta:")
            print(f"{'='*60}")
            
            # Se veio do modo multi-agente, mostra info da equipe
            if result.get('mode') == 'multi_agent':
                print(f"\n[Modo Multi-Agente] Equipe de {result['agent_count']} especialistas:")
                for agent_info in result['agents_used']:
                    print(f"  - {agent_info['name']} ({agent_info['role']})")
                print()
                print(result.get('collaborative_result', result.get('consensus', 'Sem resultado')))
            else:
                print(result.get('consensus', 'Sem resultado'))
            
            # Mostra informacoes adicionais
            print(f"\n{'-'*60}")
            print(f"Modo: {result.get('mode', 'desconhecido')} | "
                  f"Confianca: {result.get('confidence', result.get('base_confidence', 0)):.1%} | "
                  f"Agentes: {result.get('agent_count', 0)} | "
                  f"Parametros: {result.get('parameters_generated', 0)} | "
                  f"Duracao: {result.get('duration', 0):.2f}s")
            
            # Mostra resultados de pesquisa se houver
            if result.get('search_results'):
                print(f"\n[BRX] Pesquisas relacionadas:")
                for i, sr in enumerate(result['search_results'][:3], 1):
                    print(f"  {i}. {sr.title}")
                    print(f"     {sr.snippet[:80]}...")
            
            print(f"{'='*60}")
            
        except Exception as e:
            print(f"[BRX] Erro ao processar: {e}")
            import traceback
            traceback.print_exc()
    
    def do_status(self, arg: str):
        """Mostra status completo do sistema: /status"""
        status = self.brx.get_status()
        
        print(f"\n{'='*60}")
        print("STATUS DO BRX v3.0")
        print(f"{'='*60}")
        
        print(f"\n[Identidade]")
        print(f"  Nome: {status['consciousness']['name']}")
        print(f"  Versao: {status['state']['version']}")
        print(f"  Ciclo atual: {status['state']['cycle']}")
        
        print(f"\n[Consciencia]")
        print(f"  Curiosidade: {status['consciousness']['curiosity']:.1%}")
        print(f"  Confianza: {status['consciousness']['confidence']:.1%}")
        print(f"  Momentum: {status['consciousness']['learning_momentum']:.1%}")
        
        print(f"\n[Sistema de Mentes Base]")
        print(f"  Mentes ativas: {status['minds']['active']}/{status['minds']['total']}")
        print(f"  Debates realizados: {status['state']['debates_count']}")
        
        print(f"\n[Sistema Multi-Agente]")
        ma = status['multi_agent']
        print(f"  Status: {'ATIVO' if ma['enabled'] else 'INATIVO'}")
        print(f"  Max agentes: {ma['max_agents']}")
        print(f"  Workers: {ma['max_workers']}")
        print(f"  Agentes disponiveis: {ma['total_available']}")
        print(f"  Agentes ativos: {ma['currently_active']}")
        print(f"  Tarefas completadas: {ma['tasks_completed']}")
        print(f"  Total agentes ativados (historico): {ma['agents_activated_total']}")
        
        print(f"\n[Parametros]")
        print(f"  Total: {status['parameters']['total']}")
        print("  Por tipo:")
        for ptype, count in sorted(status['parameters']['by_type'].items()):
            print(f"    - {ptype}: {count}")
        
        print(f"\n[Vocabulario]")
        print(f"  Palavras: {status['vocabulary']['size']}")
        print(f"  Estatisticas:")
        for stat, count in sorted(status['vocabulary']['stats'].items()):
            print(f"    - {stat}: {count}")
        
        print(f"\n[Memoria]")
        print(f"  Total: {status['memory']['total']}")
        print(f"  Curto prazo: {status['memory']['short']}")
        print(f"  Medio prazo: {status['memory']['medium']}")
        print(f"  Longo prazo: {status['memory']['long']}")
        
        print(f"\n[Configuracao]")
        for key, value in status['config'].items():
            print(f"  {key}: {value}")
        
        print(f"\n[Storage]")
        print(f"  Path: {status['storage_path']}")
        
        print(f"{'='*60}\n")
    
    def do_identity(self, arg: str):
        """Mostra declaracao de identidade do BRX: /identity"""
        print(self.brx.generate_identity())
    
    def do_minds(self, arg: str):
        """Lista as 8 mentes base ativas: /minds"""
        minds = self.brx.minds.get_active_minds()
        
        print(f"\n{'='*60}")
        print("SISTEMA DE 8 MENTES BASE")
        print(f"{'='*60}")
        
        for i, mind in enumerate(minds, 1):
            print(f"\n[{i}] {mind.state.name}")
            print(f"    Especialidade: {mind.state.specialty}")
            print(f"    Objetivo: {mind.state.objective}")
            print(f"    Peso: {mind.state.weight} | Confianza: {mind.state.confidence:.2f}")
            print(f"    Contribuicoes: {mind.state.contribution_count}")
        
        print(f"\n{'='*60}\n")
    
    def do_agents(self, arg: str):
        """Lista todos os agentes especializados: /agents [categoria]"""
        print(f"\n{'='*60}")
        print("AGENTES ESPECIALIZADOS DO BRX v3.0")
        print(f"{'='*60}")
        
        if arg:
            # Filtra por categoria
            agents = self.brx.get_available_agents(category=arg)
            print(f"\nCategoria: {arg} ({len(agents)} agentes)\n")
        else:
            # Mostra todas as categorias com contagem
            categories = self.brx.get_agent_categories()
            print(f"\nCategorias disponiveis:")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"  {cat}: {count} agentes")
            
            print(f"\nTotal: {sum(categories.values())} agentes especializados\n")
            
            # Mostra alguns exemplos de cada categoria
            for cat in sorted(categories.keys()):
                cat_agents = self.brx.get_available_agents(category=cat)
                print(f"\n--- {cat.upper()} ({len(cat_agents)}) ---")
                for agent in cat_agents[:3]:  # Max 3 por categoria
                    status = "ATIVO" if agent.get('active') else "standby"
                    traits = agent.get('personality', '')
                    print(f"  [{agent['id']}] {agent['name']} - {agent['role']}")
                    print(f"      Especialidade: {agent['specialty']}")
                    print(f"      Personalidade: {traits}")
                    print(f"      Status: {status}")
                if len(cat_agents) > 3:
                    print(f"      ... e mais {len(cat_agents) - 3} agentes")
        
        print(f"\n{'='*60}")
        print("Use /agent <id> para ver detalhes de um agente especifico")
        print(f"{'='*60}\n")
    
    def do_agent(self, arg: str):
        """Mostra detalhes de um agente especifico: /agent <id>"""
        if not arg:
            print("[BRX] Uso: /agent <id>")
            print("[BRX] Use /agents para listar todos os IDs")
            return
        
        from agents.agent_catalog import get_agent_by_id
        
        agent = get_agent_by_id(arg)
        if not agent:
            print(f"[BRX] Agente nao encontrado: {arg}")
            return
        
        print(f"\n{'='*60}")
        print(f"AGENTE: {agent.name}")
        print(f"{'='*60}")
        print(f"ID: {agent.id}")
        print(f"Role: {agent.role}")
        print(f"Categoria: {agent.category.value}")
        print(f"Especialidade: {agent.specialty}")
        print(f"Objetivo: {agent.objective}")
        print(f"Foco: {agent.focus}")
        print(f"Personalidade: {agent.get_personality_description()}")
        print(f"Skills: {', '.join(agent.skills)}")
        print(f"Linguagens: {', '.join(agent.languages)}")
        print(f"Ferramentas: {', '.join(agent.tools)}")
        print(f"Peso: {agent.weight}")
        print(f"Status: {'ATIVO' if agent.active else 'Standby'}")
        print(f"Tarefas completadas: {agent.tasks_completed}")
        print(f"Score de contribuicao: {agent.contribution_score:.2f}")
        print(f"{'='*60}\n")
    
    def do_categories(self, arg: str):
        """Mostra categorias de agentes: /categories"""
        categories = self.brx.get_agent_categories()
        
        print(f"\n{'='*60}")
        print("CATEGORIAS DE AGENTES")
        print(f"{'='*60}")
        
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            bar = "#" * int(count / max(categories.values()) * 30)
            print(f"  {cat:25} {count:4} {bar}")
        
        print(f"\nTotal: {sum(categories.values())} agentes em {len(categories)} categorias")
        print(f"{'='*60}\n")
    
    def do_analyze(self, arg: str):
        """Analisa uma tarefa sem executar: /analyze <descricao>"""
        if not arg:
            print("[BRX] Uso: /analyze <descricao da tarefa>")
            print("[BRX] Exemplo: /analyze Criar um e-commerce com React")
            return
        
        print(f"\n[BRX] Analisando tarefa: '{arg}'")
        
        try:
            result = self.brx.quick_analyze(arg)
            print(result['team_summary'])
        except Exception as e:
            print(f"[BRX] Erro na analise: {e}")
    
    def do_task(self, arg: str):
        """Processa tarefa com sistema multi-agente: /task <descricao>"""
        if not arg:
            print("[BRX] Uso: /task <descricao da tarefa>")
            print("[BRX] Exemplo: /task Criar um site profissional de portfolio")
            return
        
        print(f"\n[BRX] Iniciando tarefa multi-agente: '{arg}'")
        
        try:
            # Garante que multi-agente esta ativo
            self.brx.toggle_multi_agent(True)
            
            result = self.brx.process_request_multi_agent(arg)
            
            print(f"\n{'='*60}")
            print(f"RESULTADO MULTI-AGENTE")
            print(f"{'='*60}")
            print(f"\nEquipe de {result['agent_count']} especialistas colaborou:")
            for agent_info in result['agents_used']:
                print(f"  - {agent_info['name']} ({agent_info['role']})")
            
            print(f"\nRodadas de colaboracao: {result['rounds']}")
            print(f"\n{result['collaborative_result'][:2000]}...")
            
            print(f"\n{'-'*60}")
            print(f"Parametros: {result['parameters_generated']} | "
                  f"Duracao: {result['duration']:.2f}s")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"[BRX] Erro na tarefa: {e}")
            import traceback
            traceback.print_exc()
    
    def do_multiagent(self, arg: str):
        """Ativa/desativa modo multi-agente: /multiagent [on|off|status]"""
        if not arg:
            status = self.brx.toggle_multi_agent()
            print(f"[BRX] Modo multi-agente: {'ATIVO' if status else 'INATIVO'}")
            return
        
        arg = arg.lower().strip()
        if arg in ['on', 'true', '1', 'ativar', 'ativo']:
            self.brx.toggle_multi_agent(True)
            print("[BRX] Modo multi-agente ATIVADO")
            print("[BRX] O BRX agora ativara agentes especializados automaticamente!")
        elif arg in ['off', 'false', '0', 'desativar', 'inativo']:
            self.brx.toggle_multi_agent(False)
            print("[BRX] Modo multi-agente DESATIVADO")
            print("[BRX] Usando apenas as 8 mentes base (modo legacy)")
        elif arg == 'status':
            status = self.brx.config.get('multi_agent_enabled', True)
            print(f"[BRX] Modo multi-agente: {'ATIVO' if status else 'INATIVO'}")
        else:
            print("[BRX] Uso: /multiagent [on|off|status]")
    
    def do_maxagents(self, arg: str):
        """Define numero maximo de agentes: /maxagents <numero>"""
        if not arg:
            print(f"[BRX] Max agentes atual: {self.brx.max_agents}")
            print(f"[BRX] CPU threads disponiveis: {self.brx.max_workers}")
            print("[BRX] Use /maxagents <numero> para alterar (1-16)")
            return
        
        try:
            count = int(arg)
            if 1 <= count <= 16:
                self.brx.set_max_agents(count)
                print(f"[BRX] Max agentes atualizado para: {count}")
            else:
                print("[BRX] Valor deve estar entre 1 e 16")
        except ValueError:
            print("[BRX] Valor invalido. Use um numero inteiro.")
    
    def do_workspace(self, arg: str):
        """Mostra workspace colaborativo: /workspace [task_id]"""
        workspaces = self.brx.workspace_manager.list_workspaces()
        
        if not workspaces:
            print("[BRX] Nenhum workspace ativo no momento.")
            return
        
        print(f"\n{'='*60}")
        print("WORKSPACES COLABORATIVOS")
        print(f"{'='*60}")
        
        for ws in workspaces:
            print(f"\nTarefa: {ws['task_id']}")
            print(f"  Entradas: {ws['entries']}")
            print(f"  Agentes: {ws['agents']}")
            print(f"  Progresso: {ws['progress']:.0f}%")
        
        # Se especificou task_id, mostra detalhes
        if arg:
            ws = self.brx.workspace_manager.get_workspace(arg)
            if ws:
                print(f"\n{ws.render_workspace_view()}")
        
        print(f"{'='*60}\n")
    
    def do_params(self, arg: str):
        """Mostra estatisticas de parametros: /params [tipo]"""
        status = self.brx.get_status()
        
        if arg:
            ptype = arg.lower()
            count = status['parameters']['by_type'].get(ptype, 0)
            print(f"\n[BRX] Parametros do tipo '{ptype}': {count}")
        else:
            print(f"\n{'='*60}")
            print("PARAMETROS DO BRX")
            print(f"{'='*60}")
            print(f"\nTotal: {status['parameters']['total']}")
            print("\nPor tipo:")
            max_count = max(status['parameters']['by_type'].values()) if status['parameters']['by_type'] else 1
            for ptype, count in sorted(status['parameters']['by_type'].items(), 
                                       key=lambda x: x[1], reverse=True):
                bar = "#" * int(count / max_count * 30)
                print(f"  {ptype:20} {count:6} {bar}")
            print(f"{'='*60}\n")
    
    def do_vocab(self, arg: str):
        """Mostra informacoes do vocabulario: /vocab [count]"""
        vocab_size = self.brx.param_generator.get_vocabulary_size()
        stats = self.brx.param_generator.get_stats()
        
        print(f"\n{'='*60}")
        print("VOCABULARIO DO BRX")
        print(f"{'='*60}")
        print(f"\nTotal de palavras: {vocab_size}")
        
        print("\nEstatisticas de geracao:")
        for stat, count in sorted(stats.items()):
            print(f"  {stat:20}: {count}")
        
        if arg:
            try:
                count = int(arg)
                words = list(self.brx.param_generator.vocabulary)[:count]
                print(f"\nPrimeiras {count} palavras:")
                print(", ".join(words))
            except ValueError:
                pass
        
        print(f"{'='*60}\n")
    
    def do_search(self, arg: str):
        """Realiza pesquisa web: /search <consulta>"""
        if not arg:
            print("[BRX] Uso: /search <consulta>")
            return
        
        print(f"\n[BRX] Pesquisando: '{arg}'...")
        
        results = self.brx.searcher.search(arg, max_results=5)
        
        if results:
            print(f"\n{'='*60}")
            print(f"RESULTADOS PARA: '{arg}'")
            print(f"{'='*60}")
            
            for i, result in enumerate(results, 1):
                print(f"\n[{i}] {result.title}")
                print(f"    URL: {result.url}")
                print(f"    {result.snippet}")
                print(f"    Relevancia: {result.relevance:.1%}")
            
            print(f"\n{'='*60}\n")
        else:
            print("[BRX] Nenhum resultado encontrado.")
    
    def do_evolve(self, arg: str):
        """Forca um ciclo de evolucao: /evolve"""
        print("\n[BRX] Iniciando ciclo de evolucao...")
        
        try:
            cycle = self.brx.run_evolution_cycle()
            
            print(f"\n{'='*60}")
            print(f"CICLO DE EVOLUCAO #{cycle.cycle_number} COMPLETADO")
            print(f"{'='*60}")
            print(f"\nNovos parametros: {len(cycle.new_parameters)}")
            print(f"Melhorias aplicadas: {len(cycle.improved_parameters)}")
            print(f"Insights: {len(cycle.learning_insights)}")
            
            if cycle.learning_insights:
                print("\nInsights:")
                for insight in cycle.learning_insights:
                    print(f"   {insight}")
            
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"[BRX] Erro na evolucao: {e}")
    
    def do_save(self, arg: str):
        """Salva estado atual do BRX: /save"""
        print("[BRX] Salvando estado...")
        self.brx.save_state()
        self.brx.consciousness.save_consciousness()
        print("[BRX] Estado salvo com sucesso")
    
    def do_clear(self, arg: str):
        """Limpa a tela: /clear"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(self.intro)
    
    def do_help(self, arg: str):
        """Mostra ajuda: /help [comando]"""
        if arg:
            help_texts = {
                'status': 'Mostra status completo do sistema',
                'identity': 'Mostra declaracao de identidade do BRX',
                'minds': 'Lista as 8 mentes base ativas',
                'agents': 'Lista todos os agentes especializados (/agents [categoria])',
                'agent': 'Mostra detalhes de um agente (/agent <id>)',
                'categories': 'Mostra categorias de agentes',
                'analyze': 'Analisa uma tarefa sem executar (/analyze <texto>)',
                'task': 'Processa tarefa com multi-agente (/task <texto>)',
                'multiagent': 'Ativa/desativa modo multi-agente (/multiagent [on|off|status])',
                'maxagents': 'Define numero maximo de agentes (/maxagents <n>)',
                'workspace': 'Mostra workspace colaborativo',
                'params': 'Mostra estatisticas de parametros (/params [tipo])',
                'vocab': 'Mostra informacoes do vocabulario (/vocab [count])',
                'search': 'Realiza pesquisa web (/search <consulta>)',
                'evolve': 'Forca um ciclo de evolucao',
                'save': 'Salva estado atual no HD',
                'clear': 'Limpa a tela',
                'quit': 'Encerra o chat'
            }
            
            if arg in help_texts:
                print(f"\n[BRX] /{arg}: {help_texts[arg]}\n")
            else:
                print(f"[BRX] Comando desconhecido: /{arg}")
        else:
            print(f"""
{'='*60}
COMANDOS DISPONIVEIS - BRX v3.0
{'='*60}

SISTEMA:
  /status         - Status completo do sistema
  /identity       - Declaracao de identidade do BRX
  /save           - Salva estado atual
  /clear          - Limpa a tela
  /quit           - Encerra o chat

MENTES BASE (8):
  /minds          - Lista as 8 mentes base ativas

MULTI-AGENTE (100+ agentes):
  /agents         - Lista todos os agentes especializados
  /agents <cat>   - Filtra agentes por categoria
  /agent <id>     - Detalhes de um agente especifico
  /categories     - Mostra categorias disponiveis
  /analyze <text> - Analisa tarefa sem executar
  /task <text>    - Processa tarefa com equipe especializada
  /multiagent on  - Ativa modo multi-agente
  /multiagent off - Desativa modo multi-agente
  /maxagents <n>  - Define max agentes (1-16, padrao: 8)
  /workspace      - Mostra workspace colaborativo

DADOS:
  /params         - Estatisticas de parametros
  /vocab          - Informacoes do vocabulario
  /search         - Pesquisa web
  /evolve         - Ciclo de evolucao

{'='*60}
Para conversar, digite sua mensagem normalmente.
O BRX ativara agentes especializados automaticamente!
{'='*60}
            """)
    
    def do_quit(self, arg: str):
        """Encerra o chat: /quit"""
        print("\n[BRX] Salvando estado...")
        self.brx.save_state()
        self.brx.consciousness.save_consciousness()
        
        print("""
                                                                              
                    OBRIGADO POR CONVERSAR COM O BRX v3.0!                     
                                                                              
                    Sistema Multi-Agente desligado.                             
                    Continue evoluindo. Ate breve.                              
                                                                              
        """)
        return True
    
    def do_EOF(self, arg: str):
        """Handler para Ctrl+D"""
        return self.do_quit(arg)
    
    def emptyline(self):
        """Ignora linhas vazias"""
        pass
    
    def preloop(self):
        """Executado antes do loop principal"""
        print(self.intro)


def main():
    """Funcao principal"""
    parser = argparse.ArgumentParser(
        description="BRX-Agent v3.0 - Interface de Chat com Multi-Agente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
    # Modo padrao (8 agentes)
    python brx_chat_v3.py
    
    # Com 4 agentes
    python brx_chat_v3.py --max-agents 4
    
    # Com 12 agentes
    python brx_chat_v3.py --max-agents 12
    
    # Com storage externo
    python brx_chat_v3.py --storage "/media/dragonscp/modelo BRX"
        """
    )
    
    parser.add_argument(
        "--storage",
        type=str,
        default="./storage",
        help="Diretorio para armazenamento de dados (padrao: ./storage)"
    )
    
    parser.add_argument(
        "--max-agents",
        type=int,
        default=None,
        help="Numero maximo de agentes simultaneos (padrao: auto-detectado)"
    )
    
    args = parser.parse_args()
    
    try:
        chat = BRXChat(storage_path=args.storage, max_agents=args.max_agents)
        chat.cmdloop()
    except KeyboardInterrupt:
        print("\n\n[BRX] Encerrado pelo usuario")
    except Exception as e:
        print(f"\n[BRX] Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
