#!/usr/bin/env python3
"""
BRX-AGENT v3.0 - Testes Completos
=================================
Testa todas as funcionalidades do sistema.

Uso:
    python test_v3.py
    python test_v3.py --verbose
"""

import sys
import time
from core.brx_engine_v3 import BRXCoreV3
from core.knowledge_base import BRXKnowledgeBase
from core.text_processor import GranularTextProcessor


def test_knowledge_base():
    """Testa o banco de conhecimento"""
    print("\n" + "=" * 60)
    print("TESTE 1: Banco de Conhecimento")
    print("=" * 60)
    
    kb = BRXKnowledgeBase()
    stats = kb.get_stats()
    
    print(f"✓ Total de entradas: {stats['total_entries']}")
    print(f"✓ Letras indexadas: {stats['indexed_letters']}")
    print(f"✓ Palavras indexadas: {stats['indexed_words']}")
    
    # Testa consulta por letra
    states_with_a = kb.query_by_letter("a")
    print(f"✓ Estados com letra 'A': {len(states_with_a)}")
    
    # Testa consulta sem letra
    states_without_a = kb.query_states_without_letter("a")
    print(f"✓ Estados SEM letra 'A': {len(states_without_a)}")
    
    if states_without_a:
        print(f"  Exemplos: {', '.join(states_without_a[:3])}")
    
    return True


def test_text_processor():
    """Testa o processador de texto"""
    print("\n" + "=" * 60)
    print("TESTE 2: Processador de Texto Granular")
    print("=" * 60)
    
    processor = GranularTextProcessor()
    
    test_texts = [
        "Oi BRX",
        "Qual estado não tem a letra A?",
        "Liste os estados do Brasil"
    ]
    
    for text in test_texts:
        print(f"\n📝 Texto: '{text}'")
        processed = processor.process(text)
        
        print(f"  ✓ {processed.char_count} caracteres")
        print(f"  ✓ {processed.word_count} palavras")
        print(f"  ✓ {processed.phrase_count} frases")
        print(f"  ✓ Letras únicas: {len(processed.letter_frequency)}")
    
    return True


def test_eight_minds():
    """Testa o sistema de 8 mentes"""
    print("\n" + "=" * 60)
    print("TESTE 3: Sistema de 8 Mentes")
    print("=" * 60)
    
    brx = BRXCoreV3(storage_path="./test_storage")
    
    test_inputs = [
        ("Oi", "Saudação"),
        ("Qual estado não tem a letra A?", "Pergunta com restrição"),
        ("Liste os estados do Brasil", "Comando de listagem"),
    ]
    
    for text, description in test_inputs:
        print(f"\n📝 {description}: '{text}'")
        
        start = time.time()
        result = brx.process(text)
        elapsed = time.time() - start
        
        print(f"  ✓ Resposta: {result['response'][:60]}...")
        print(f"  ✓ Confiança: {result['confidence']:.2f}")
        print(f"  ✓ Tempo: {elapsed:.3f}s")
        print(f"  ✓ Mentes processadas: {len(result['thoughts'])}")
    
    return True


def test_letter_constraints():
    """Testa restrições de letras"""
    print("\n" + "=" * 60)
    print("TESTE 4: Restrições de Letras")
    print("=" * 60)
    
    brx = BRXCoreV3(storage_path="./test_storage")
    
    letters = ["a", "e", "i", "o", "u"]
    
    for letter in letters:
        states = brx.query_without_letter(letter)
        print(f"✓ Estados sem '{letter.upper()}': {len(states)}")
        if states:
            print(f"  Exemplos: {', '.join(states[:5])}")
    
    return True


def test_demonstration():
    """Testa a demonstração de processamento"""
    print("\n" + "=" * 60)
    print("TESTE 5: Demonstração de Processamento")
    print("=" * 60)
    
    brx = BRXCoreV3(storage_path="./test_storage")
    
    demo_text = "Qual estado não tem a letra A?"
    print(f"\nTexto de demonstração: '{demo_text}'\n")
    
    demo = brx.demonstrate_processing(demo_text)
    print(demo)
    
    return True


def run_all_tests():
    """Executa todos os testes"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              BRX-AGENT v3.0 - TESTES AUTOMATIZADOS               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Banco de Conhecimento", test_knowledge_base),
        ("Processador de Texto", test_text_processor),
        ("Sistema de 8 Mentes", test_eight_minds),
        ("Restrições de Letras", test_letter_constraints),
        ("Demonstração", test_demonstration),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {name}: PASSOU")
            else:
                failed += 1
                print(f"\n❌ {name}: FALHOU")
        except Exception as e:
            failed += 1
            print(f"\n❌ {name}: ERRO - {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"✅ Passaram: {passed}/{len(tests)}")
    print(f"❌ Falharam: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
