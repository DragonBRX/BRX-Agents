#!/usr/bin/env python3
"""
BRX-AGENT v2.0 - Interface de Chat
==================================
Arquivo para conversar interativamente com o BRX.
Use este arquivo quando quiser interagir diretamente com o agente.

O BRX irá:
- Processar suas solicitações usando seu sistema de 8 mentes
- Realizar debates internos para alcançar o melhor consenso
- Gerar parâmetros relevantes para a conversa
- Pesquisar informações na web quando necessário
- Aprender com cada interação

Uso:
    python brx_chat.py [--storage PATH]

Comandos disponíveis no chat:
    /status     - Mostra status do sistema
    /identity   - Mostra declaração de identidade do BRX
    /minds      - Lista as mentes ativas
    /params     - Mostra estatísticas de parâmetros
    /vocab      - Mostra tamanho do vocabulário
    /search     - Realiza pesquisa web
    /evolve     - Força um ciclo de evolução
    /save       - Salva estado atual
    /clear      - Limpa a tela
    /help       - Mostra esta ajuda
    /quit       - Encerra o chat
"""

import os
import sys
import cmd
import argparse
from pathlib import Path
from typing import List, Optional

# Adiciona diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.brx_engine import BRXCore, get_brx_core


class BRXChat(cmd.Cmd):
    """
    Interface interativa de chat com o BRX
    """
    
    intro = """

                                                                              
                            
                     
                                
                                
                                
                                   
                                                                              
                    INTERFACE DE CONVERSAÇÃO                                  
                         Versão 2.0.0                                         

  Digite sua mensagem para conversar com o BRX.                               
  Use /help para ver os comandos disponíveis.                                 
  Use /quit para sair.                                                        

    """
    
    prompt = "\n[BRX] Você: "
    ruler = "="
    
    def __init__(self, storage_path: str = "./storage"):
        super().__init__()
        self.storage_path = Path(storage_path)
        
        print("[BRX Chat] Inicializando núcleo...")
        self.brx = get_brx_core(str(self.storage_path))
        self.brx.load_state()
        
        print("[BRX Chat]  Sistema pronto para conversação\n")
    
    def default(self, line: str):
        """Processa mensagens do usuário"""
        if not line.strip():
            return
        
        # Verifica se é comando
        if line.startswith('/'):
            # Remove a barra e processa como comando
            cmd_parts = line[1:].split()
            if cmd_parts:
                cmd_name = cmd_parts[0]
                cmd_args = cmd_parts[1:] if len(cmd_parts) > 1 else []
                
                # Mapeia comandos
                command_map = {
                    'status': self.do_status,
                    'identity': self.do_identity,
                    'minds': self.do_minds,
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
                    print("[BRX] Use /help para ver comandos disponíveis")
            return
        
        # Processa como mensagem normal
        self._process_message(line)
    
    def _process_message(self, message: str):
        """Processa mensagem do usuário através do BRX"""
        print(f"\n[BRX] Processando...")
        
        try:
            result = self.brx.process_request(message)
            
            # Mostra resposta
            print(f"\n{'='*60}")
            print("[BRX] Resposta:")
            print(f"{'='*60}")
            print(result['consensus'])
            
            # Mostra informações adicionais
            print(f"\n{'-'*60}")
            print(f"Confiança: {result['confidence']:.1%} | "
                  f"Parâmetros: {result['parameters_generated']} | "
                  f"Duração: {result['duration']:.2f}s")
            
            # Mostra resultados de pesquisa se houver
            if result['search_results']:
                print(f"\n[BRX] Pesquisas relacionadas:")
                for i, sr in enumerate(result['search_results'][:3], 1):
                    print(f"  {i}. {sr.title}")
                    print(f"     {sr.snippet[:80]}...")
            
            print(f"{'='*60}")
            
        except Exception as e:
            print(f"[BRX] Erro ao processar: {e}")
    
    def do_status(self, arg: str):
        """Mostra status completo do sistema: /status"""
        status = self.brx.get_status()
        
        print(f"\n{'='*60}")
        print("STATUS DO BRX")
        print(f"{'='*60}")
        
        print(f"\n[Identidade]")
        print(f"  Nome: {status['consciousness']['name']}")
        print(f"  Versão: {status['state']['version']}")
        print(f"  Ciclo atual: {status['state']['cycle']}")
        
        print(f"\n[Consciência]")
        print(f"  Curiosidade: {status['consciousness']['curiosity']:.1%}")
        print(f"  Confiança: {status['consciousness']['confidence']:.1%}")
        print(f"  Momentum: {status['consciousness']['learning_momentum']:.1%}")
        
        print(f"\n[Sistema de Mentes]")
        print(f"  Mentes ativas: {status['minds']['active']}/{status['minds']['total']}")
        print(f"  Debates realizados: {status['state']['debates_count']}")
        
        print(f"\n[Parâmetros]")
        print(f"  Total: {status['parameters']['total']}")
        print("  Por tipo:")
        for ptype, count in sorted(status['parameters']['by_type'].items()):
            print(f"    - {ptype}: {count}")
        
        print(f"\n[Vocabulário]")
        print(f"  Palavras: {status['vocabulary']['size']}")
        print(f"  Estatísticas:")
        for stat, count in sorted(status['vocabulary']['stats'].items()):
            print(f"    - {stat}: {count}")
        
        print(f"\n[Memória]")
        print(f"  Total: {status['memory']['total']}")
        print(f"  Curto prazo: {status['memory']['short']}")
        print(f"  Médio prazo: {status['memory']['medium']}")
        print(f"  Longo prazo: {status['memory']['long']}")
        
        print(f"\n[Pesquisas]")
        print(f"  Realizadas: {status['state']['searches_count']}")
        
        print(f"{'='*60}\n")
    
    def do_identity(self, arg: str):
        """Mostra declaração de identidade do BRX: /identity"""
        print(self.brx.generate_identity())
    
    def do_minds(self, arg: str):
        """Lista as mentes ativas do BRX: /minds"""
        minds = self.brx.minds.get_active_minds()
        
        print(f"\n{'='*60}")
        print("SISTEMA DE 8 MENTES")
        print(f"{'='*60}")
        
        for i, mind in enumerate(minds, 1):
            print(f"\n[{i}] {mind.state.name}")
            print(f"    Especialidade: {mind.state.specialty}")
            print(f"    Objetivo: {mind.state.objective}")
            print(f"    Peso: {mind.state.weight} | Confiança: {mind.state.confidence:.2f}")
            print(f"    Contribuições: {mind.state.contribution_count}")
        
        print(f"\n{'='*60}\n")
    
    def do_params(self, arg: str):
        """Mostra estatísticas de parâmetros: /params [tipo]"""
        status = self.brx.get_status()
        
        if arg:
            # Filtra por tipo
            ptype = arg.lower()
            count = status['parameters']['by_type'].get(ptype, 0)
            print(f"\n[BRX] Parâmetros do tipo '{ptype}': {count}")
        else:
            print(f"\n{'='*60}")
            print("PARÂMETROS DO BRX")
            print(f"{'='*60}")
            print(f"\nTotal: {status['parameters']['total']}")
            print("\nPor tipo:")
            for ptype, count in sorted(status['parameters']['by_type'].items(), 
                                       key=lambda x: x[1], reverse=True):
                bar = "" * int(count / max(status['parameters']['by_type'].values(), 1) * 30)
                print(f"  {ptype:15} {count:6} {bar}")
            print(f"{'='*60}\n")
    
    def do_vocab(self, arg: str):
        """Mostra informações do vocabulário: /vocab [count]"""
        vocab_size = self.brx.param_generator.get_vocabulary_size()
        stats = self.brx.param_generator.get_stats()
        
        print(f"\n{'='*60}")
        print("VOCABULÁRIO DO BRX")
        print(f"{'='*60}")
        print(f"\nTotal de palavras: {vocab_size}")
        
        print("\nEstatísticas de geração:")
        for stat, count in sorted(stats.items()):
            print(f"  {stat:15}: {count}")
        
        # Mostra algumas palavras se solicitado
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
                print(f"    Relevância: {result.relevance:.1%}")
            
            print(f"\n{'='*60}\n")
        else:
            print("[BRX] Nenhum resultado encontrado.")
    
    def do_evolve(self, arg: str):
        """Força um ciclo de evolução: /evolve"""
        print("\n[BRX] Iniciando ciclo de evolução...")
        
        try:
            cycle = self.brx.run_evolution_cycle()
            
            print(f"\n{'='*60}")
            print(f"CICLO DE EVOLUÇÃO #{cycle.cycle_number} COMPLETADO")
            print(f"{'='*60}")
            print(f"\nNovos parâmetros: {len(cycle.new_parameters)}")
            print(f"Melhorias aplicadas: {len(cycle.improved_parameters)}")
            print(f"Insights: {len(cycle.learning_insights)}")
            
            if cycle.learning_insights:
                print("\nInsights:")
                for insight in cycle.learning_insights:
                    print(f"   {insight}")
            
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"[BRX] Erro na evolução: {e}")
    
    def do_save(self, arg: str):
        """Salva estado atual do BRX: /save"""
        print("[BRX] Salvando estado...")
        self.brx.save_state()
        self.brx.consciousness.save_consciousness()
        print("[BRX]  Estado salvo com sucesso")
    
    def do_clear(self, arg: str):
        """Limpa a tela: /clear"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(self.intro)
    
    def do_help(self, arg: str):
        """Mostra ajuda: /help [comando]"""
        if arg:
            # Ajuda específica
            help_texts = {
                'status': 'Mostra status completo do sistema',
                'identity': 'Mostra declaração de identidade do BRX',
                'minds': 'Lista as 8 mentes e suas especialidades',
                'params': 'Mostra estatísticas de parâmetros (/params [tipo])',
                'vocab': 'Mostra informações do vocabulário (/vocab [count])',
                'search': 'Realiza pesquisa web (/search <consulta>)',
                'evolve': 'Força um ciclo de evolução do sistema',
                'save': 'Salva estado atual no HD',
                'clear': 'Limpa a tela',
                'quit': 'Encerra o chat'
            }
            
            if arg in help_texts:
                print(f"\n[BRX] /{arg}: {help_texts[arg]}\n")
            else:
                print(f"[BRX] Comando desconhecido: /{arg}")
        else:
            # Ajuda geral
            print(f"""
{'='*60}
COMANDOS DISPONÍVEIS
{'='*60}

  /status     - Mostra status completo do sistema
  /identity   - Mostra declaração de identidade do BRX
  /minds      - Lista as mentes ativas e suas especialidades
  /params     - Mostra estatísticas de parâmetros (/params [tipo])
  /vocab      - Mostra informações do vocabulário (/vocab [count])
  /search     - Realiza pesquisa web (/search <consulta>)
  /evolve     - Força um ciclo de evolução do sistema
  /save       - Salva estado atual no HD
  /clear      - Limpa a tela
  /help       - Mostra esta ajuda (/help [comando])
  /quit       - Encerra o chat

{'='*60}
Para conversar, digite sua mensagem normalmente.
O BRX irá processar usando seu sistema de 8 mentes.
{'='*60}
            """)
    
    def do_quit(self, arg: str):
        """Encerra o chat: /quit"""
        print("\n[BRX] Salvando estado...")
        self.brx.save_state()
        self.brx.consciousness.save_consciousness()
        
        print("""

                                                                              
                    OBRIGADO POR CONVERSAR COM O BRX!                         
                                                                              
                    Continue evoluindo. Até breve.                            
                                                                              

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
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="BRX-Agent v2.0 - Interface de Chat",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--storage",
        type=str,
        default="./storage",
        help="Diretório para armazenamento de dados (padrão: ./storage)"
    )
    
    args = parser.parse_args()
    
    try:
        chat = BRXChat(storage_path=args.storage)
        chat.cmdloop()
    except KeyboardInterrupt:
        print("\n\n[BRX] Encerrado pelo usuário")
    except Exception as e:
        print(f"\n[BRX] Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
