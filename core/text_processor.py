# BRX-AGENT v3.0 - Processamento Granular de Texto
# Processa texto em múltiplas camadas: caracter → token → palavra → frase → conceito

import re
import unicodedata
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum

class TokenType(Enum):
    CHAR = "caractere"
    WORD = "palavra"
    NUMBER = "numero"
    SYMBOL = "simbolo"
    SPACE = "espaco"
    PUNCTUATION = "pontuacao"

class WordType(Enum):
    NOUN = "substantivo"
    VERB = "verbo"
    ADJECTIVE = "adjetivo"
    ADVERB = "adverbio"
    PRONOUN = "pronome"
    ARTICLE = "artigo"
    PREPOSITION = "preposicao"
    CONJUNCTION = "conjuncao"
    INTERJECTION = "interjeicao"
    NUMERAL = "numeral"
    UNKNOWN = "desconhecido"

@dataclass
class CharacterToken:
    """Representa um caractere individual"""
    char: str
    position: int
    is_alpha: bool
    is_digit: bool
    is_space: bool
    is_punctuation: bool
    is_upper: bool
    is_vowel: bool
    normalized: str  # Sem acento
    
    def __post_init__(self):
        vowels = "aeiou"
        self.is_vowel = self.normalized.lower() in vowels

@dataclass
class WordToken:
    """Representa uma palavra tokenizada"""
    text: str
    start_pos: int
    end_pos: int
    characters: List[CharacterToken] = field(default_factory=list)
    word_type: WordType = WordType.UNKNOWN
    lemma: str = ""  # Forma base
    
    @property
    def length(self) -> int:
        return len(self.text)
    
    @property
    def letters(self) -> List[str]:
        """Retorna lista de letras da palavra"""
        return [c.char for c in self.characters if c.is_alpha]
    
    def contains_letter(self, letter: str) -> bool:
        """Verifica se a palavra contém uma letra específica"""
        return letter.lower() in [c.normalized.lower() for c in self.characters if c.is_alpha]
    
    def count_letter(self, letter: str) -> int:
        """Conta ocorrências de uma letra na palavra"""
        return sum(1 for c in self.characters 
                  if c.is_alpha and c.normalized.lower() == letter.lower())

@dataclass
class Phrase:
    """Representa uma frase processada"""
    text: str
    start_pos: int
    end_pos: int
    words: List[WordToken] = field(default_factory=list)
    phrase_type: str = "declarativa"  # declarativa, interrogativa, exclamativa
    
    @property
    def word_count(self) -> int:
        return len(self.words)
    
    def get_words_without_letter(self, letter: str) -> List[WordToken]:
        """Retorna palavras que NÃO contêm uma letra"""
        return [w for w in self.words if not w.contains_letter(letter)]

@dataclass
class ProcessedText:
    """Texto completamente processado em todas as camadas"""
    raw_text: str
    characters: List[CharacterToken] = field(default_factory=list)
    words: List[WordToken] = field(default_factory=list)
    phrases: List[Phrase] = field(default_factory=list)
    
    # Estatísticas
    char_count: int = 0
    word_count: int = 0
    phrase_count: int = 0
    
    # Análise
    letter_frequency: Dict[str, int] = field(default_factory=dict)
    word_frequency: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        self.char_count = len(self.characters)
        self.word_count = len(self.words)
        self.phrase_count = len(self.phrases)


