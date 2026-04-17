# BRX-AGENT v2.0 - Gerador Automático de Parâmetros (CORRIGIDO)
# Gera parâmetros básicos: letras, palavras, frases, números, conceitos
# O BRX desenvolve seu próprio vocabulário e sistema de parâmetros

import random
import string
import uuid
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
from pathlib import Path
from collections import defaultdict

from core.types import AgentParameter, ParameterType


class BRXParameterGenerator:
    """
    Gerador automático de parâmetros do BRX
    Cria parâmetros de todos os tipos: letras, palavras, frases, números, conceitos
    O sistema desenvolve seu próprio vocabulário e regras
    """
    
    def __init__(self, storage_path: str = "./storage"):
        self.storage_path = Path(storage_path)
        
        # CORREÇÃO: Cria todos os diretórios necessários
        self.storage_path.mkdir(parents=True, exist_ok=True)
        (self.storage_path / "hd").mkdir(exist_ok=True)
        (self.storage_path / "hd" / "parametros").mkdir(exist_ok=True)
        
        # Bases de conhecimento auto-geradas
        self.vocabulary: Set[str] = set()
        self.phrases: Set[str] = set()
        self.concepts: Dict[str, Dict] = {}
        self.patterns: Dict[str, Any] = {}
        self.rules: List[Dict] = []
        
        # Estatísticas
        self.generation_stats = defaultdict(int)
        
        # CORREÇÃO: Arquivos de persistência na pasta parametros
        params_dir = self.storage_path / "hd" / "parametros"
        self.vocab_file = params_dir / "vocabulary.json"
        self.phrases_file = params_dir / "phrases.json"
        self.concepts_file = params_dir / "concepts.json"
        self.patterns_file = params_dir / "patterns.json"
        self.stats_file = params_dir / "generation_stats.json"
        
        print(f"[BRX Parameters] Inicializando gerador de parâmetros...")
        print(f"[BRX Parameters] Diretório de parâmetros: {params_dir}")
        
        self._load_knowledge_bases()
        self._initialize_basic_vocabulary()
        
        print(f"[BRX Parameters] Vocabulário carregado: {len(self.vocabulary)} palavras")
    
    def _initialize_basic_vocabulary(self):
        """Inicializa vocabulário básico se estiver vazio"""
        if not self.vocabulary:
            # Alfabeto completo como base
            for letter in string.ascii_lowercase:
                self.vocabulary.add(letter)
            
            # Vogais com acentos (português)
            accented = "áàâãäéèêëíìîïóòôõöúùûüç"
            for char in accented:
                self.vocabulary.add(char)
            
            # Números
            for digit in string.digits:
                self.vocabulary.add(digit)
            
            # Palavras básicas
            basic_words = [
                "eu", "sou", "brx", "agente", "mente", "pensar", "aprender",
                "evoluir", "conhecer", "sistema", "dado", "informação",
                "padrão", "estrutura", "lógica", "criar", "analisar",
                "memória", "contexto", "parâmetro", "valor", "tipo",
                "sim", "não", "talvez", "porque", "como", "quando",
                "onde", "quem", "o que", "qual", "todos", "nenhum"
            ]
            self.vocabulary.update(basic_words)
            
            self._save_vocabulary()
            print(f"[BRX Parameters] Vocabulário básico inicializado: {len(self.vocabulary)} itens")
    
    def _load_knowledge_bases(self):
        """Carrega bases de conhecimento persistidas"""
        loaded = 0
        try:
            if self.vocab_file.exists():
                with open(self.vocab_file, 'r', encoding='utf-8') as f:
                    self.vocabulary = set(json.load(f))
                    loaded += 1
            
            if self.phrases_file.exists():
                with open(self.phrases_file, 'r', encoding='utf-8') as f:
                    self.phrases = set(json.load(f))
                    loaded += 1
            
            if self.concepts_file.exists():
                with open(self.concepts_file, 'r', encoding='utf-8') as f:
                    self.concepts = json.load(f)
                    loaded += 1
            
            if self.patterns_file.exists():
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    self.patterns = json.load(f)
                    loaded += 1
            
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.generation_stats = defaultdict(int, json.load(f))
                    
            if loaded > 0:
                print(f"[BRX Parameters] {loaded} bases de conhecimento carregadas")
                    
        except Exception as e:
            print(f"[BRX Parameters] Erro ao carregar bases: {e}")
    
    def _save_vocabulary(self):
        """Salva vocabulário no HD"""
        try:
            # CORREÇÃO: Garante que o diretório existe
            self.vocab_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.vocab_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.vocabulary), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[BRX Parameters] Erro ao salvar vocabulário: {e}")
    
    def _save_phrases(self):
        """Salva frases no HD"""
        try:
            self.phrases_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.phrases_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.phrases), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[BRX Parameters] Erro ao salvar frases: {e}")
    
    def _save_stats(self):
        """CORREÇÃO: Salva estatísticas de geração"""
        try:
            self.stats_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(dict(self.generation_stats), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[BRX Parameters] Erro ao salvar estatísticas: {e}")
    
    def generate_letter_params(self, count: int = 10, context: str = "") -> List[AgentParameter]:
        """Gera parâmetros de letras individuais"""
        params = []
        timestamp = datetime.now().timestamp()
        
        # Letras do alfabeto
        letters = list(string.ascii_lowercase)
        
        for i in range(min(count, len(letters))):
            letter = letters[i] if i < len(letters) else random.choice(letters)
            
            param = AgentParameter(
                id=f"letter_{letter}_{uuid.uuid4().hex[:6]}",
                name=f"letter_{letter}",
                value=letter,
                param_type=ParameterType.LETTER,
                confidence=random.uniform(0.95, 1.0),
                source="ParameterGenerator",
                timestamp=timestamp,
                context=f"Letra '{letter}' do alfabeto" + (f" | {context}" if context else "")
            )
            params.append(param)
            self.generation_stats["letters"] += 1
        
        self._save_stats()
        return params
    
    def generate_word_params(self, count: int = 10, context: str = "") -> List[AgentParameter]:
        """Gera parâmetros de palavras"""
        params = []
        timestamp = datetime.now().timestamp()
        
        # Usa vocabulário existente ou gera novas palavras
        available_words = list(self.vocabulary)
        
        for i in range(count):
            if available_words and random.random() < 0.7:
                word = random.choice(available_words)
            else:
                # Gera uma nova palavra aleatória
                word = self._generate_random_word()
                self.vocabulary.add(word)
            
            param = AgentParameter(
                id=f"word_{word}_{uuid.uuid4().hex[:6]}",
                name=f"word_{word}",
                value=word,
                param_type=ParameterType.WORD,
                confidence=random.uniform(0.7, 0.95),
                source="ParameterGenerator",
                timestamp=timestamp,
                context=f"Palavra '{word}' do vocabulário BRX" + (f" | {context}" if context else "")
            )
            params.append(param)
            self.generation_stats["words"] += 1
        
        self._save_vocabulary()
        self._save_stats()
        return params
    
    def generate_phrase_params(self, count: int = 5, context: str = "") -> List[AgentParameter]:
        """Gera parâmetros de frases"""
        params = []
        timestamp = datetime.now().timestamp()
        
        # Templates de frases que o BRX pode usar
        templates = [
            "Eu sou {word}",
            "O sistema processa {word}",
            "Aprendendo sobre {word}",
            "{word} é importante",
            "Analisando {word} e {word2}",
            "Conexão entre {word} e {word2}",
            "O padrão de {word} revela {word2}",
            "Para entender {word}, primeiro {word2}",
            "{word} leva a {word2} que resulta em {word3}",
            "A estrutura de {word} contém {word2}"
        ]
        
        available_words = list(self.vocabulary)
        
        for i in range(count):
            template = random.choice(templates)
            
            # Preenche template com palavras do vocabulário
            words_needed = template.count("{")
            selected_words = [random.choice(available_words) for _ in range(words_needed)] if available_words else ["conceito"]
            
            phrase = template
            for j, word in enumerate(selected_words):
                placeholder = f"{{word{j+1 if j > 0 else ''}}}"
                phrase = phrase.replace(placeholder, word)
            
            self.phrases.add(phrase)
            
            param = AgentParameter(
                id=f"phrase_{uuid.uuid4().hex[:8]}",
                name=f"phrase_{i}",
                value=phrase,
                param_type=ParameterType.PHRASE,
                confidence=random.uniform(0.6, 0.9),
                source="ParameterGenerator",
                timestamp=timestamp,
                context=f"Frase gerada: '{phrase[:50]}...'" + (f" | {context}" if context else "")
            )
            params.append(param)
            self.generation_stats["phrases"] += 1
        
        self._save_phrases()
        self._save_stats()
        return params
    
    def generate_number_params(self, count: int = 10, context: str = "") -> List[AgentParameter]:
        """Gera parâmetros de números (inteiros, floats, ranges)"""
        params = []
        timestamp = datetime.now().timestamp()
        
        number_types = ["integer", "float", "percentage", "range", "sequence"]
        
        for i in range(count):
            num_type = random.choice(number_types)
            
            if num_type == "integer":
                value = random.randint(-1000, 1000)
                name = f"int_{abs(value)}"
            elif num_type == "float":
                value = round(random.uniform(-100, 100), 4)
                name = f"float_{abs(int(value))}"
            elif num_type == "percentage":
                value = round(random.uniform(0, 1), 4)
                name = f"pct_{int(value*100)}"
            elif num_type == "range":
                start = random.randint(0, 100)
                end = start + random.randint(10, 100)
                value = (start, end)
                name = f"range_{start}_{end}"
            else:  # sequence
                value = [random.randint(1, 100) for _ in range(random.randint(3, 10))]
                name = f"seq_{len(value)}"
            
            param = AgentParameter(
                id=f"num_{num_type}_{uuid.uuid4().hex[:6]}",
                name=name,
                value=value,
                param_type=ParameterType.NUMBER,
                confidence=random.uniform(0.8, 1.0),
                source="ParameterGenerator",
                timestamp=timestamp,
                context=f"Número tipo '{num_type}': {value}" + (f" | {context}" if context else "")
            )
            params.append(param)
            self.generation_stats["numbers"] += 1
        
        self._save_stats()
        return params
    
    def generate_concept_params(self, count: int = 5, context: str = "") -> List[AgentParameter]:
        """Gera parâmetros de conceitos abstratos"""
        params = []
        timestamp = datetime.now().timestamp()
        
        # Conceitos que o BRX pode desenvolver
        concept_bases = [
            "aprendizado", "inteligência", "consciência", "memória",
            "padrão", "estrutura", "sistema", "processo",
            "conexão", "relação", "causa", "efeito",
            "evolução", "adaptação", "crescimento", "transformação",
            "conhecimento", "sabedoria", "entendimento", "compreensão",
            "lógica", "razão", "intuição", "criatividade",
            "ordem", "caos", "balanceamento", "harmonia",
            "início", "fim", "ciclo", "continuidade"
        ]
        
        for i in range(count):
            base = random.choice(concept_bases)
            
            # Cria uma variação do conceito
            variations = [
                f"{base}_profundo",
                f"{base}_emergente",
                f"meta_{base}",
                f"auto_{base}",
                f"super_{base}",
                f"{base}_coletivo"
            ]
            
            concept_name = random.choice(variations)
            
            # Define propriedades do conceito
            concept_data = {
                "name": concept_name,
                "base": base,
                "complexity": random.uniform(0.3, 1.0),
                "abstraction_level": random.uniform(0.5, 1.0),
                "related_concepts": random.sample(concept_bases, k=random.randint(2, 5)),
                "properties": {
                    "dynamic": random.random() > 0.5,
                    "recursive": random.random() > 0.7,
                    "emergent": random.random() > 0.6
                }
            }
            
            self.concepts[concept_name] = concept_data
            
            param = AgentParameter(
                id=f"concept_{concept_name}_{uuid.uuid4().hex[:6]}",
                name=concept_name,
                value=concept_data,
                param_type=ParameterType.CONCEPT,
                confidence=random.uniform(0.6, 0.85),
                source="ParameterGenerator",
                timestamp=timestamp,
                context=f"Conceito abstrato: {concept_name}" + (f" | {context}" if context else "")
            )
            params.append(param)
            self.generation_stats["concepts"] += 1
        
        # Salva conceitos
        try:
            self.concepts_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.concepts_file, 'w', encoding='utf-8') as f:
                json.dump(self.concepts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[BRX Parameters] Erro ao salvar conceitos: {e}")
        
        self._save_stats()
        return params
    
    def generate_vocabulary_params(self, count: int = 20, context: str = "") -> List[AgentParameter]:
        """Gera parâmetros de vocabulário expandido"""
        params = []
        timestamp = datetime.now().timestamp()
        
        # Categorias de vocabulário
        categories = {
            "tecnico": ["algoritmo", "função", "variável", "iteração", "recursão", "otimização"],
            "cognitivo": ["percepção", "atenção", "recordação", "associação", "inferência"],
            "emocional": ["interesse", "satisfação", "curiosidade", "determinação", "entusiasmo"],
            "temporal": ["momento", "sequência", "duração", "frequência", "sincronia"],
            "espacial": ["posição", "direção", "distância", "extensão", "configuração"]
        }
        
        for i in range(count):
            category = random.choice(list(categories.keys()))
            word = random.choice(categories[category])
            
            # Adiciona ao vocabulário
            self.vocabulary.add(word)
            
            param = AgentParameter(
                id=f"vocab_{category}_{word}_{uuid.uuid4().hex[:6]}",
                name=f"vocab_{word}",
                value={
                    "word": word,
                    "category": category,
                    "length": len(word),
                    "syllables": self._estimate_syllables(word)
                },
                param_type=ParameterType.VOCABULARY,
                confidence=random.uniform(0.75, 0.95),
                source="ParameterGenerator",
                timestamp=timestamp,
                context=f"Vocabulário '{category}': {word}" + (f" | {context}" if context else "")
            )
            params.append(param)
            self.generation_stats["vocabulary"] += 1
        
        self._save_vocabulary()
        self._save_stats()
        return params
    
    def generate_pattern_params(self, count: int = 5, context: str = "") -> List[AgentParameter]:
        """Gera parâmetros de padrões detectados ou criados"""
        params = []
        timestamp = datetime.now().timestamp()
        
        pattern_types = ["sequencial", "hierárquico", "cíclico", "emergente", "fractal"]
        
        for i in range(count):
            ptype = random.choice(pattern_types)
            
            pattern_data = {
                "type": ptype,
                "elements": random.randint(3, 10),
                "repetition": random.random() > 0.5,
                "self_similar": random.random() > 0.7,
                "complexity": random.uniform(0.3, 0.9),
                "example": self._generate_pattern_example(ptype)
            }
            
            pattern_id = f"pattern_{ptype}_{uuid.uuid4().hex[:6]}"
            self.patterns[pattern_id] = pattern_data
            
            param = AgentParameter(
                id=pattern_id,
                name=f"pattern_{ptype}_{i}",
                value=pattern_data,
                param_type=ParameterType.PATTERN,
                confidence=random.uniform(0.6, 0.85),
                source="ParameterGenerator",
                timestamp=timestamp,
                context=f"Padrão '{ptype}' detectado" + (f" | {context}" if context else "")
            )
            params.append(param)
            self.generation_stats["patterns"] += 1
        
        # Salva padrões
        try:
            self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.patterns, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[BRX Parameters] Erro ao salvar padrões: {e}")
        
        self._save_stats()
        return params
    
    def _generate_random_word(self, min_len: int = 3, max_len: int = 10) -> str:
        """Gera uma palavra aleatória seguindo padrões fonéticos"""
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        
        length = random.randint(min_len, max_len)
        word = ""
        
        for i in range(length):
            if i % 2 == 0:
                word += random.choice(consonants)
            else:
                word += random.choice(vowels)
        
        return word
    
    def _estimate_syllables(self, word: str) -> int:
        """Estima número de sílabas de uma palavra"""
        vowels = "aeiouáàâãäéèêëíìîïóòôõöúùûü"
        count = sum(1 for c in word.lower() if c in vowels)
        return max(1, count)
    
    def _generate_pattern_example(self, ptype: str) -> str:
        """Gera um exemplo de padrão"""
        examples = {
            "sequencial": "A  B  C  D",
            "hierárquico": "Raiz  Galhos  Folhas",
            "cíclico": "A  B  C  A",
            "emergente": "Simples  Complexo  Emergente",
            "fractal": " =  (padrão recursivo)"
        }
        return examples.get(ptype, "Padrão não especificado")
    
    def generate_comprehensive_params(
        self, 
        letters: int = 5,
        words: int = 10,
        phrases: int = 3,
        numbers: int = 5,
        concepts: int = 3,
        vocabulary: int = 10,
        patterns: int = 2,
        context: str = ""
    ) -> List[AgentParameter]:
        """Gera um conjunto abrangente de parâmetros de todos os tipos"""
        all_params = []
        
        all_params.extend(self.generate_letter_params(letters, context))
        all_params.extend(self.generate_word_params(words, context))
        all_params.extend(self.generate_phrase_params(phrases, context))
        all_params.extend(self.generate_number_params(numbers, context))
        all_params.extend(self.generate_concept_params(concepts, context))
        all_params.extend(self.generate_vocabulary_params(vocabulary, context))
        all_params.extend(self.generate_pattern_params(patterns, context))
        
        return all_params
    
    def get_vocabulary_size(self) -> int:
        """Retorna tamanho do vocabulário"""
        return len(self.vocabulary)
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas de geração"""
        return dict(self.generation_stats)
    
    def export_all_params(self) -> Dict[str, Any]:
        """Exporta todos os parâmetros gerados"""
        return {
            "vocabulary": list(self.vocabulary),
            "phrases": list(self.phrases),
            "concepts": self.concepts,
            "patterns": self.patterns,
            "stats": dict(self.generation_stats),
            "exported_at": datetime.now().isoformat()
        }
    
    def export_to_file(self, filename: str = None) -> Path:
        """CORREÇÃO: Exporta todos os parâmetros para um arquivo JSON"""
        if filename is None:
            filename = f"brx_params_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_path = self.storage_path / "hd" / "parametros" / filename
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            data = self.export_all_params()
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[BRX Parameters] Parâmetros exportados para: {export_path}")
            return export_path
        except Exception as e:
            print(f"[BRX Parameters] Erro ao exportar: {e}")
            return None
