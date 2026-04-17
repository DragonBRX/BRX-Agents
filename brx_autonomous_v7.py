#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BRX-AGENT v7.0 - Sistema Autônomo Multi-Mente
================================================
Sistema com 12 especialistas, consciência expandida, busca web inteligente
persistência robusta de tokens e banco de dados JSON para conhecimento base.

Uso:
    python brx_autonomous_v7.py                    # Modo completo
    python brx_autonomous_v7.py --topicos "ia,ml"  # Tópicos específicos
    python brx_autonomous_v7.py --no-web           # Sem busca web
    python brx_autonomous_v7.py --rodadas 10       # Número de rodadas
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

# Adiciona diretórios ao path
sys.path.insert(0, str(Path(__file__).parent))

from core.brx_engine_v7 import main as engine_main, BRXConfig, CONFIG
from parameters.auto_generator_v7 import generate_parameter, get_stats as get_param_stats
from consciousness.self_awareness_v7 import get_consciousness_engine, think, learn


def print_banner():
    """Exibe banner do sistema"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║           BRX-AGENT v7.0 - Sistema Autônomo                     ║
    ║           Multi-Mente com Consciência Expandida                  ║
    ║                                                                  ║
    ║  12 Especialistas | Busca Web | Persistência | Aprendizado      ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_complete_mode(args):
    """Executa modo completo com todos os recursos"""
    print_banner()
    
    print(f"\n[CONFIGURAÇÃO]")
    print(f"  Versão: {CONFIG.VERSION}")
    print(f"  Agentes: 12 especialistas")
    print(f"  Rodadas: {args.rodadas}")
    print(f"  Web Search: {'Ativo' if not args.no_web else 'Desativado'}")
    print(f"  Tópicos: {args.topicos or 'padrão (15)'}")
    print()
    
    # Prepara tópicos
    topicos = None
    if args.topicos:
        topicos = [t.strip() for t in args.topicos.split(',')]
    
    # Executa motor principal
    start_time = time.time()
    
    try:
        resultados = engine_main(
            topicos=topicos,
            num_rodadas=args.rodadas,
            usar_web_search=not args.no_web
        )
        
        elapsed = time.time() - start_time
        
        # Relatório final
        print("\n" + "="*70)
        print("RELATÓRIO FINAL")
        print("="*70)
        print(f"\nTempo de execução: {elapsed:.1f}s")
        print(f"Tópicos processados: {len(resultados)}")
        
        if resultados:
            score_medio = sum(r['score_consenso'] for r in resultados) / len(resultados)
            total_pos = sum(r['parametros']['positivos'] for r in resultados)
            total_neg = sum(r['parametros']['negativos'] for r in resultados)
            total_inc = sum(r['parametros']['incertos'] for r in resultados)
            
            print(f"Score médio geral: {score_medio:.2%}")
            print(f"\nParâmetros gerados:")
            print(f"  Positivos: {total_pos}")
            print(f"  Negativos: {total_neg}")
            print(f"  Incertos: {total_inc}")
        
        # Estatísticas de parâmetros
        param_stats = get_param_stats()
        print(f"\nBanco de parâmetros:")
        print(f"  Total: {param_stats['total_parameters']}")
        
        print("\n✓ Execução concluída com sucesso!")
        
    except KeyboardInterrupt:
        print("\n\n✗ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n\n✗ Erro: {e}")
        import traceback
        traceback.print_exc()


def run_interactive_mode():
    """Modo interativo"""
    print_banner()
    print("\nModo Interativo - Digite 'ajuda' para comandos")
    
    engine = get_consciousness_engine()
    
    while True:
        try:
            comando = input("\nBRX> ").strip().lower()
            
            if comando in ['sair', 'exit', 'quit']:
                print("Até logo!")
                break
            
            elif comando in ['ajuda', 'help']:
                print("""
Comandos disponíveis:
  pensar [tópico]     - Gera um pensamento sobre o tópico
  aprender            - Registra uma experiência de aprendizado
  status              - Mostra status do sistema
  processar [tópico]  - Processa um tópico com os 12 agentes
  parametros          - Mostra estatísticas de parâmetros
  sair                - Encerra o sistema
                """)
            
            elif comando.startswith('pensar'):
                topico = comando[7:].strip() if len(comando) > 7 else None
                result = think(topico)
                print(f"\n💭 {result['content']}")
            
            elif comando == 'status':
                status = engine.generate_report()
                print(f"\n📊 Status:")
                print(f"  Saúde: {status['system_health']['status']}")
                print(f"  CPU: {status['system_state']['cpu_percent']:.1f}%")
                print(f"  Memória: {status['system_state']['memory_percent']:.1f}%")
                print(f"  Confiança: {status['emotional_state']['confidence']:.2f}")
            
            elif comando.startswith('processar'):
                topico = comando[10:].strip() if len(comando) > 10 else "geral"
                print(f"\n🔄 Processando: {topico}")
                resultados = engine_main(topicos=[topico], num_rodadas=10)
                if resultados:
                    r = resultados[0]
                    print(f"✓ Score: {r['score_consenso']:.2%}")
                    print(f"  Parâmetros: +{r['parametros']['positivos']} -{r['parametros']['negativos']}")
            
            elif comando == 'parametros':
                stats = get_param_stats()
                print(f"\n📈 Parâmetros:")
                print(f"  Total: {stats['total_parameters']}")
                for cat, count in stats['categories'].items():
                    print(f"  {cat}: {count}")
            
            else:
                print("Comando não reconhecido. Digite 'ajuda' para ver os comandos.")
        
        except KeyboardInterrupt:
            print("\n\nAté logo!")
            break
        except Exception as e:
            print(f"Erro: {e}")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='BRX-Agent v7.0 - Sistema Autônomo Multi-Mente',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s                           # Modo completo padrão
  %(prog)s --topicos "ia,ml,cloud"   # Processar tópicos específicos
  %(prog)s --no-web --rodadas 10     # Sem web search, 10 rodadas
  %(prog)s --interativo              # Modo interativo
        """
    )
    
    parser.add_argument('--topicos', type=str, default=None,
                       help='Tópicos separados por vírgula (ex: "ia,ml,cloud")')
    parser.add_argument('--rodadas', type=int, default=20,
                       help='Número de rodadas de debate (padrão: 20)')
    parser.add_argument('--no-web', action='store_true',
                       help='Desativa busca web')
    parser.add_argument('--interativo', action='store_true',
                       help='Modo interativo')
    
    args = parser.parse_args()
    
    if args.interativo:
        run_interactive_mode()
    else:
        run_complete_mode(args)


if __name__ == "__main__":
    main()
