# BRX-AGENT v3.0 - Banco de Conhecimento Embutido
# Conhecimento base para processamento offline e independente

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class KnowledgeCategory(Enum):
    GEOGRAPHY = "geografia"
    LANGUAGE = "linguagem"
    MATHEMATICS = "matematica"
    SCIENCE = "ciencia"
    HISTORY = "historia"
    GENERAL = "geral"

@dataclass
class KnowledgeEntry:
    key: str
    value: any
    category: KnowledgeCategory
    attributes: Dict[str, any]
    related: List[str]

class BRXKnowledgeBase:
    """
    Banco de conhecimento embutido do BRX
    Fornece dados base para processamento sem internet
    """
    
    def __init__(self):
        self.data: Dict[str, KnowledgeEntry] = {}
        self.index_by_letter: Dict[str, Set[str]] = {}
        self.index_by_word: Dict[str, Set[str]] = {}
        self._initialize_all_knowledge()
    
    def _initialize_all_knowledge(self):
        """Inicializa todo o conhecimento base"""
        self._init_geography_brazil()
        self._init_language_data()
        self._init_mathematics()
        self._init_common_facts()
        self._build_indexes()
    
    def _init_geography_brazil(self):
        """Inicializa dados geográficos do Brasil"""
        # Estados do Brasil com suas letras
        estados = {
            "Acre": {"sigla": "AC", "capital": "Rio Branco", "regiao": "Norte"},
            "Alagoas": {"sigla": "AL", "capital": "Maceió", "regiao": "Nordeste"},
            "Amapá": {"sigla": "AP", "capital": "Macapá", "regiao": "Norte"},
            "Amazonas": {"sigla": "AM", "capital": "Manaus", "regiao": "Norte"},
            "Bahia": {"sigla": "BA", "capital": "Salvador", "regiao": "Nordeste"},
            "Ceará": {"sigla": "CE", "capital": "Fortaleza", "regiao": "Nordeste"},
            "Distrito Federal": {"sigla": "DF", "capital": "Brasília", "regiao": "Centro-Oeste"},
            "Espírito Santo": {"sigla": "ES", "capital": "Vitória", "regiao": "Sudeste"},
            "Goiás": {"sigla": "GO", "capital": "Goiânia", "regiao": "Centro-Oeste"},
            "Maranhão": {"sigla": "MA", "capital": "São Luís", "regiao": "Nordeste"},
            "Mato Grosso": {"sigla": "MT", "capital": "Cuiabá", "regiao": "Centro-Oeste"},
            "Mato Grosso do Sul": {"sigla": "MS", "capital": "Campo Grande", "regiao": "Centro-Oeste"},
            "Minas Gerais": {"sigla": "MG", "capital": "Belo Horizonte", "regiao": "Sudeste"},
            "Pará": {"sigla": "PA", "capital": "Belém", "regiao": "Norte"},
            "Paraíba": {"sigla": "PB", "capital": "João Pessoa", "regiao": "Nordeste"},
            "Paraná": {"sigla": "PR", "capital": "Curitiba", "regiao": "Sul"},
            "Pernambuco": {"sigla": "PE", "capital": "Recife", "regiao": "Nordeste"},
            "Piauí": {"sigla": "PI", "capital": "Teresina", "regiao": "Nordeste"},
            "Rio de Janeiro": {"sigla": "RJ", "capital": "Rio de Janeiro", "regiao": "Sudeste"},
            "Rio Grande do Norte": {"sigla": "RN", "capital": "Natal", "regiao": "Nordeste"},
            "Rio Grande do Sul": {"sigla": "RS", "capital": "Porto Alegre", "regiao": "Sul"},
            "Rondônia": {"sigla": "RO", "capital": "Porto Velho", "regiao": "Norte"},
            "Roraima": {"sigla": "RR", "capital": "Boa Vista", "regiao": "Norte"},
            "Santa Catarina": {"sigla": "SC", "capital": "Florianópolis", "regiao": "Sul"},
            "São Paulo": {"sigla": "SP", "capital": "São Paulo", "regiao": "Sudeste"},
            "Sergipe": {"sigla": "SE", "capital": "Aracaju", "regiao": "Nordeste"},
            "Tocantins": {"sigla": "TO", "capital": "Palmas", "regiao": "Norte"},
        }
        
        for nome, dados in estados.items():
            entry = KnowledgeEntry(
                key=f"estado_{nome.lower().replace(' ', '_')}",
                value=nome,
                category=KnowledgeCategory.GEOGRAPHY,
                attributes={
                    "tipo": "estado",
                    "sigla": dados["sigla"],
                    "capital": dados["capital"],
                    "regiao": dados["regiao"],
                    "letras": list(nome.lower().replace(' ', '')),
                    "tem_letra_a": 'a' in nome.lower(),
                    "tem_letra_e": 'e' in nome.lower(),
                    "tem_letra_i": 'i' in nome.lower(),
                    "tem_letra_o": 'o' in nome.lower(),
                    "tem_letra_u": 'u' in nome.lower(),
                },
                related=[f"capital_{dados['capital'].lower().replace(' ', '_')}", 
                        f"regiao_{dados['regiao'].lower().replace('-', '_')}"]
            )
            self.data[entry.key] = entry
        
        # Capitais
        for nome, dados in estados.items():
            capital = dados["capital"]
            entry = KnowledgeEntry(
                key=f"capital_{capital.lower().replace(' ', '_')}",
                value=capital,
                category=KnowledgeCategory.GEOGRAPHY,
                attributes={
                    "tipo": "capital",
                    "estado": nome,
                    "sigla_estado": dados["sigla"],
                    "regiao": dados["regiao"],
                    "letras": list(capital.lower().replace(' ', '')),
                },
                related=[f"estado_{nome.lower().replace(' ', '_')}"]
            )
            self.data[entry.key] = entry
        
        # Regiões
        regioes = {
            "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
            "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
            "Centro-Oeste": ["DF", "GO", "MT", "MS"],
            "Sudeste": ["ES", "MG", "RJ", "SP"],
            "Sul": ["PR", "RS", "SC"],
        }
        
        for regiao, siglas in regioes.items():
            entry = KnowledgeEntry(
                key=f"regiao_{regiao.lower().replace('-', '_')}",
                value=regiao,
                category=KnowledgeCategory.GEOGRAPHY,
                attributes={
                    "tipo": "regiao",
                    "estados": [e for e, d in estados.items() if d["sigla"] in siglas],
                    "siglas": siglas,
                    "quantidade_estados": len(siglas),
                },
                related=[]
            )
            self.data[entry.key] = entry
    
    def _init_language_data(self):
        """Inicializa dados linguísticos"""
        # Alfabeto completo com atributos
        alfabeto = {
            'a': {"tipo": "vogal", "acentuadas": ['á', 'à', 'â', 'ã', 'ä']},
            'b': {"tipo": "consoante", "acentuadas": []},
            'c': {"tipo": "consoante", "acentuadas": ['ç']},
            'd': {"tipo": "consoante", "acentuadas": []},
            'e': {"tipo": "vogal", "acentuadas": ['é', 'è', 'ê', 'ë']},
            'f': {"tipo": "consoante", "acentuadas": []},
            'g': {"tipo": "consoante", "acentuadas": []},
            'h': {"tipo": "consoante", "acentuadas": []},
            'i': {"tipo": "vogal", "acentuadas": ['í', 'ì', 'î', 'ï']},
            'j': {"tipo": "consoante", "acentuadas": []},
            'k': {"tipo": "consoante", "acentuadas": []},
            'l': {"tipo": "consoante", "acentuadas": []},
            'm': {"tipo": "consoante", "acentuadas": []},
            'n': {"tipo": "consoante", "acentuadas": []},
            'o': {"tipo": "vogal", "acentuadas": ['ó', 'ò', 'ô', 'õ', 'ö']},
            'p': {"tipo": "consoante", "acentuadas": []},
            'q': {"tipo": "consoante", "acentuadas": []},
            'r': {"tipo": "consoante", "acentuadas": []},
            's': {"tipo": "consoante", "acentuadas": []},
            't': {"tipo": "consoante", "acentuadas": []},
            'u': {"tipo": "vogal", "acentuadas": ['ú', 'ù', 'û', 'ü']},
            'v': {"tipo": "consoante", "acentuadas": []},
            'w': {"tipo": "consoante", "acentuadas": []},
            'x': {"tipo": "consoante", "acentuadas": []},
            'y': {"tipo": "consoante", "acentuadas": []},
            'z': {"tipo": "consoante", "acentuadas": []},
        }
        
        for letra, dados in alfabeto.items():
            entry = KnowledgeEntry(
                key=f"letra_{letra}",
                value=letra,
                category=KnowledgeCategory.LANGUAGE,
                attributes={
                    "tipo": dados["tipo"],
                    "maiuscula": letra.upper(),
                    "acentuadas": dados["acentuadas"],
                    "posicao_alfabeto": ord(letra) - ord('a') + 1,
                },
                related=[]
            )
            self.data[entry.key] = entry
        
        # Palavras funcionais
        funcionais = {
            "artigos": ["o", "a", "os", "as", "um", "uma", "uns", "umas"],
            "preposicoes": ["de", "em", "para", "por", "com", "sem", "sob", "sobre", 
                           "ante", "apos", "ate", "contra", "desde", "entre", "perante"],
            "conjuncoes": ["e", "ou", "mas", "porém", "contudo", "todavia", "entretanto",
                          "se", "quando", "enquanto", "porque", "pois", "logo", "assim"],
            "pronomes": ["eu", "tu", "ele", "ela", "nós", "vós", "eles", "elas",
                        "me", "te", "se", "nos", "vos", "o", "a", "os", "as",
                        "meu", "minha", "teu", "tua", "seu", "sua", "nosso", "nossa"],
        }
        
        for categoria, palavras in funcionais.items():
            for palavra in palavras:
                key = f"palavra_{palavra.lower().replace(' ', '_')}"
                if key not in self.data:
                    entry = KnowledgeEntry(
                        key=key,
                        value=palavra,
                        category=KnowledgeCategory.LANGUAGE,
                        attributes={
                            "tipo": categoria,
                            "letras": list(palavra.lower()),
                            "tamanho": len(palavra),
                        },
                        related=[]
                    )
                    self.data[key] = entry
    
    def _init_mathematics(self):
        """Inicializa dados matemáticos"""
        # Números com propriedades
        for i in range(0, 1001):
            atributos = {
                "par": i % 2 == 0,
                "impar": i % 2 != 0,
                "primo": self._is_prime(i),
                "digitos": len(str(i)),
                "quadrado": i ** 2,
                "raiz_quadrada": i ** 0.5,
            }
            
            if i <= 100:
                atributos["tabuada"] = [i * j for j in range(1, 11)]
            
            entry = KnowledgeEntry(
                key=f"numero_{i}",
                value=i,
                category=KnowledgeCategory.MATHEMATICS,
                attributes=atributos,
                related=[]
            )
            self.data[entry.key] = entry
    
    def _is_prime(self, n: int) -> bool:
        """Verifica se número é primo"""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def _init_common_facts(self):
        """Inicializa fatos comuns"""
        fatos = {
            "dias_semana": ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"],
            "meses_ano": ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
            "cores_basicas": ["vermelho", "azul", "verde", "amarelo", "preto", "branco"],
            "direcoes": ["norte", "sul", "leste", "oeste"],
        }
        
        for categoria, itens in fatos.items():
            entry = KnowledgeEntry(
                key=f"fato_{categoria}",
                value=itens,
                category=KnowledgeCategory.GENERAL,
                attributes={
                    "categoria": categoria,
                    "quantidade": len(itens),
                    "itens": itens,
                },
                related=[]
            )
            self.data[entry.key] = entry
    
    def _build_indexes(self):
        """Constrói índices para busca rápida"""
        for key, entry in self.data.items():
            value_str = str(entry.value).lower()
            
            # Indexa por letra
            for char in value_str:
                if char.isalpha():
                    if char not in self.index_by_letter:
                        self.index_by_letter[char] = set()
                    self.index_by_letter[char].add(key)
            
            # Indexa por palavra
            words = value_str.split()
            for word in words:
                clean_word = ''.join(c for c in word if c.isalnum())
                if clean_word:
                    if clean_word not in self.index_by_word:
                        self.index_by_word[clean_word] = set()
                    self.index_by_word[clean_word].add(key)
    
    def query_by_letter(self, letter: str, exclude_letter: str = None) -> List[KnowledgeEntry]:
        """Busca entradas que contêm uma letra específica"""
        letter = letter.lower()
        keys = self.index_by_letter.get(letter, set())
        
        results = []
        for key in keys:
            entry = self.data.get(key)
            if entry:
                if exclude_letter:
                    value_str = str(entry.value).lower()
                    if exclude_letter.lower() not in value_str:
                        results.append(entry)
                else:
                    results.append(entry)
        
        return results
    
    def query_states_without_letter(self, letter: str) -> List[str]:
        """Retorna estados que NÃO contêm uma letra específica"""
        letter = letter.lower()
        results = []
        
        for key, entry in self.data.items():
            if entry.attributes.get("tipo") == "estado":
                value_str = str(entry.value).lower()
                if letter not in value_str:
                    results.append(entry.value)
        
        return results
    
    def get_state_info(self, state_name: str) -> Optional[KnowledgeEntry]:
        """Retorna informações de um estado"""
        key = f"estado_{state_name.lower().replace(' ', '_')}"
        return self.data.get(key)
    
    def get_all_states(self) -> List[str]:
        """Retorna todos os nomes de estados"""
        states = []
        for key, entry in self.data.items():
            if entry.attributes.get("tipo") == "estado":
                states.append(entry.value)
        return states
    
    def search(self, query: str) -> List[KnowledgeEntry]:
        """Busca genérica no banco de conhecimento"""
        query = query.lower()
        results = []
        
        for key, entry in self.data.items():
            if query in str(entry.value).lower() or query in key.lower():
                results.append(entry)
        
        return results
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do banco de conhecimento"""
        categories = {}
        for entry in self.data.values():
            cat = entry.category.value
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_entries": len(self.data),
            "by_category": categories,
            "indexed_letters": len(self.index_by_letter),
            "indexed_words": len(self.index_by_word),
        }