class GranularTextProcessor:
    """
    Processador granular de texto do BRX
    Quebra o texto em múltiplas camadas de abstração
    """
    
    def __init__(self):
        # Palavras interrogativas
        self.interrogative_words = {
            "o que", "qual", "quais", "quem", "quando", "onde", 
            "por que", "porquê", "como", "quanto", "quantos", "quantas"
        }
        
        # Palavras de negação
        self.negative_words = {"não", "nunca", "jamais", "nem", "sem"}
        
        # Palavras de afirmação
        self.affirmative_words = {"sim", "claro", "certamente", "exato", "correto"}
        
        # Verbos comuns (forma base)
        self.common_verbs = {
            "ser", "estar", "ter", "fazer", "ir", "vir", "ver", "dar",
            "saber", "querer", "poder", "dever", "falar", "pensar",
            "achar", "saber", "conhecer", "entender", "compreender"
        }
    
    def process(self, text: str) -> ProcessedText:
        """Processa texto em todas as camadas"""
        # Camada 1: Caracteres
        characters = self._tokenize_characters(text)
        
        # Camada 2: Palavras
        words = self._tokenize_words(text, characters)
        
        # Camada 3: Frases
        phrases = self._segment_phrases(text, words)
        
        # Estatísticas
        letter_freq = self._calculate_letter_frequency(characters)
        word_freq = self._calculate_word_frequency(words)
        
        return ProcessedText(
            raw_text=text,
            characters=characters,
            words=words,
            phrases=phrases,
            letter_frequency=letter_freq,
            word_frequency=word_freq
        )
    
    def _tokenize_characters(self, text: str) -> List[CharacterToken]:
        """Tokeniza texto em caracteres individuais"""
        characters = []
        
        for i, char in enumerate(text):
            # Normaliza (remove acento para comparação)
            normalized = unicodedata.normalize('NFKD', char)
            normalized = ''.join(c for c in normalized if not unicodedata.combining(c))
            
            token = CharacterToken(
                char=char,
                position=i,
                is_alpha=char.isalpha(),
                is_digit=char.isdigit(),
                is_space=char.isspace(),
                is_punctuation=char in ".,;:!?()[]{}\"'-'",
                is_upper=char.isupper(),
                normalized=normalized
            )
            characters.append(token)
        
        return characters
    
    def _tokenize_words(self, text: str, characters: List[CharacterToken]) -> List[WordToken]:
        """Extrai palavras dos caracteres"""
        words = []
        current_word_chars = []
        word_start = 0
        
        for i, char_token in enumerate(characters):
            if char_token.is_alpha or char_token.is_digit:
                if not current_word_chars:
                    word_start = i
                current_word_chars.append(char_token)
            else:
                if current_word_chars:
                    word_text = ''.join(c.char for c in current_word_chars)
                    word = WordToken(
                        text=word_text,
                        start_pos=word_start,
                        end_pos=i - 1,
                        characters=current_word_chars.copy(),
                        word_type=self._classify_word(word_text),
                        lemma=self._get_lemma(word_text)
                    )
                    words.append(word)
                    current_word_chars = []
        
        # Última palavra
        if current_word_chars:
            word_text = ''.join(c.char for c in current_word_chars)
            word = WordToken(
                text=word_text,
                start_pos=word_start,
                end_pos=len(characters) - 1,
                characters=current_word_chars,
                word_type=self._classify_word(word_text),
                lemma=self._get_lemma(word_text)
            )
            words.append(word)
        
        return words
    
    def _classify_word(self, word: str) -> WordType:
        """Classifica uma palavra por tipo gramatical"""
        word_lower = word.lower()
        
        # Artigos
        if word_lower in ["o", "a", "os", "as", "um", "uma", "uns", "umas"]:
            return WordType.ARTICLE
        
        # Preposições
        if word_lower in ["de", "em", "para", "por", "com", "sem", "sob", "sobre"]:
            return WordType.PREPOSITION
        
        # Conjunções
        if word_lower in ["e", "ou", "mas", "porém", "se", "quando", "porque"]:
            return WordType.CONJUNCTION
        
        # Pronomes
        if word_lower in ["eu", "tu", "ele", "ela", "nós", "vós", "eles", "elas",
                         "me", "te", "se", "nos", "vos", "meu", "teu", "seu"]:
            return WordType.PRONOUN
        
        # Verbos
        if word_lower in self.common_verbs or word_lower.endswith(("ar", "er", "ir")):
            return WordType.VERB
        
        # Numerais
        if word_lower.isdigit() or word_lower in ["um", "dois", "três", "primeiro"]:
            return WordType.NUMERAL
        
        # Adjetivos comuns
        if word_lower.endswith(("o", "a", "os", "as")) and len(word_lower) > 2:
            return WordType.ADJECTIVE
        
        # Advérbios
        if word_lower.endswith(("mente", "mente")):
            return WordType.ADVERB
        
        return WordType.NOUN  # Padrão: substantivo
    
    def _get_lemma(self, word: str) -> str:
        """Retorna a forma base (lema) de uma palavra"""
        word_lower = word.lower()
        
        # Remove plural simples
        if word_lower.endswith("s") and len(word_lower) > 3:
            return word_lower[:-1]
        
        # Remove conjugação verbal básica
        if word_lower.endswith(("ando", "endo", "indo")):
            return word_lower[:-3] + "ar"  # aproximação
        
        if word_lower.endswith(("ei", "ou", "iu")):
            return word_lower[:-2] + "ar"
        
        return word_lower
    
    def _segment_phrases(self, text: str, words: List[WordToken]) -> List[Phrase]:
        """Segmenta texto em frases"""
        phrases = []
        current_words = []
        phrase_start = 0
        
        for word in words:
            current_words.append(word)
            
            # Verifica se é fim de frase
            if word.text.endswith((".", "!", "?")):
                phrase_text = ' '.join(w.text for w in current_words)
                phrase_type = self._classify_phrase_type(phrase_text)
                
                phrase = Phrase(
                    text=phrase_text,
                    start_pos=phrase_start,
                    end_pos=word.end_pos,
                    words=current_words.copy(),
                    phrase_type=phrase_type
                )
                phrases.append(phrase)
                current_words = []
                phrase_start = word.end_pos + 1
        
        # Última frase (sem pontuação final)
        if current_words:
            phrase_text = ' '.join(w.text for w in current_words)
            phrase_type = self._classify_phrase_type(phrase_text)
            
            phrase = Phrase(
                text=phrase_text,
                start_pos=phrase_start,
                end_pos=len(text),
                words=current_words,
                phrase_type=phrase_type
            )
            phrases.append(phrase)
        
        return phrases
    
    def _classify_phrase_type(self, text: str) -> str:
        """Classifica o tipo de frase"""
        text_lower = text.lower().strip()
        
        # Interrogativa
        if text_lower.endswith("?"):
            return "interrogativa"
        
        # Exclamativa
        if text_lower.endswith("!"):
            return "exclamativa"
        
        # Verifica palavras interrogativas no início
        for interrogative in self.interrogative_words:
            if text_lower.startswith(interrogative):
                return "interrogativa"
        
        return "declarativa"
    
    def _calculate_letter_frequency(self, characters: List[CharacterToken]) -> Dict[str, int]:
        """Calcula frequência de cada letra"""
        freq = {}
        for char in characters:
            if char.is_alpha:
                normalized = char.normalized.lower()
                freq[normalized] = freq.get(normalized, 0) + 1
        return freq
    
    def _calculate_word_frequency(self, words: List[WordToken]) -> Dict[str, int]:
        """Calcula frequência de cada palavra"""
        freq = {}
        for word in words:
            text_lower = word.text.lower()
            freq[text_lower] = freq.get(text_lower, 0) + 1
        return freq
    
    def analyze_question(self, processed: ProcessedText) -> Dict:
        """Analisa uma pergunta e extrai informações-chave"""
        analysis = {
            "is_question": False,
            "question_type": None,
            "subject": None,
            "action": None,
            "target": None,
            "constraints": [],
            "key_words": []
        }
        
        # Verifica se é pergunta
        if processed.phrases and processed.phrases[0].phrase_type == "interrogativa":
            analysis["is_question"] = True
        
        # Extrai palavras-chave
        for word in processed.words:
            word_lower = word.text.lower()
            
            # Tipo de pergunta
            if word_lower in ["qual", "quais", "quem", "onde", "quando", "como", "por que"]:
                analysis["question_type"] = word_lower
            
            # Palavras de restrição
            if word_lower in ["não", "sem", "exceto", "somente", "apenas"]:
                analysis["constraints"].append(word_lower)
            
            # Possível alvo
            if word.word_type in [WordType.NOUN, WordType.ADJECTIVE]:
                if word_lower not in ["o", "a", "os", "as", "de", "do", "da"]:
                    analysis["key_words"].append(word_lower)
        
        return analysis
    
    def extract_letter_constraints(self, processed: ProcessedText) -> List[Dict]:
        """Extrai restrições de letras da pergunta"""
        constraints = []
        
        for word in processed.words:
            word_lower = word.text.lower()
            
            # Padrão: "não tem a letra X" ou "sem a letra X"
            if word_lower in ["não", "sem"]:
                # Procura letra nas próximas palavras
                idx = processed.words.index(word)
                for next_word in processed.words[idx:idx+5]:
                    if len(next_word.text) == 1 and next_word.text.isalpha():
                        constraints.append({
                            "type": "exclude",
                            "letter": next_word.text.lower(),
                            "context": "nao_tem_letra"
                        })
        
        return constraints
