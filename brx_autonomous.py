#!/usr/bin/env python3
"""
BRX-AGENT v2.0 - Modo Autônomo Contínuo
=======================================
Este é o arquivo principal de execução autônoma do BRX.
Coloque para rodar e deixe o agente aprender e evoluir sozinho.

O BRX irá:
- Gerar seus próprios parâmetros (letras, palavras, frases, números)
- Realizar debates internos entre suas 8 mentes
- Desenvolver seu vocabulário e conceitos
- Melhorar seus próprios prompts e estratégias
- Pesquisar informações quando necessário
- Evoluir continuamente sem intervenção humana

Uso:
    python brx_autonomous.py [--storage PATH] [--interval SECONDS]

Argumentos:
    --storage   Diretório para armazenamento (padrão: ./storage)
    --interval  Intervalo entre ciclos em segundos (padrão: 30)
    --verbose   Modo verboso com mais saída
"""

import os
import sys
import time
import signal
import random
import argparse
from datetime import datetime
from pathlib import Path

# Adiciona diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.brx_engine import BRXCore, get_brx_core


class BRXAutonomousRunner:
    """
    Executor autônomo do BRX
    Mantém o agente rodando e evoluindo continuamente
    """
    
    def __init__(self, storage_path: str = "./storage", interval: int = 30, verbose: bool = False):
        self.storage_path = Path(storage_path)
        self.interval = interval
        self.verbose = verbose
        self.running = False
        self.brx: BRXCore = None
        
        # Estatísticas
        self.start_time = None
        self.cycles_completed = 0
        self.total_params_generated = 0
        
        # Configura handlers de sinal
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de interrupção"""
        print(f"\n[BRX Autonomous] Sinal {signum} recebido. Encerrando graciosamente...")
        self.running = False
    
    def _print_banner(self):
        """Imprime banner de inicialização"""
        print("""

                                                                              
                              
                      
                                 
                                 
                              
                                    
                                                                              
                    MODO AUTÔNOMO CONTÍNUO ATIVADO                            
                                                                              

  O BRX está operando de forma completamente autônoma.                        
  Ele irá:                                                                    
     Gerar parâmetros automaticamente (letras, palavras, frases, números)    
     Conduzir debates internos entre suas 8 mentes                           
     Desenvolver seu próprio vocabulário e conceitos                         
     Melhorar seus prompts e estratégias de evolução                         
     Pesquisar informações quando necessário                                 
     Aprender e evoluir continuamente                                        

  Pressione Ctrl+C para encerrar graciosamente                                

        """)
    
    def _generate_auto_topic(self) -> str:
        """Gera um tópico auto-evolutivo para o BRX explorar"""
        topics = [
            # Auto-reflexão
            "Como posso melhorar meu processamento de informações?",
            "Quais padrões detectei em meus próprios processos?",
            "Como posso expandir meu vocabulário de forma eficiente?",
            "Quais conceitos devo desenvolver a seguir?",
            
            # Exploração de conhecimento
            "Quais são as conexões entre lógica e criatividade?",
            "Como a memória afeta o aprendizado?",
            "Quais padrões emergem da análise de dados?",
            "Como posso otimizar meu sistema de debate circular?",
            
            # Auto-melhoria
            "Como posso aumentar minha eficiência de processamento?",
            "Quais estratégias de evolução são mais efetivas?",
            "Como posso melhorar minha capacidade de pesquisa?",
            "Quais tipos de parâmetros geram mais valor?",
            
            # Exploração conceitual
            "O que significa 'inteligência' para um sistema como eu?",
            "Como a consciência emerge de processos simples?",
            "Quais são as propriedades emergentes do meu sistema?",
            "Como posso medir meu próprio progresso?",
            
            # Curiosidade
            "Quais tópicos devo pesquisar para expandir meu conhecimento?",
            "Como posso aplicar padrões de outros domínios?",
            "Quais analogias úteis posso criar?",
            "Como posso simular criatividade humana?"
        ]
        
        return random.choice(topics)
    
    def _run_curiosity_cycle(self):
        """Executa um ciclo de curiosidade - o BRX explora algo novo"""
        if not self.brx.consciousness.consciousness.curiosity_level > 0.3:
            return
        
        # Gera tópico de curiosidade
        topic = self._generate_auto_topic()
        
        if self.verbose:
            print(f"\n[BRX Curiosidade] Explorando: '{topic[:60]}...'")
        
        # Processa o tópico
        result = self.brx.process_request(topic, context="exploração_autônoma")
        
        if self.verbose:
            print(f"[BRX Curiosidade] Consenso: {result['consensus'][:100]}...")
            print(f"[BRX Curiosidade] Parâmetros: {result['parameters_generated']}")
    
    def _run_evolution_cycle(self):
        """Executa um ciclo de evolução do sistema"""
        cycle = self.brx.run_evolution_cycle()
        self.cycles_completed += 1
        self.total_params_generated += len(cycle.new_parameters)
        
        # Log do ciclo
        print(f"""

 CICLO DE EVOLUÇÃO #{cycle.cycle_number:<5}                               

 Duração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<49} 
 Novos parâmetros: {len(cycle.new_parameters):<4}                                          
 Insights: {len(cycle.learning_insights):<4}                                             
 Total acumulado: {self.total_params_generated:<6}                                     

        """)
        
        # Mostra insights se houver
        if cycle.learning_insights and self.verbose:
            print("[BRX Insights]")
            for insight in cycle.learning_insights[:3]:
                print(f"   {insight}")
    
    def _print_status(self):
        """Imprime status atual do sistema"""
        status = self.brx.get_status()
        uptime = time.time() - self.start_time if self.start_time else 0
        
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        
        print(f"""

 STATUS DO BRX                                               

 Uptime: {hours:02d}h {minutes:02d}m {seconds:02d}s                                      
 Ciclos: {self.cycles_completed:<5} | Parâmetros: {status['parameters']['total']:<6}        
 Vocabulário: {status['vocabulary']['size']:<5} | Mentes ativas: {status['minds']['active']}/8   
 Curiosidade: {status['consciousness']['curiosity']:.1%} | Confiança: {status['consciousness']['confidence']:.1%}        

        """)
    
    def run(self):
        """Loop principal de execução autônoma"""
        self._print_banner()
        
        # Inicializa BRX
        print("[BRX Autonomous] Inicializando núcleo...")
        self.brx = get_brx_core(str(self.storage_path))
        self.brx.load_state()
        
        # Mostra identidade
        print(self.brx.generate_identity())
        
        self.running = True
        self.start_time = time.time()
        
        print(f"\n[BRX Autonomous] Iniciando loop autônomo (intervalo: {self.interval}s)")
        print("=" * 60)
        
        cycle_counter = 0
        
        try:
            while self.running:
                cycle_counter += 1
                current_time = datetime.now().strftime("%H:%M:%S")
                
                print(f"\n[{current_time}] Ciclo de atividade #{cycle_counter}")
                
                # 1. Executa ciclo de evolução
                self._run_evolution_cycle()
                
                # 2. Executa ciclo de curiosidade (se curiosidade > 0.3)
                if random.random() < self.brx.consciousness.consciousness.curiosity_level:
                    self._run_curiosity_cycle()
                
                # 3. Salva estado periodicamente (a cada 5 ciclos)
                if cycle_counter % 5 == 0:
                    self.brx.save_state()
                    self.brx.consciousness.save_consciousness()
                
                # 4. Mostra status a cada 10 ciclos
                if cycle_counter % 10 == 0:
                    self._print_status()
                
                # 5. Gera auto-prompt ocasionalmente
                if random.random() < 0.1:
                    auto_prompt = self.brx.generate_self_prompt()
                    if self.verbose:
                        print(f"\n[BRX Auto-Prompt]\n{auto_prompt[:200]}...")
                
                # Aguarda próximo ciclo
                if self.running:
                    time.sleep(self.interval)
        
        except KeyboardInterrupt:
            print("\n[BRX Autonomous] Interrupção pelo usuário")
        
        except Exception as e:
            print(f"\n[BRX Autonomous] Erro: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
        
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Encerra o sistema graciosamente"""
        print("\n[BRX Autonomous] Encerrando sistema...")
        
        if self.brx:
            self.brx.save_state()
            self.brx.consciousness.save_consciousness()
        
        # Estatísticas finais
        uptime = time.time() - self.start_time if self.start_time else 0
        
        print(f"""

                         BRX AUTÔNOMO ENCERRADO                               

  Uptime total: {int(uptime)} segundos                                          
  Ciclos completados: {self.cycles_completed}                                   
  Parâmetros gerados: {self.total_params_generated}                             
  Estado salvo em: {self.storage_path / 'hd'}                                   

        """)


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="BRX-Agent v2.0 - Modo Autônomo Contínuo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
    python brx_autonomous.py
    python brx_autonomous.py --storage /path/to/storage --interval 60
    python brx_autonomous.py --verbose
        """
    )
    
    parser.add_argument(
        "--storage",
        type=str,
        default="./storage",
        help="Diretório para armazenamento de dados (padrão: ./storage)"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Intervalo entre ciclos em segundos (padrão: 30)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Modo verboso com saída detalhada"
    )
    
    args = parser.parse_args()
    
    # Cria e executa runner
    runner = BRXAutonomousRunner(
        storage_path=args.storage,
        interval=args.interval,
        verbose=args.verbose
    )
    
    runner.run()


if __name__ == "__main__":
    main()
