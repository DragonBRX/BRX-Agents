# BRX-AGENT v3.0 - Sistema de 8 Mentes em Camadas
# Cada mente processa uma camada diferente da informação

import random
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from core.text_processor import GranularTextProcessor, ProcessedText, WordType
from core.knowledge_base import BRXKnowledgeBase, KnowledgeCategory

class MindLayer(Enum):
    """Camadas de processamento das mentes"""
    CHARACTER = 1    # Processamento de caracteres
    LEXICAL = 2      # Processamento léxico (palavras)
    SYNTACTIC = 3    # Análise sintática
    SEMANTIC = 4     # Análise semântica
    LOGICAL = 5      # Raciocínio lógico
    MEMORY = 6       # Acesso à memória
    GENERATIVE = 7   # Geração de resposta
    VALIDATION = 8   # Validação e correção

@dataclass
class MindThought:
    """Pensamento gerado por uma mente"""
    mind_name: str
    layer: MindLayer
    input_data: Any
    output_data: Any
    confidence: float
    reasoning: str

@dataclass
class ConsensusResult:
    """Resultado do consenso entre as mentes"""
    final_answer: str
    confidence: float
    thoughts: List[MindThought]
    processing_time: float


class CharacterMind:
    """
    Mente 1: Processamento de Caracteres
    Analisa cada letra individualmente
    """
    
    def __init__(self):
        self.name = "Caractere"
        self.layer = MindLayer.CHARACTER
    
    def process(self, text: str, processed: ProcessedText) -> MindThought:
        """Processa caracteres do texto"""
        analysis = {
            "total_chars": len(processed.characters),
            "letters": [c.char for c in processed.characters if c.is_alpha],
            "unique_letters": list(set(c.normalized.lower() for c in processed.characters if c.is_alpha)),
            "letter_frequency": processed.letter_frequency,
            "has_numbers": any(c.is_digit for c in processed.characters),
            "has_punctuation": any(c.is_punctuation for c in processed.characters),
        }
        
        reasoning = f"Analisei {analysis['total_chars']} caracteres. "
        reasoning += f"Encontrei {len(analysis['unique_letters'])} letras únicas: {', '.join(sorted(analysis['unique_letters']))}."
        
        return MindThought(
            mind_name=self.name,
            layer=self.layer,
            input_data=text,
            output_data=analysis,
            confidence=0.95,
            reasoning=reasoning
        )


class LexicalMind:
    """
    Mente 2: Processamento Léxico
    Analisa palavras e seu significado
    """
    
    def __init__(self, knowledge_base: BRXKnowledgeBase):
        self.name = "Léxico"
        self.layer = MindLayer.LEXICAL
        self.kb = knowledge_base
    
    def process(self, text: str, processed: ProcessedText) -> MindThought:
        """Processa palavras do texto"""
        word_analysis = []
        
        for word in processed.words:
            word_info = {
                "text": word.text,
                "type": word.word_type.value,
                "letters": word.letters,
                "length": word.length,
                "knowledge_matches": self._find_knowledge_matches(word.text)
            }
            word_analysis.append(word_info)
        
        # Identifica palavras-chave
        key_words = [w.text for w in processed.words 
                    if w.word_type in [WordType.NOUN, WordType.ADJECTIVE, WordType.VERB]]
        
        analysis = {
            "words": word_analysis,
            "word_count": len(processed.words),
            "key_words": key_words,
            "word_frequency": processed.word_frequency,
        }
        
        reasoning = f"Identifiquei {analysis['word_count']} palavras. "
        reasoning += f"Palavras-chave: {', '.join(key_words[:5])}. "
        
        return MindThought(
            mind_name=self.name,
            layer=self.layer,
            input_data=processed.words,
            output_data=analysis,
            confidence=0.90,
            reasoning=reasoning
        )
    
    def _find_knowledge_matches(self, word: str) -> List[str]:
        """Busca correspondências no banco de conhecimento"""
        matches = []
        results = self.kb.search(word)
        for entry in results[:3]:  # Top 3
            matches.append(f"{entry.value} ({entry.category.value})")
        return matches


