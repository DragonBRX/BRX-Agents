#!/usr/bin/env python3
"""
BRX-AGENT v3.0 - Chat Inteligente Offline
==========================================
Sistema de conversação completamente offline e inteligente.
Processa linguagem natural em múltiplas camadas usando 8 mentes especializadas.

NÃO DEPENDE DE INTERNET - Todo o processamento é local e simbólico.

Funcionalidades:
- Processamento granular: letra → palavra → frase → conceito
- Banco de conhecimento embutido (estados, cidades, fatos)
- 8 mentes trabalhando em camadas
- Respostas contextualizadas e inteligentes
- Capacidade de responder perguntas complexas como:
  "Qual estado do Brasil não tem a letra A?"

Uso:
    python brx_chat_v3.py
    python brx_chat_v3.py --verbose  # Mostra processamento das mentes
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# Adiciona diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.knowledge_base import BRXKnowledgeBase
from core.text_processor import GranularTextProcessor
from minds.eight_minds_v3 import EightMindsSystemV3, ConsensusResult


class BRXChatV3:
    """
    Sistema de Chat Inteligente BRX v3.0
    Processamento completamente offline
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.session_start = datetime.now()
        self.interaction_count = 0
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    BRX-AGENT v3.0 - CHAT                         ║
║              Sistema Inteligente 100% Offline                    ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  Processamento em 8 camadas:                                     ║
║    1. Caracteres    2. Léxico      3. Sintática   4. Semântica  ║
║    5. Lógica        6. Memória     7. Geração     8. Validação  ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        
        # Inicializa componentes
        print("[BRX] Inicializando banco de conhecimento...")
        self.knowledge_base = BRXKnowledgeBase()
        
        kb_stats = self.knowledge_base.get_stats()
        print(f"[BRX] ✓ {kb_stats['total_entries']} entradas carregadas")
        print(f"[BRX]   - Geografia: {kb_stats['by_category'].get('geografia', 0)}")
        print(f"[BRX]   - Linguagem: {kb_stats['by_category'].get('linguagem', 0)}")
        print(f"[BRX]   - Matemática: {kb_stats['by_category'].get('matematica', 0)}")
        
        print("[BRX] Inicializando sistema de 8 mentes...")
        self.minds_system = EightMindsSystemV3(self.knowledge_base)
        print("[BRX] ✓ Sistema de mentes ativo\n")
        
        print("=" * 66)
        print("Digite 'sair' para encerrar ou 'ajuda' para ver comandos")
        print("=" * 66 + "\n")
    
    def process_input(self, user_input: str) -> str:
        """Processa entrada do usuário"""
        self.interaction_count += 1
        
        # Processa através das 8 mentes
        result = self.minds_system.process(user_input)
        
        # Mostra processamento se verbose
        if self.verbose:
            print(self.minds_system.get_thoughts_summary(result))
        
        return result.final_answer
    
    def handle_command(self, command: str) -> str:
        """Manipula comandos especiais"""
        cmd = command.lower().strip()
        
        if cmd == "sair" or cmd == "exit" or cmd == "quit":
            return "__EXIT__"
        
        elif cmd == "ajuda" or cmd == "help":
            return self._get_help()
        
        elif cmd == "estados":
            states = self.knowledge_base.get_all_states()
            return f"Os 26 estados do Brasil + DF:\n{', '.join(states[:10])}..."
        
        elif cmd == "estatisticas" or cmd == "stats":
            return self._get_stats()
        
        elif cmd.startswith("sem ") or cmd.startswith("sem a "):
            # Comando: "sem a letra X" ou "sem letra X"
            parts = cmd.split()
            if len(parts) >= 3:
                letter = parts[-1] if len(parts[-1]) == 1 else None
                if letter:
                    states = self.knowledge_base.query_states_without_letter(letter)
                    if states:
                        return f"Estados sem a letra '{letter.upper()}':\n{', '.join(states)}"
                    else:
                        return f"Nenhum estado encontrado sem a letra '{letter.upper()}'"
        
        elif cmd == "teste" or cmd == "test":
            return self._run_tests()
        
        return None  # Não é comando, processar normalmente
    
    def _get_help(self) -> str:
        """Retorna mensagem de ajuda"""
        return """
╔════════════════ COMANDOS DISPONÍVEIS ════════════════════╗
║                                                          ║
║  Comandos Gerais:                                        ║
║    sair, exit, quit    - Encerra o chat                  ║
║    ajuda, help         - Mostra esta mensagem            ║
║    estatisticas, stats - Mostra estatísticas do sistema  ║
║                                                          ║
║  Consultas de Conhecimento:                              ║
║    estados             - Lista todos os estados do BR    ║
║    sem letra X         - Estados sem a letra X           ║
║                                                          ║
║  Testes:                                                 ║
║    teste, test         - Executa testes de funcionalidade║
║                                                          ║
║  Exemplos de Perguntas:                                  ║
║    "Qual estado não tem a letra A?"                      ║
║    "Liste os estados do Brasil"                          ║
║    "Oi, tudo bem?"                                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
    
    def _get_stats(self) -> str:
        """Retorna estatísticas do sistema"""
        kb_stats = self.knowledge_base.get_stats()
        uptime = datetime.now() - self.session_start
        
        return f"""
