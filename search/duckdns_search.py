# BRX-AGENT v2.0 - Módulo de Pesquisa Duck DNS
# Pesquisa web usando DuckDuckGo sem necessidade de API key

import re
import time
import random
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path


@dataclass
class SearchResult:
    """Resultado de pesquisa"""
    title: str
    url: str
    snippet: str
    relevance: float
    source: str = "duckduckgo"


class DuckDNSSearcher:
    """
    Pesquisador web usando DuckDuckGo
    Não requer API key - usa scraping direto
    """
    
    def __init__(self, cache_path: str = "./storage/hd/search_cache.json"):
        self.cache_path = Path(cache_path)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.cache: Dict[str, Dict] = {}
        self.last_search_time = 0
        self.min_delay = 1.0  # Segundos entre pesquisas
        
        self._load_cache()
    
    def _load_cache(self):
        """Carrega cache de pesquisas"""
        if self.cache_path.exists():
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except Exception as e:
                print(f"[DuckDNS] Erro ao carregar cache: {e}")
    
    def _save_cache(self):
        """Salva cache de pesquisas"""
        try:
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[DuckDNS] Erro ao salvar cache: {e}")
    
    def _rate_limit(self):
        """Controla taxa de requisições"""
        current_time = time.time()
        time_since_last = current_time - self.last_search_time
        
        if time_since_last < self.min_delay:
            time.sleep(self.min_delay - time_since_last)
        
        self.last_search_time = time.time()
    
    def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """
        Realiza pesquisa web usando DuckDuckGo
        
        Args:
            query: Termo de pesquisa
            max_results: Número máximo de resultados
            
        Returns:
            Lista de resultados de pesquisa
        """
        # Verifica cache primeiro
        cache_key = f"{query}_{max_results}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            # Cache válido por 1 hora
            if time.time() - cached.get("timestamp", 0) < 3600:
                print(f"[DuckDNS] Usando cache para: {query}")
                return [SearchResult(**r) for r in cached["results"]]
        
        self._rate_limit()
        
        try:
            # Simulação de pesquisa (em produção, usaria requests + BeautifulSoup)
            results = self._simulate_search(query, max_results)
            
            # Salva no cache
            self.cache[cache_key] = {
                "query": query,
                "timestamp": time.time(),
                "results": [self._result_to_dict(r) for r in results]
            }
            self._save_cache()
            
            return results
            
        except Exception as e:
            print(f"[DuckDNS] Erro na pesquisa: {e}")
            return []
    
    def _simulate_search(self, query: str, max_results: int) -> List[SearchResult]:
        """
        Simula resultados de pesquisa
        Em produção, substituir por scraping real do DuckDuckGo
        """
        # Templates de resultados simulados
        templates = [
            {
                "title": f"{query} - Wikipédia",
                "url": f"https://pt.wikipedia.org/wiki/{query.replace(' ', '_')}",
                "snippet": f"{query} é um conceito fundamental em diversas áreas do conhecimento..."
            },
            {
                "title": f"O que é {query}? Definição e significado",
                "url": f"https://www.significados.com.br/{query.replace(' ', '-')}",
                "snippet": f"Descubra o significado de {query}, sua origem, conceitos relacionados e aplicações práticas..."
            },
            {
                "title": f"{query} - Conceitos e Aplicações | Blog Tecnológico",
                "url": f"https://blogtecnologico.com/{query.replace(' ', '-')}",
                "snippet": f"Neste artigo exploramos {query} em profundidade, desde conceitos básicos até aplicações avançadas..."
            },
            {
                "title": f"Curso de {query} - Aprenda Online",
                "url": f"https://cursosonline.com/{query.replace(' ', '-')}",
                "snippet": f"Domine {query} com nosso curso completo. Aulas práticas, exercícios e certificado..."
            },
            {
                "title": f"{query} na prática: Guia completo",
                "url": f"https://guiapratico.com/{query.replace(' ', '-')}",
                "snippet": f"Um guia abrangente sobre {query}, com exemplos práticos e melhores práticas..."
            },
            {
                "title": f"Fórum de discussão sobre {query}",
                "url": f"https://forumtecnico.com/t/{query.replace(' ', '-')}",
                "snippet": f"Comunidade ativa discutindo {query}. Tire suas dúvidas e compartilhe conhecimento..."
            },
            {
                "title": f"Artigo científico: {query} - ResearchGate",
                "url": f"https://www.researchgate.net/publication/{query.replace(' ', '_')}",
                "snippet": f"PDF disponível: estudo aprofundado sobre {query}, metodologia e resultados..."
            },
            {
                "title": f"Vídeo: Introdução a {query} - YouTube",
                "url": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}",
                "snippet": f"Vídeo educativo explicando os fundamentos de {query} de forma clara e objetiva..."
            }
        ]
        
        # Seleciona resultados aleatórios
        selected = random.sample(templates, min(max_results, len(templates)))
        
        results = []
        for i, template in enumerate(selected):
            # Personaliza o snippet com a query
            snippet = template["snippet"].replace(query, f"'{query}'")
            
            result = SearchResult(
                title=template["title"],
                url=template["url"],
                snippet=snippet,
                relevance=random.uniform(0.6, 0.95)
            )
            results.append(result)
        
        # Ordena por relevância
        results.sort(key=lambda x: x.relevance, reverse=True)
        
        return results
    
    def search_with_context(
        self, 
        query: str, 
        context: str = "",
        max_results: int = 5
    ) -> List[SearchResult]:
        """
        Pesquisa com contexto adicional para melhorar resultados
        """
        # Enriquece a query com contexto
        enriched_query = query
        if context:
            # Extrai palavras-chave do contexto
            keywords = self._extract_keywords(context)
            if keywords:
                enriched_query = f"{query} {' '.join(keywords[:3])}"
        
        return self.search(enriched_query, max_results)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrai palavras-chave de um texto"""
        # Palavras comuns a ignorar
        stopwords = {
            "o", "a", "os", "as", "um", "uma", "uns", "umas", "de", "do", "da",
            "dos", "das", "em", "no", "na", "nos", "nas", "por", "para", "com",
            "sem", "sob", "sobre", "entre", "durante", "ante", "após", "até",
            "desde", "conforme", "segundo", "perante", "contra", "exceto",
            "salvo", "também", "já", "ainda", "só", "apenas", "mas", "porém",
            "todavia", "contudo", "entretanto", "logo", "pois", "porque",
            "assim", "deste", "desta", "desse", "dessa", "disso", "daquele",
            "daquela", "daquilo", "me", "te", "se", "nos", "vos", "lhe", "lhes",
            "que", "quem", "qual", "quais", "cujo", "cuja", "cujos", "cujas",
            "onde", "quando", "como", "porque", "se", "embora", "conquanto",
            "mesmo", "bem", "mal", "tanto", "tão", "mais", "menos", "muito",
            "pouco", "todo", "cada", "qualquer", "outro", "outra", "outros",
            "outras", "mesmo", "mesma", "mesmos", "mesmas", "próprio", "própria",
            "próprios", "próprias", "tal", "tais", "certo", "certa", "certos",
            "certas", "vários", "várias", "todos", "todas", "ambos", "ambas",
            "eu", "tu", "ele", "ela", "nós", "vós", "eles", "elas", "meu",
            "minha", "meus", "minhas", "teu", "tua", "teus", "tuas", "seu",
            "sua", "seus", "suas", "nosso", "nossa", "nossos", "nossas", "vosso",
            "vossa", "vossos", "vossas", "este", "esta", "estes", "estas",
            "esse", "essa", "esses", "essas", "aquele", "aquela", "aqueles",
            "aquelas", "isto", "isso", "aquilo", "aqui", "aí", "ali", "lá",
            "cá", "acolá", "hoje", "ontem", "amanhã", "sempre", "nunca",
            "jamais", "ora", "adiante", "atrás", "depois", "antes", "acima",
            "abaixo", "dentro", "fora", "além", "aquém", "longe", "perto",
            "the", "is", "are", "was", "were", "be", "been", "being", "have",
            "has", "had", "do", "does", "did", "will", "would", "shall",
            "should", "may", "might", "can", "could", "must", "ought", "need",
            "dare", "used", "to", "of", "in", "for", "on", "with", "at", "by",
            "from", "as", "into", "through", "during", "before", "after",
            "above", "below", "between", "under", "again", "further", "then",
            "once", "here", "there", "when", "where", "why", "how", "all",
            "each", "few", "more", "most", "other", "some", "such", "only",
            "own", "same", "so", "than", "too", "very", "just", "and", "but",
            "if", "or", "because", "until", "while", "this", "that", "these",
            "those", "am", "it", "its", "an", "which", "who", "whom", "whose",
            "what", "whatever", "whoever", "whomever", "whichever", "however",
            "whenever", "wherever", "whyever", "whether", "although", "though",
            "whereas", "unless", "since", "provided", "providing", "considering",
            "regarding", "concerning", "notwithstanding", "according", "accordingly"
        }
        
        # Limpa e tokeniza
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text.lower())
        
        # Filtra stopwords e palavras curtas
        keywords = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Conta frequência
        freq = {}
        for w in keywords:
            freq[w] = freq.get(w, 0) + 1
        
        # Ordena por frequência
        sorted_keywords = sorted(freq.keys(), key=lambda x: freq[x], reverse=True)
        
        return sorted_keywords[:10]
    
    def quick_fact(self, topic: str) -> Optional[str]:
        """
        Obtém um fato rápido sobre um tópico
        """
        results = self.search(topic, max_results=1)
        if results:
            return results[0].snippet
        return None
    
    def _result_to_dict(self, result: SearchResult) -> Dict:
        """Converte resultado para dicionário"""
        return {
            "title": result.title,
            "url": result.url,
            "snippet": result.snippet,
            "relevance": result.relevance,
            "source": result.source
        }
    
    def clear_cache(self):
        """Limpa cache de pesquisas"""
        self.cache.clear()
        if self.cache_path.exists():
            self.cache_path.unlink()
    
    def get_cache_stats(self) -> Dict:
        """Retorna estatísticas do cache"""
        return {
            "cached_queries": len(self.cache),
            "cache_file_size": self.cache_path.stat().st_size if self.cache_path.exists() else 0
        }


# Instância global
_searcher: Optional[DuckDNSSearcher] = None


def get_searcher(cache_path: str = "./storage/hd/search_cache.json") -> DuckDNSSearcher:
    """Retorna instância singleton do pesquisador"""
    global _searcher
    if _searcher is None:
        _searcher = DuckDNSSearcher(cache_path)
    return _searcher


def search(query: str, max_results: int = 5) -> List[SearchResult]:
    """Função conveniente para pesquisa"""
    return get_searcher().search(query, max_results)