class SyntacticMind:
    """
    Mente 3: Análise Sintática
    Entende a estrutura gramatical
    """
    
    def __init__(self):
        self.name = "Sintática"
        self.layer = MindLayer.SYNTACTIC
    
    def process(self, text: str, processed: ProcessedText) -> MindThought:
        """Analisa estrutura sintática"""
        phrase_analysis = []
        
        for phrase in processed.phrases:
            structure = {
                "text": phrase.text,
                "type": phrase.phrase_type,
                "word_count": phrase.word_count,
                "word_types": [w.word_type.value for w in phrase.words],
            }
            phrase_analysis.append(structure)
        
        # Detecta tipo de sentença
        is_question = any(p.phrase_type == "interrogativa" for p in processed.phrases)
        is_exclamation = any(p.phrase_type == "exclamativa" for p in processed.phrases)
        
        analysis = {
            "phrases": phrase_analysis,
            "phrase_count": len(processed.phrases),
            "is_question": is_question,
            "is_exclamation": is_exclamation,
            "sentence_type": "interrogativa" if is_question else "exclamativa" if is_exclamation else "declarativa"
        }
        
        reasoning = f"Estrutura: {analysis['phrase_count']} frase(s). "
        reasoning += f"Tipo: {analysis['sentence_type']}. "
        
        return MindThought(
            mind_name=self.name,
            layer=self.layer,
            input_data=processed.phrases,
            output_data=analysis,
            confidence=0.85,
            reasoning=reasoning
        )


class SemanticMind:
    """
    Mente 4: Análise Semântica
    Extrai significado e intenção
    """
    
    def __init__(self, knowledge_base: BRXKnowledgeBase):
        self.name = "Semântica"
        self.layer = MindLayer.SEMANTIC
        self.kb = knowledge_base
    
    def process(self, text: str, processed: ProcessedText) -> MindThought:
        """Extrai significado semântico"""
        processor = GranularTextProcessor()
        question_analysis = processor.analyze_question(processed)
        letter_constraints = processor.extract_letter_constraints(processed)
        
        # Extrai intenção
        intention = self._extract_intention(processed, question_analysis)
        
        # Busca entidades no conhecimento
        entities = []
        for word in processed.words:
            if word.word_type in [WordType.NOUN, WordType.ADJECTIVE]:
                kb_results = self.kb.search(word.text)
                if kb_results:
                    entities.append({
                        "word": word.text,
                        "matches": [(e.value, e.category.value) for e in kb_results[:2]]
                    })
        
        analysis = {
            "intention": intention,
            "question_analysis": question_analysis,
            "letter_constraints": letter_constraints,
            "entities": entities,
            "subject": question_analysis.get("key_words", [])[0] if question_analysis.get("key_words") else None,
        }
        
        reasoning = f"Intenção detectada: {intention}. "
        if letter_constraints:
            reasoning += f"Restrições de letras: {len(letter_constraints)}. "
        
        return MindThought(
            mind_name=self.name,
            layer=self.layer,
            input_data=text,
            output_data=analysis,
            confidence=0.80,
            reasoning=reasoning
        )
    
    def _extract_intention(self, processed: ProcessedText, question_analysis: Dict) -> str:
        """Extrai a intenção do usuário"""
        if question_analysis.get("is_question"):
            q_type = question_analysis.get("question_type")
            
            if q_type in ["qual", "quais"]:
                return "identificar_lista"
            elif q_type in ["quem"]:
                return "identificar_entidade"
            elif q_type in ["onde"]:
                return "localizar"
            elif q_type in ["como"]:
                return "explicar_processo"
            elif q_type in ["por que"]:
                return "explicar_causa"
            else:
                return "responder_pergunta"
        
        # Verifica comandos
        first_word = processed.words[0].text.lower() if processed.words else ""
        if first_word in ["liste", "mostre", "exiba", "quais"]:
            return "listar"
        
        return "conversar"