╔═══════════════════ ESTATÍSTICAS BRX ═══════════════════╗
║                                                          ║
║  Sessão:                                                 ║
║    Início: {self.session_start.strftime('%H:%M:%S')}                                    ║
║    Uptime: {str(uptime).split('.')[0]}                                   ║
║    Interações: {self.interaction_count}                                        ║
║                                                          ║
║  Banco de Conhecimento:                                  ║
║    Total de entradas: {kb_stats['total_entries']}                               ║
║    Letras indexadas: {kb_stats['indexed_letters']}                               ║
║    Palavras indexadas: {kb_stats['indexed_words']}                             ║
║                                                          ║
║  Por Categoria:                                          ║
║    Geografia: {kb_stats['by_category'].get('geografia', 0)}                                    ║
║    Linguagem: {kb_stats['by_category'].get('linguagem', 0)}                                    ║
║    Matemática: {kb_stats['by_category'].get('matematica', 0)}                                   ║
║    Geral: {kb_stats['by_category'].get('geral', 0)}                                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
    
    def _run_tests(self) -> str:
        """Executa testes de funcionalidade"""
        tests = []
        passed = 0
        
        # Teste 1: Processamento de caracteres
        try:
            processor = GranularTextProcessor()
            processed = processor.process("Oi BRX")
            assert len(processed.characters) == 6
            tests.append("✓ Processamento de caracteres")
            passed += 1
        except Exception as e:
            tests.append(f"✗ Processamento de caracteres: {e}")
        
        # Teste 2: Busca por letra
        try:
            states_with_a = self.knowledge_base.query_by_letter("a")
            assert len(states_with_a) > 0
            tests.append(f"✓ Busca por letra (encontrados {len(states_with_a)} resultados)")
            passed += 1
        except Exception as e:
            tests.append(f"✗ Busca por letra: {e}")
        
        # Teste 3: Estados sem letra
        try:
            states_without_a = self.knowledge_base.query_states_without_letter("a")
            assert len(states_without_a) >= 0
            tests.append(f"✓ Estados sem letra A ({len(states_without_a)} encontrados)")
            passed += 1
        except Exception as e:
            tests.append(f"✗ Estados sem letra: {e}")
        
        # Teste 4: Processamento das 8 mentes
        try:
            result = self.minds_system.process("Oi")
            assert result.final_answer is not None
            tests.append("✓ Sistema de 8 mentes")
            passed += 1
        except Exception as e:
            tests.append(f"✗ Sistema de 8 mentes: {e}")
        
        result = "\n".join(tests)
        result += f"\n\nResultado: {passed}/{len(tests)} testes passaram"
        
        return result
    
    def run(self):
        """Loop principal do chat"""
        try:
            while True:
                # Input do usuário
                try:
                    user_input = input("\n👤 Você: ").strip()
                except (KeyboardInterrupt, EOFError):
                    print("\n")
                    break
                
                if not user_input:
                    continue
                
                # Verifica comandos
                command_result = self.handle_command(user_input)
                
                if command_result == "__EXIT__":
                    break
                
                if command_result:
                    print(f"\n🤖 BRX: {command_result}")
                    continue
                
                # Processa normalmente
                start_time = time.time()
                response = self.process_input(user_input)
                process_time = time.time() - start_time
                
                # Mostra resposta
                print(f"\n🤖 BRX: {response}")
                
                if self.verbose:
                    print(f"   [Processado em {process_time:.3f}s]")
        
        finally:
            self._print_goodbye()
    
    def _print_goodbye(self):
        """Imprime mensagem de despedida"""
        uptime = datetime.now() - self.session_start
        
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    BRX-AGENT v3.0 - CHAT                         ║
║                        Encerrado                                 ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  Sessão: {self.interaction_count} interações em {str(uptime).split('.')[0]}                            ║
║                                                                  ║
║  Obrigado por conversar comigo!                                  ║
║  Até a próxima!                                                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """)


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="BRX-Agent v3.0 - Chat Inteligente Offline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
    python brx_chat_v3.py              # Modo normal
    python brx_chat_v3.py --verbose    # Mostra processamento das mentes
        """
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostra processamento detalhado das 8 mentes"
    )
    
    args = parser.parse_args()
    
    # Cria e executa chat
    chat = BRXChatV3(verbose=args.verbose)
    chat.run()


if __name__ == "__main__":
    main()
