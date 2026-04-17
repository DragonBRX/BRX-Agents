# BRX-AGENT v3.0 - Gerador de Parâmetros Expandido
# Gera parâmetros completos: letras, palavras, frases, conceitos, números

import random
import string
import uuid
import json
from datetime import datetime
from typing import List, Dict, Any, Set, Optional
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

class ParameterType(Enum):
    """Tipos de parâmetros gerados"""
    LETTER = "letra"
    DIGIT = "digito"
    SYMBOL = "simbolo"
    WORD = "palavra"
    PHRASE = "frase"
    NUMBER = "numero"
    CONCEPT = "conceito"
    PATTERN = "padrao"
    RULE = "regra"

@dataclass
class Parameter:
    """Representa um parâmetro gerado"""
    id: str
    name: str
    value: Any
    param_type: ParameterType
    confidence: float
    source: str
    timestamp: float
    context: str
    metadata: Dict = field(default_factory=dict)


class BRXParameterGeneratorV3:
    """
    Gerador de Parâmetros BRX v3.0
    Cria parâmetros de todos os tipos para processamento simbólico
    """
    
    def __init__(self, storage_path: str = "./storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Diretórios de parâmetros
        self.params_dir = self.storage_path / "hd" / "parametros"
        self.params_dir.mkdir(parents=True, exist_ok=True)
        
        # Bases de conhecimento
        self.letters: Dict[str, Dict] = {}
        self.digits: Dict[str, Dict] = {}
        self.symbols: Dict[str, Dict] = {}
        self.vocabulary: Set[str] = set()
        self.phrases: Set[str] = set()
        self.concepts: Dict[str, Dict] = {}
        self.patterns: Dict[str, Any] = {}
        
        # Estatísticas
        self.generation_count = 0
        
        # Inicializa
        self._initialize_all_parameters()
        
        print(f"[BRX Parameters] Gerador v3.0 inicializado")
        print(f"[BRX Parameters] {len(self.letters)} letras, {len(self.digits)} dígitos, {len(self.symbols)} símbolos")
    
    def _initialize_all_parameters(self):
        """Inicializa todos os parâmetros base"""
        self._initialize_letters()
        self._initialize_digits()
        self._initialize_symbols()
        self._initialize_vocabulary()
        self._save_all_parameters()
    
    def _initialize_letters(self):
        """Inicializa parâmetros de todas as letras"""
        # Alfabeto minúsculo
        for letter in string.ascii_lowercase:
            self.letters[letter] = {
                "char": letter,
                "upper": letter.upper(),
                "type": "vogal" if letter in "aeiou" else "consoante",
                "position": ord(letter) - ord('a') + 1,
                "phoneme": self._get_phoneme(letter),
            }
        
        # Vogais acentuadas
        accented_vowels = {
            'á': {'base': 'a', 'accent': 'agudo'},
            'à': {'base': 'a', 'accent': 'grave'},
            'â': {'base': 'a', 'accent': 'circunflexo'},
            'ã': {'base': 'a', 'accent': 'til'},
            'ä': {'base': 'a', 'accent': 'trema'},
            'é': {'base': 'e', 'accent': 'agudo'},
            'è': {'base': 'e', 'accent': 'grave'},
            'ê': {'base': 'e', 'accent': 'circunflexo'},
            'ë': {'base': 'e', 'accent': 'trema'},
            'í': {'base': 'i', 'accent': 'agudo'},
            'ì': {'base': 'i', 'accent': 'grave'},
            'î': {'base': 'i', 'accent': 'circunflexo'},
            'ï': {'base': 'i', 'accent': 'trema'},
            'ó': {'base': 'o', 'accent': 'agudo'},
            'ò': {'base': 'o', 'accent': 'grave'},
            'ô': {'base': 'o', 'accent': 'circunflexo'},
            'õ': {'base': 'o', 'accent': 'til'},
            'ö': {'base': 'o', 'accent': 'trema'},
            'ú': {'base': 'u', 'accent': 'agudo'},
            'ù': {'base': 'u', 'accent': 'grave'},
            'û': {'base': 'u', 'accent': 'circunflexo'},
            'ü': {'base': 'u', 'accent': 'trema'},
            'ç': {'base': 'c', 'accent': 'cedilha'},
        }
        
        for char, info in accented_vowels.items():
            self.letters[char] = {
                "char": char,
                "base": info['base'],
                "type": "vogal_acentuada" if info['base'] in "aeiou" else "consoante_acentuada",
                "accent": info['accent'],
            }
    
    def _get_phoneme(self, letter: str) -> str:
        """Retorna o fonema aproximado da letra"""
        phonemes = {
            'a': '/a/', 'b': '/be/', 'c': '/se/', 'd': '/de/',
            'e': '/ɛ/', 'f': '/ɛfi/', 'g': '/ʒe/', 'h': '/aga/',
            'i': '/i/', 'j': '/ʒota/', 'k': '/ka/', 'l': '/ɛli/',
            'm': '/ɛmi/', 'n': '/ɛni/', 'o': '/ɔ/', 'p': '/pe/',
            'q': '/ke/', 'r': '/ɛʁi/', 's': '/ɛsi/', 't': '/te/',
            'u': '/u/', 'v': '/ve/', 'w': '/dablju/', 'x': '/ʃi/',
            'y': '/ipsilon/', 'z': '/ze/'
        }
        return phonemes.get(letter, f"/{letter}/")
    
    def _initialize_digits(self):
        """Inicializa parâmetros de dígitos"""
        digit_words = ["zero", "um", "dois", "três", "quatro", 
                      "cinco", "seis", "sete", "oito", "nove"]
        
        for i in range(10):
            self.digits[str(i)] = {
                "digit": i,
                "word": digit_words[i],
                "parity": "par" if i % 2 == 0 else "ímpar",
                "is_prime": i in [2, 3, 5, 7],
            }
    
    def _initialize_symbols(self):
        """Inicializa parâmetros de símbolos"""
        symbols = {
            '.': {'name': 'ponto', 'type': 'pontuacao'},
            ',': {'name': 'vírgula', 'type': 'pontuacao'},
            ';': {'name': 'ponto-e-vírgula', 'type': 'pontuacao'},
            ':': {'name': 'dois-pontos', 'type': 'pontuacao'},
            '!': {'name': 'exclamação', 'type': 'pontuacao'},
            '?': {'name': 'interrogação', 'type': 'pontuacao'},
            '"': {'name': 'aspas', 'type': 'pontuacao'},
            "'": {'name': 'apóstrofo', 'type': 'pontuacao'},
            '-': {'name': 'hífen', 'type': 'pontuacao'},
            '_': {'name': 'underscore', 'type': 'símbolo'},
            '(': {'name': 'parêntese_aberto', 'type': 'agrupamento'},
            ')': {'name': 'parêntese_fechado', 'type': 'agrupamento'},
            '[': {'name': 'colchete_aberto', 'type': 'agrupamento'},
            ']': {'name': 'colchete_fechado', 'type': 'agrupamento'},
            '{': {'name': 'chave_aberta', 'type': 'agrupamento'},
            '}': {'name': 'chave_fechada', 'type': 'agrupamento'},
            '+': {'name': 'mais', 'type': 'operador'},
            '-': {'name': 'menos', 'type': 'operador'},
            '*': {'name': 'asterisco', 'type': 'operador'},
            '/': {'name': 'barra', 'type': 'operador'},
            '=': {'name': 'igual', 'type': 'operador'},
            '<': {'name': 'menor_que', 'type': 'comparador'},
            '>': {'name': 'maior_que', 'type': 'comparador'},
            '@': {'name': 'arroba', 'type': 'símbolo'},
            '#': {'name': 'hashtag', 'type': 'símbolo'},
            '$': {'name': 'cifrão', 'type': 'moeda'},
            '%': {'name': 'porcento', 'type': 'símbolo'},
            '&': {'name': 'e_comercial', 'type': 'símbolo'},
            ' ': {'name': 'espaço', 'type': 'separador'},
        }
        
        self.symbols = symbols
    
    def _initialize_vocabulary(self):
        """Inicializa vocabulário base"""
        # Palavras funcionais
        functional = [
            # Artigos
            "o", "a", "os", "as", "um", "uma", "uns", "umas",
            # Preposições
            "de", "em", "para", "por", "com", "sem", "sob", "sobre",
            "ante", "apos", "ate", "contra", "desde", "entre", "perante",
            # Conjunções
            "e", "ou", "mas", "porém", "contudo", "todavia", "entretanto",
            "se", "quando", "enquanto", "porque", "pois", "logo", "assim",
            # Pronomes
            "eu", "tu", "ele", "ela", "nós", "vós", "eles", "elas",
            "me", "te", "se", "nos", "vos", "lhe", "lhes",
            "meu", "minha", "teu", "tua", "seu", "sua", "nosso", "nossa",
            "este", "esta", "isto", "esse", "essa", "isso", "aquele", "aquela",
            # Advérbios
            "não", "sim", "talvez", "já", "ainda", "sempre", "nunca",
            "aqui", "ali", "lá", "onde", "longe", "perto",
            "agora", "hoje", "ontem", "amanhã", "depois", "antes",
            "bem", "mal", "assim", "depressa", "devagar",
            # Verbos auxiliares
            "ser", "estar", "ter", "haver", "fazer", "ir", "vir",
        ]
        
        # Substantivos comuns
        nouns = [
            "tempo", "pessoa", "ano", "dia", "coisa", "homem", "mulher",
            "vida", "mundo", "casa", "trabalho", "maneira", "forma",
            "lugar", "parte", "grupo", "problema", "questão", "resposta",
            "sistema", "processo", "resultado", "mudança", "desenvolvimento",
            "conhecimento", "informação", "dado", "ideia", "pensamento",
            "palavra", "letra", "frase", "texto", "linguagem", "comunicação",
            "mente", "cérebro", "inteligência", "aprendizado", "memória",
            "agente", "sistema", "modelo", "algoritmo", "programa",
        ]
        
        # Adjetivos comuns
        adjectives = [
            "bom", "mau", "grande", "pequeno", "novo", "velho",
            "alto", "baixo", "longo", "curto", "largo", "estreito",
            "bonito", "feio", "fácil", "difícil", "simples", "complexo",
            "importante", "necessário", "possível", "certo", "errado",
            "verdadeiro", "falso", "real", "virtual", "digital",
            "inteligente", "rápido", "lento", "forte", "fraco",
        ]
        
        # Verbos comuns
        verbs = [
            "fazer", "dizer", "ir", "vir", "ver", "dar", "saber",
            "querer", "poder", "dever", "falar", "pensar", "achar",
            "conhecer", "entender", "compreender", "aprender", "ensinar",
            "criar", "construir", "destruir", "mudar", "transformar",
            "analisar", "processar", "gerar", "produzir", "desenvolver",
            "usar", "utilizar", "operar", "funcionar", "trabalhar",
        ]
        
        self.vocabulary.update(functional)
        self.vocabulary.update(nouns)
        self.vocabulary.update(adjectives)
        self.vocabulary.update(verbs)
    
    def _save_all_parameters(self):
        """Salva todos os parâmetros em arquivos"""
        # Salva letras
        letters_file = self.params_dir / "letters.json"
        with open(letters_file, 'w', encoding='utf-8') as f:
            json.dump(self.letters, f, ensure_ascii=False, indent=2)
        
        # Salva dígitos
        digits_file = self.params_dir / "digits.json"
        with open(digits_file, 'w', encoding='utf-8') as f:
            json.dump(self.digits, f, ensure_ascii=False, indent=2)
        
        # Salva símbolos
        symbols_file = self.params_dir / "symbols.json"
        with open(symbols_file, 'w', encoding='utf-8') as f:
            json.dump(self.symbols, f, ensure_ascii=False, indent=2)
        
        # Salva vocabulário
        vocab_file = self.params_dir / "vocabulary.json"
        with open(vocab_file, 'w', encoding='utf-8') as f:
            json.dump(sorted(list(self.vocabulary)), f, ensure_ascii=False, indent=2)
        
        print(f"[BRX Parameters] Parâmetros salvos em {self.params_dir}")
    
    def get_all_letters(self) -> List[str]:
        """Retorna todas as letras disponíveis"""
        return list(self.letters.keys())
    
    def get_letter_info(self, letter: str) -> Optional[Dict]:
        """Retorna informações de uma letra"""
        return self.letters.get(letter.lower())
    
    def get_vocabulary_size(self) -> int:
        """Retorna tamanho do vocabulário"""
        return len(self.vocabulary)
    
    def generate_word_params(self, count: int = 10) -> List[Parameter]:
        """Gera parâmetros de palavras aleatórias"""
        params = []
        words = list(self.vocabulary)
        
        for _ in range(min(count, len(words))):
            word = random.choice(words)
            
            param = Parameter(
                id=f"word_{word}_{uuid.uuid4().hex[:6]}",
                name=f"word_{word}",
                value=word,
                param_type=ParameterType.WORD,
                confidence=0.9,
                source="ParameterGeneratorV3",
                timestamp=datetime.now().timestamp(),
                context="Palavra do vocabulário BRX",
                metadata={
                    "length": len(word),
                    "letters": list(word),
                }
            )
            params.append(param)
        
        return params
    
    def generate_number_params(self, count: int = 10) -> List[Parameter]:
        """Gera parâmetros de números"""
        params = []
        
        for _ in range(count):
            num_type = random.choice(["integer", "float", "percentage"])
            
            if num_type == "integer":
                value = random.randint(0, 1000)
            elif num_type == "float":
                value = round(random.uniform(0, 100), 2)
            else:
                value = round(random.uniform(0, 1), 4)
            
            param = Parameter(
                id=f"num_{num_type}_{uuid.uuid4().hex[:6]}",
                name=f"num_{value}",
                value=value,
                param_type=ParameterType.NUMBER,
                confidence=1.0,
                source="ParameterGeneratorV3",
                timestamp=datetime.now().timestamp(),
                context=f"Número tipo {num_type}",
                metadata={"type": num_type}
            )
            params.append(param)
        
        return params
    
    def generate_concept_params(self, count: int = 5) -> List[Parameter]:
        """Gera parâmetros de conceitos abstratos"""
        concepts_base = [
            "aprendizado", "conhecimento", "inteligência", "processamento",
            "análise", "síntese", "compreensão", "raciocínio",
            "memória", "contexto", "significado", "interpretação",
            "padrão", "estrutura", "relação", "conexão",
            "sistema", "processo", "função", "operação",
            "dado", "informação", "conhecimento", "sabedoria",
            "linguagem", "comunicação", "expressão", "representação",
            "agente", "entidade", "objeto", "conceito",
        ]
        
        params = []
        
        for _ in range(count):
            base = random.choice(concepts_base)
            variation = f"{base}_{random.choice(['profundo', 'emergente', 'complexo', 'simples'])}"
            
            param = Parameter(
                id=f"concept_{variation}_{uuid.uuid4().hex[:6]}",
                name=f"concept_{variation}",
                value={
                    "name": variation,
                    "base": base,
                    "complexity": random.uniform(0.3, 1.0),
                },
                param_type=ParameterType.CONCEPT,
                confidence=0.7,
                source="ParameterGeneratorV3",
                timestamp=datetime.now().timestamp(),
                context=f"Conceito abstrato: {variation}",
            )
            params.append(param)
        
        return params
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do gerador"""
        return {
            "letters": len(self.letters),
            "digits": len(self.digits),
            "symbols": len(self.symbols),
            "vocabulary": len(self.vocabulary),
            "generation_count": self.generation_count,
        }