class LogicalMind:
    """
    Mente 5: Raciocínio Lógico
    Aplica lógica para resolver problemas
    """
    
    def __init__(self, knowledge_base: BRXKnowledgeBase):
        self.name = "Lógica"
        self.layer = MindLayer.LOGICAL
        self.kb = knowledge_base
    
    def process(self, text: str, semantic_analysis: Dict) -> MindThought:
        """Aplica raciocínio lógico"""
        intention = semantic_analysis.get("intention", "")
        constraints = semantic_analysis.get("letter_constraints", [])
        
        result = None
        reasoning_steps = []
        
        # Raciocínio baseado na intenção
        if intention == "identificar_lista":
            result = self._reason_list_identification(semantic_analysis)
            reasoning_steps.append("Identificação de lista solicitada")
        
        elif intention == "listar":
            result = self._reason_listing(semantic_analysis)
            reasoning_steps.append("Listagem solicitada")
        
        # Aplica restrições de letras
        if constraints:
            for constraint in constraints:
                if constraint["type"] == "exclude":
                    letter = constraint["letter"]
                    states_without = self.kb.query_states_without_letter(letter)
                    result = {
                        "constraint_type": "exclude_letter",
                        "letter": letter,
                        "matching_items": states_without,
                        "count": len(states_without)
                    }
                    reasoning_steps.append(f"Aplicada restrição: excluir letra '{letter}'")
        
        analysis = {
            "result": result,
            "reasoning_steps": reasoning_steps,
            "applied_rules": len(reasoning_steps),
        }
        
        reasoning = " → ".join(reasoning_steps) if reasoning_steps else "Nenhum raciocínio especial aplicado"
        
        return MindThought(
            mind_name=self.name,
            layer=self.layer,
            input_data=semantic_analysis,
            output_data=analysis,
            confidence=0.85 if result else 0.60,
            reasoning=reasoning
        )
    
    def _reason_list_identification(self, analysis: Dict) -> Dict:
        """Raciocínio para identificação de lista"""
        entities = analysis.get("entities", [])
        
        # Procura por entidades geográficas
        geo_entities = [e for e in entities 
                       if any("geografia" in str(m) for m in e.get("matches", []))]
        
        if geo_entities:
            return {
                "domain": "geografia",
                "entities": geo_entities,
                "suggested_action": "listar_por_categoria"
            }
        
        return {"domain": "desconhecido", "suggested_action": "buscar_conhecimento"}
    
    def _reason_listing(self, analysis: Dict) -> Dict:
        """Raciocínio para listagem"""
        key_words = analysis.get("question_analysis", {}).get("key_words", [])
        
        # Detecta categoria
        if any(w in ["estado", "estados"] for w in key_words):
            return {
                "category": "estados_brasil",
                "items": self.kb.get_all_states(),
                "count": len(self.kb.get_all_states())
            }
        
        return {"category": "desconhecido", "items": []}


class MemoryMind:
    """
    Mente 6: Memória e Contexto
    Acessa memória de conversas anteriores
    """
    
    def __init__(self):
        self.name = "Memória"
        self.layer = MindLayer.MEMORY
        self.short_term: List[Dict] = []  # Últimas 10 interações
        self.context: Dict = {}
    
    def process(self, text: str, current_analysis: Dict) -> MindThought:
        """Acessa memória contextual"""
        # Recupera contexto relevante
        relevant_memories = self._find_relevant_memories(text)
        
        # Atualiza contexto atual
        self._update_context(current_analysis)
        
        analysis = {
            "relevant_memories": relevant_memories,
            "context": self.context.copy(),
            "conversation_history": len(self.short_term),
        }
        
        reasoning = f"Recuperadas {len(relevant_memories)} memórias relevantes. "
        reasoning += f"Contexto atual: {list(self.context.keys())}"
        
        return MindThought(
            mind_name=self.name,
            layer=self.layer,
            input_data=text,
            output_data=analysis,
            confidence=0.75,
            reasoning=reasoning
        )
    
    def store_interaction(self, user_input: str, brx_response: str):
        """Armazena interação na memória"""
        self.short_term.append({
            "user": user_input,
            "brx": brx_response,
            "timestamp": __import__('time').time()
        })
        
        # Mantém apenas últimas 10
        if len(self.short_term) > 10:
            self.short_term.pop(0)
    
    def _find_relevant_memories(self, text: str) -> List[Dict]:
        """Encontra memórias relevantes"""
        relevant = []
        text_lower = text.lower()
        
        for memory in self.short_term:
            if any(word in memory["user"].lower() for word in text_lower.split()):
                relevant.append(memory)
        
        return relevant[-3:]  # Últimas 3 relevantes
    
    def _update_context(self, analysis: Dict):
        """Atualiza contexto da conversa"""
        if "subject" in analysis and analysis["subject"]:
            self.context["last_subject"] = analysis["subject"]
        if "intention" in analysis:
            self.context["last_intention"] = analysis["intention"]


