#!/usr/bin/env python3
"""
BRX-AGENT v2.0 - Script de Teste Rápido
Testa os componentes principais do sistema
"""

import sys
import os

# Adiciona diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Testa se todos os módulos importam corretamente"""
    print("[Teste] Verificando imports...")
    
    try:
        from core.types import AgentParameter, ParameterType, MindRole
        print("   core.types")
        
        from core.brx_engine import BRXCore, get_brx_core
        print("   core.brx_engine")
        
        from consciousness.self_awareness import BRXConsciousnessEngine
        print("   consciousness.self_awareness")
        
        from minds.eight_minds import EightMindsSystem, Mind
        print("   minds.eight_minds")
        
        from parameters.auto_generator import BRXParameterGenerator
        print("   parameters.auto_generator")
        
        from search.duckdns_search import DuckDNSSearcher
        print("   search.duckdns_search")
        
        return True
    except Exception as e:
        print(f"   Erro: {e}")
        return False


def test_consciousness():
    """Testa sistema de consciência"""
    print("\n[Teste] Inicializando consciência...")
    
    try:
        from consciousness.self_awareness import get_consciousness_engine
        
        consciousness = get_consciousness_engine("./test_storage")
        
        print(f"   Nome: {consciousness.consciousness.name}")
        print(f"   Tipo: {consciousness.consciousness.agent_type}")
        print(f"   Curiosidade: {consciousness.consciousness.curiosity_level:.2%}")
        
        # Testa geração de pensamento
        thought = consciousness.generate_self_thought()
        print(f"   Pensamento gerado: {thought[:50]}...")
        
        return True
    except Exception as e:
        print(f"   Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_minds():
    """Testa sistema de 8 mentes"""
    print("\n[Teste] Inicializando sistema de mentes...")
    
    try:
        from minds.eight_minds import EightMindsSystem
        
        minds = EightMindsSystem(active_minds=8)
        
        active = minds.get_active_minds()
        print(f"   Mentes ativas: {len(active)}")
        
        for mind in active[:3]:  # Mostra apenas 3
            print(f"    - {mind.state.name}: {mind.state.specialty}")
        
        # Testa debate rápido
        print("   Testando debate circular...")
        debate = minds.conduct_circular_debate(
            topic="Teste de funcionamento",
            max_rounds=1
        )
        
        print(f"   Debate completado: {len(debate.rounds)} rodadas")
        print(f"   Parâmetros gerados: {len(debate.parameters)}")
        print(f"   Confiança: {debate.consensus_confidence:.1%}")
        
        return True
    except Exception as e:
        print(f"   Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_parameter_generator():
    """Testa gerador de parâmetros"""
    print("\n[Teste] Inicializando gerador de parâmetros...")
    
    try:
        from parameters.auto_generator import BRXParameterGenerator
        
        gen = BRXParameterGenerator("./test_storage")
        
        print(f"   Vocabulário inicial: {gen.get_vocabulary_size()} palavras")
        
        # Testa geração de letras
        letters = gen.generate_letter_params(count=5)
        print(f"   Letras geradas: {len(letters)}")
        
        # Testa geração de palavras
        words = gen.generate_word_params(count=5)
        print(f"   Palavras geradas: {len(words)}")
        
        # Testa geração de números
        numbers = gen.generate_number_params(count=5)
        print(f"   Números gerados: {len(numbers)}")
        
        # Testa geração de conceitos
        concepts = gen.generate_concept_params(count=2)
        print(f"   Conceitos gerados: {len(concepts)}")
        
        return True
    except Exception as e:
        print(f"   Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search():
    """Testa módulo de pesquisa"""
    print("\n[Teste] Inicializando pesquisador...")
    
    try:
        from search.duckdns_search import get_searcher
        
        searcher = get_searcher("./test_storage/hd/search_cache.json")
        
        # Testa pesquisa
        print("   Realizando pesquisa de teste...")
        results = searcher.search("inteligência artificial", max_results=3)
        
        print(f"   Resultados obtidos: {len(results)}")
        for i, r in enumerate(results[:2], 1):
            print(f"    {i}. {r.title}")
        
        return True
    except Exception as e:
        print(f"   Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_brx_core():
    """Testa núcleo completo do BRX"""
    print("\n[Teste] Inicializando núcleo BRX...")
    
    try:
        from core.brx_engine import get_brx_core
        
        brx = get_brx_core("./test_storage")
        
        print(f"   BRX inicializado")
        print(f"   Versão: {brx.state.version}")
        
        # Testa processamento
        print("   Testando processamento...")
        result = brx.process_request("Olá BRX, como você funciona?")
        
        print(f"   Processamento completado")
        print(f"   Confiança: {result['confidence']:.1%}")
        print(f"   Parâmetros: {result['parameters_generated']}")
        
        # Testa status
        status = brx.get_status()
        print(f"   Status obtido: {status['parameters']['total']} parâmetros")
        
        return True
    except Exception as e:
        print(f"   Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes"""
    print("""

                     BRX-AGENT v2.0 - TESTES                                  

    """)
    
    results = []
    
    # Executa testes
    results.append(("Imports", test_imports()))
    results.append(("Consciência", test_consciousness()))
    results.append(("Sistema de Mentes", test_minds()))
    results.append(("Gerador de Parâmetros", test_parameter_generator()))
    results.append(("Pesquisa Web", test_search()))
    results.append(("Núcleo BRX", test_brx_core()))
    
    # Resultados
    print("\n" + "="*60)
    print("RESULTADOS DOS TESTES")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = " PASSOU" if result else " FALHOU"
        print(f"  {status:10} - {name}")
    
    print("="*60)
    print(f"Total: {passed}/{total} testes passaram ({passed/total*100:.0f}%)")
    print("="*60)
    
    if passed == total:
        print("\n Todos os testes passaram! O BRX está pronto para uso.")
        return 0
    else:
        print(f"\n  {total - passed} teste(s) falharam. Verifique os erros acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