class GenerativeMind:
    """
    Mente 7: Geração de Resposta
    Gera resposta coerente baseada em todas as análises
    """
    
    def __init__(self):
        self.name = "Geração"
        self.layer = MindLayer.GENERATIVE
        self.response_templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Carrega templates de resposta"""
        return {
            "greeting": [
                "Olá! Sou o BRX, pronto para ajudar.",
                "Oi! Em que posso ser útil?",
                "Saudações! Estou aqui para responder suas perguntas."
            ],
            "list_result": [
                "Encontrei {count} resultado(s): {items}",
                "Aqui está a lista com {count} item(ns): {items}",
                "Foram identificados {count} resultado(s): {items}"
            ],
            "single_result": [
                "O resultado é: {result}",
                "Encontrei: {result}",
                "Resposta: {result}"
            ],
            "unknown": [
                "Não tenho certeza sobre isso. Pode reformular?",
                "Preciso de mais contexto para responder adequadamente.",
                "Não compreendi completamente. Pode explicar melhor?"
            ],
            "thinking": [
                "Analisando sua pergunta... ",
                "Processando as informações... ",
                "Deixe-me pensar sobre isso... "
            ]
        }
    
    def generate(self, all_thoughts: List[MindThought], original_text: str) -> str:
        """Gera resposta final"""
        # Extrai dados de cada mente
        semantic_data = self._get_thought_data(all_thoughts, MindLayer.SEMANTIC)
        logical_data = self._get_thought_data(all_thoughts, MindLayer.LOGICAL)
        syntactic_data = self._get_thought_data(all_thoughts, MindLayer.SYNTACTIC)
        
        intention = semantic_data.get("intention", "") if semantic_data else ""
        
        # Gera resposta baseada na intenção
        if intention == "conversar" and self._is_greeting(original_text):
            return random.choice(self.response_templates["greeting"])
        
        # Resposta para listas com restrições
        if logical_data and logical_data.get("result"):
            result = logical_data["result"]
            
            if result.get("constraint_type") == "exclude_letter":
                items = result.get("matching_items", [])
                count = result.get("count", 0)
                letter = result.get("letter", "")
                
                if items:
                    items_str = ", ".join(items[:10])  # Max 10
                    if count > 10:
                        items_str += f" e mais {count - 10}..."
                    
                    template = random.choice(self.response_templates["list_result"])
                    return template.format(count=count, items=items_str)
                else:
                    return f"Não encontrei nenhum resultado sem a letra '{letter}'."
            
            # Lista simples
            if result.get("category") == "estados_brasil":
                items = result.get("items", [])
                count = result.get("count", 0)
                items_str = ", ".join(items[:10])
                if count > 10:
                    items_str += f" e mais {count - 10}..."
                
                template = random.choice(self.response_templates["list_result"])
                return template.format(count=count, items=items_str)
        
        # Pergunta não reconhecida
        return random.choice(self.response_templates["unknown"])
    
    def _get_thought_data(self, thoughts: List[MindThought], layer: MindLayer) -> Optional[Dict]:
        """Extrai dados de uma mente específica"""
        for thought in thoughts:
            if thought.layer == layer:
                return thought.output_data
        return None
    
    def _is_greeting(self, text: str) -> bool:
        """Verifica se é uma saudação"""
        greetings = ["oi", "olá", "ola", "eae", "e aí", "bom dia", "boa tarde", "boa noite", "hello", "hi"]
        return any(g in text.lower() for g in greetings)


class ValidationMind:
    """
    Mente 8: Validação e Correção
    Valida e melhora a resposta gerada
    """
    
    def __init__(self):
        self.name = "Validação"
        self.layer = MindLayer.VALIDATION
    
    def validate(self, response: str, all_thoughts: List[MindThought], original_text: str) -> str:
        """Valida e corrige a resposta"""
        # Verifica se resposta está vazia
        if not response or len(response.strip()) < 3:
            return "Desculpe, não consegui processar sua solicitação. Pode tentar novamente?"
        
        # Verifica confiança das mentes
        low_confidence = [t for t in all_thoughts if t.confidence < 0.60]
        
        if len(low_confidence) >= 3:
            # Muitas mentes com baixa confiança
            return f"Não tenho certeza, mas: {response}"
        
        # Adiciona contexto se necessário
        if self._needs_context(response, original_text):
            response = self._add_context(response, all_thoughts)
        
        return response
    
    def _needs_context(self, response: str, original: str) -> bool:
        """Verifica se resposta precisa de mais contexto"""
        # Se a resposta é muito curta e a pergunta é complexa
        if len(response) < 20 and len(original) > 30:
            return True
        return False
    
    def _add_context(self, response: str, thoughts: List[MindThought]) -> str:
        """Adiciona contexto à resposta"""
        # Busca informações relevantes nos pensamentos
        for thought in thoughts:
            if thought.layer == MindLayer.LOGICAL and thought.output_data:
                result = thought.output_data.get("result")
                if result:
                    return f"{response} (Baseado em análise de {result.get('count', 0)} itens)"
        
        return response


class EightMindsSystemV3:
    """
    Sistema integrado das 8 Mentes do BRX v3.0
    """
    
    def __init__(self, knowledge_base: BRXKnowledgeBase):
        self.kb = knowledge_base
        self.text_processor = GranularTextProcessor()
        
        # Inicializa as 8 mentes
        self.character_mind = CharacterMind()
        self.lexical_mind = LexicalMind(knowledge_base)
        self.syntactic_mind = SyntacticMind()
        self.semantic_mind = SemanticMind(knowledge_base)
        self.logical_mind = LogicalMind(knowledge_base)
        self.memory_mind = MemoryMind()
        self.generative_mind = GenerativeMind()
        self.validation_mind = ValidationMind()
        
        self.minds = [
            self.character_mind,
            self.lexical_mind,
            self.syntactic_mind,
            self.semantic_mind,
            self.logical_mind,
            self.memory_mind,
            self.generative_mind,
            self.validation_mind
        ]
    
    def process(self, text: str) -> ConsensusResult:
        """Processa texto através de todas as 8 mentes"""
        import time
        start_time = time.time()
        
        # Processamento granular do texto
        processed = self.text_processor.process(text)
        
        # Executa cada mente em sequência
        thoughts = []
        
        # Camadas 1-3: Processamento básico
        thoughts.append(self.character_mind.process(text, processed))
        thoughts.append(self.lexical_mind.process(text, processed))
        thoughts.append(self.syntactic_mind.process(text, processed))
        
        # Camada 4: Semântica
        semantic_thought = self.semantic_mind.process(text, processed)
        thoughts.append(semantic_thought)
        
        # Camada 5: Lógica
        logical_thought = self.logical_mind.process(text, semantic_thought.output_data)
        thoughts.append(logical_thought)
        
        # Camada 6: Memória
        memory_thought = self.memory_mind.process(text, semantic_thought.output_data)
        thoughts.append(memory_thought)
        
        # Camada 7: Geração
        raw_response = self.generative_mind.generate(thoughts, text)
        
        # Camada 8: Validação
        final_response = self.validation_mind.validate(raw_response, thoughts, text)
        
        # Calcula confiança geral
        avg_confidence = sum(t.confidence for t in thoughts[:6]) / 6
        
        processing_time = time.time() - start_time
        
        return ConsensusResult(
            final_answer=final_response,
            confidence=avg_confidence,
            thoughts=thoughts,
            processing_time=processing_time
        )
    
    def get_thoughts_summary(self, result: ConsensusResult) -> str:
        """Retorna resumo dos pensamentos"""
        summary = "\n[BRX Processamento]\n"
        for thought in result.thoughts:
            summary += f"  {thought.mind_name}: {thought.reasoning[:60]}...\n"
        return summary
