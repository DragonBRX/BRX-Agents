# BRX-AGENT v7.0 - Núcleo Principal Aprimorado
# Sistema Multi-Agente com 12 especialistas, consciência expandida e busca web inteligente

import os
import sys
import json
import time
import random
import hashlib
import logging
import sqlite3
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Tuple
from pathlib import Path
from dataclasses import dataclass, field, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter

# Configuração de logging avançado
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m', 'INFO': '\033[32m',
        'WARNING': '\033[33m', 'ERROR': '\033[31m',
        'CRITICAL': '\033[35m\033[1m'
    }
    RESET = '\033[0m'
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)

def setup_logging(level=logging.INFO):
    logger = logging.getLogger("BRXv7")
    logger.setLevel(level)
    logger.handlers = []
    
    fmt = "%(asctime)s | %(levelname)-20s | %(name)s | %(message)s"
    datefmt = "%H:%M:%S"
    
    # Console com cores
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(ColoredFormatter(fmt, datefmt=datefmt))
    logger.addHandler(ch)
    
    return logger

logger = setup_logging()

# ====================================================================================
# CONFIGURAÇÃO GLOBAL v7.0
# ====================================================================================

@dataclass
class BRXConfig:
    """Configuração centralizada do sistema BRX v7.0"""
    VERSION: str = "7.0.0"
    NAME: str = "BRX-Agent Multi-Mente v7.0"
    MAX_WORKERS: int = 12
    TIMEOUT_DEBATE: int = 300
    NUM_RODADAS_PADRAO: int = 20
    PARALELISMO_TOPICO: int = 4
    
    # Thresholds de classificação
    THRESHOLD_POSITIVO: float = 0.60
    THRESHOLD_NEGATIVO: float = 0.35
    PARADA_ANTECIPADA: bool = True
    SCORE_CONVERGENCIA: float = 0.995
    
    # Web Search
    WEB_SEARCH_ENABLED: bool = True
    WEB_SEARCH_TIMEOUT: int = 30
    MAX_RESULTADOS_WEB: int = 8
    CACHE_WEB_TTL: int = 86400
    
    # SQLite
    SQLITE_WAL_MODE: bool = True
    SQLITE_TIMEOUT: int = 30
    
    # Caminhos
    BASE_DIR: Path = field(default_factory=lambda: Path.home() / "BRX-Agent")
    DB_PATH: Path = None
    SAIDA_DIR: Path = None
    LOG_DIR: Path = None
    KNOWLEDGE_BASE: Path = None
    
    def __post_init__(self):
        self.BASE_DIR = Path.home() / "BRX-Agent"
        self.DB_PATH = self.BASE_DIR / "data" / "brx_memory.db"
        self.SAIDA_DIR = self.BASE_DIR / "output"
        self.LOG_DIR = self.BASE_DIR / "logs"
        self.KNOWLEDGE_BASE = Path(__file__).parent / "knowledge_base_v7.json"
        
        for path in [self.BASE_DIR, self.BASE_DIR / "data", self.SAIDA_DIR, self.LOG_DIR]:
            path.mkdir(parents=True, exist_ok=True)

CONFIG = BRXConfig()

# ====================================================================================
# GERENCIADOR DE BANCO DE DADOS v7.0 - SQLite Robusto
# ====================================================================================

class DatabaseManager:
    """Gerenciador SQLite com WAL mode, retry automático e pool de conexões"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.db_path = str(CONFIG.DB_PATH)
        self._local = threading.local()
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Conexão thread-local com WAL e timeout"""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            conn = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=CONFIG.SQLITE_TIMEOUT
            )
            conn.row_factory = sqlite3.Row
            if CONFIG.SQLITE_WAL_MODE:
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                conn.execute("PRAGMA cache_size=10000")
                conn.execute("PRAGMA temp_store=MEMORY")
            self._local.conn = conn
        return self._local.conn
    
    def _executar_com_retry(self, func, max_tentativas: int = 5):
        """Executa operação com retry exponencial"""
        for tentativa in range(max_tentativas):
            try:
                return func()
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and tentativa < max_tentativas - 1:
                    espera = (2 ** tentativa) * 0.1 + random.uniform(0, 0.05)
                    logger.warning(f"DB locked, retry {tentativa+1}/{max_tentativas} em {espera:.2f}s")
                    time.sleep(espera)
                else:
                    raise
    
    def _init_database(self):
        """Inicializa tabelas com índices otimizados"""
        conn = sqlite3.connect(self.db_path, timeout=CONFIG.SQLITE_TIMEOUT)
        if CONFIG.SQLITE_WAL_MODE:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
        cursor = conn.cursor()
        
        # Tabela de parâmetros com metadados ricos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parametros (
            id TEXT PRIMARY KEY,
            topico TEXT NOT NULL,
            tipo_param TEXT NOT NULL,
            conteudo TEXT,
            score REAL DEFAULT 0.0,
            score_detalhado TEXT,
            criados_por TEXT,
            fonte TEXT DEFAULT 'gerado',
            url_fonte TEXT,
            validado INTEGER DEFAULT 0,
            usos INTEGER DEFAULT 0,
            timestamp REAL,
            rodada_debate INTEGER DEFAULT 1,
            tags TEXT,
            confianca REAL DEFAULT 0.5
        )""")
        
        # Tabela de críticas com análise de qualidade
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS criticas (
            id TEXT PRIMARY KEY,
            parametro_id TEXT,
            de_agente TEXT NOT NULL,
            para_agente TEXT NOT NULL,
            para_topico TEXT NOT NULL,
            tipo_critica TEXT DEFAULT 'construtiva',
            pontos_positivos TEXT,
            pontos_negativos TEXT,
            sugestoes TEXT,
            score_qualidade REAL DEFAULT 0.5,
            timestamp REAL,
            rodada INTEGER DEFAULT 1,
            impacto_score REAL DEFAULT 0.0
        )""")
        
        # Tabela de ciclos de debate
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ciclos_debate (
            id TEXT PRIMARY KEY,
            topico TEXT NOT NULL,
            rodada INTEGER DEFAULT 1,
            num_criticas INTEGER DEFAULT 0,
            consenso_final TEXT,
            score_consenso REAL DEFAULT 0.0,
            agentes_participantes TEXT,
            timestamp_inicio REAL,
            timestamp_fim REAL,
            duracao_segundos REAL,
            status TEXT DEFAULT 'em_andamento'
        )""")
        
        # Tabela de memória global com embeddings simulados
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memoria_global (
            id TEXT PRIMARY KEY,
            tipo TEXT NOT NULL,
            dados TEXT NOT NULL,
            relevancia REAL DEFAULT 1.0,
            acessos INTEGER DEFAULT 0,
            ultima_atualizacao REAL,
            tags TEXT,
            topico_relacionado TEXT,
            fonte TEXT,
            agente_origem TEXT,
            embedding_simulado TEXT
        )""")
        
        # Tabela de performance de agentes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agente_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agente_nome TEXT NOT NULL,
            agente_id INTEGER NOT NULL,
            total_debates INTEGER DEFAULT 0,
            total_criticas_geradas INTEGER DEFAULT 0,
            score_medio REAL DEFAULT 0.5,
            acuracia REAL DEFAULT 0.5,
            credibilidade REAL DEFAULT 1.0,
            acertos INTEGER DEFAULT 0,
            erros INTEGER DEFAULT 0,
            primeiro_debate REAL,
            ultimo_debate REAL
        )""")
        
        # Tabela de cache de busca web
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS busca_web_cache (
            id TEXT PRIMARY KEY,
            query TEXT NOT NULL UNIQUE,
            resultados TEXT NOT NULL,
            timestamp REAL,
            ttl INTEGER DEFAULT 86400,
            usos INTEGER DEFAULT 0
        )""")
        
        # Tabela de tokens de treinamento
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens_treinamento (
            id TEXT PRIMARY KEY,
            tipo TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            topico TEXT,
            agente_origem TEXT,
            score REAL DEFAULT 0.0,
            timestamp REAL,
            usado INTEGER DEFAULT 0,
            embedding TEXT
        )""")
        
        # Índices otimizados
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_param_topico ON parametros(topico)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_param_tipo ON parametros(tipo_param)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_param_score ON parametros(score)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_param_tags ON parametros(tags)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_criticas_de ON criticas(de_agente)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memoria_topico ON memoria_global(topico_relacionado)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tokens_tipo ON tokens_treinamento(tipo)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tokens_topico ON tokens_treinamento(topico)")
        
        conn.commit()
        conn.close()
        logger.info("Banco de dados v7.0 inicializado (WAL mode ativo)")
    
    # === OPERAÇÕES DE PARÂMETROS ===
    
    def salvar_parametro(self, topico, tipo, conteudo, score, criados_por,
                         fonte="gerado", rodada=1, url_fonte=None, 
                         score_detalhado=None, tags=None, confianca=0.5) -> str:
        param_id = hashlib.sha256(f"{tipo}_{topico}_{time.time()}_{random.randint(1000,9999)}".encode()).hexdigest()[:16]
        
        def _op():
            conn = self._get_connection()
            conn.execute("""
            INSERT OR IGNORE INTO parametros
            (id, topico, tipo_param, conteudo, score, score_detalhado, criados_por, 
             fonte, url_fonte, timestamp, rodada_debate, tags, confianca)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (param_id, topico, tipo, json.dumps(conteudo), score,
                  json.dumps(score_detalhado) if score_detalhado else None,
                  ','.join(criados_por) if isinstance(criados_por, list) else criados_por,
                  fonte, url_fonte, time.time(), rodada, 
                  ','.join(tags) if tags else None, confianca))
            conn.commit()
        
        self._executar_com_retry(_op)
        return param_id
    
    def buscar_parametros(self, topico=None, tipo=None, min_score=None, tags=None, limit=100) -> List[Dict]:
        conn = self._get_connection()
        query = "SELECT * FROM parametros WHERE 1=1"
        params = []
        
        if topico:
            query += " AND topico = ?"
            params.append(topico)
        if tipo:
            query += " AND tipo_param = ?"
            params.append(tipo)
        if min_score is not None:
            query += " AND score >= ?"
            params.append(min_score)
        if tags:
            query += " AND tags LIKE ?"
            params.append(f"%{tags}%")
        
        query += " ORDER BY score DESC, confianca DESC LIMIT ?"
        params.append(limit)
        
        rows = conn.execute(query, params).fetchall()
        return [{
            'id': r['id'], 'topico': r['topico'], 'tipo': r['tipo_param'],
            'conteudo': json.loads(r['conteudo']) if r['conteudo'] else {},
            'score': r['score'], 'confianca': r['confianca'],
            'criados_por': r['criados_por'].split(',') if r['criados_por'] else [],
            'tags': r['tags'].split(',') if r['tags'] else [],
            'timestamp': r['timestamp']
        } for r in rows]
    
    # === OPERAÇÕES DE TOKENS ===
    
    def salvar_token_treinamento(self, tipo, conteudo, topico=None, agente_origem=None, score=0.0) -> str:
        token_id = hashlib.sha256(f"token_{tipo}_{time.time()}".encode()).hexdigest()[:16]
        
        def _op():
            conn = self._get_connection()
            conn.execute("""
            INSERT INTO tokens_treinamento (id, tipo, conteudo, topico, agente_origem, score, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (token_id, tipo, json.dumps(conteudo), topico, agente_origem, score, time.time()))
            conn.commit()
        
        self._executar_com_retry(_op)
        return token_id
    
    def buscar_tokens_treinamento(self, tipo=None, topico=None, limit=100) -> List[Dict]:
        conn = self._get_connection()
        query = "SELECT * FROM tokens_treinamento WHERE usado = 0"
        params = []
        
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo)
        if topico:
            query += " AND topico = ?"
            params.append(topico)
        
        query += " ORDER BY score DESC LIMIT ?"
        params.append(limit)
        
        rows = conn.execute(query, params).fetchall()
        return [{
            'id': r['id'], 'tipo': r['tipo'],
            'conteudo': json.loads(r['conteudo']) if r['conteudo'] else {},
            'topico': r['topico'], 'agente_origem': r['agente_origem'],
            'score': r['score'], 'timestamp': r['timestamp']
        } for r in rows]
    
    def marcar_token_usado(self, token_id):
        def _op():
            conn = self._get_connection()
            conn.execute("UPDATE tokens_treinamento SET usado = 1 WHERE id = ?", (token_id,))
            conn.commit()
        self._executar_com_retry(_op)
    
    # === ESTATÍSTICAS ===
    
    def get_estatisticas(self) -> Dict:
        conn = self._get_connection()
        return {
            'total_parametros': conn.execute("SELECT COUNT(*) FROM parametros").fetchone()[0],
            'total_criticas': conn.execute("SELECT COUNT(*) FROM criticas").fetchone()[0],
            'total_debates': conn.execute("SELECT COUNT(*) FROM ciclos_debate").fetchone()[0],
            'total_memorias': conn.execute("SELECT COUNT(*) FROM memoria_global").fetchone()[0],
            'total_tokens': conn.execute("SELECT COUNT(*) FROM tokens_treinamento").fetchone()[0],
            'tokens_usados': conn.execute("SELECT COUNT(*) FROM tokens_treinamento WHERE usado = 1").fetchone()[0],
            'score_medio_geral': round(
                conn.execute("SELECT AVG(score) FROM parametros").fetchone()[0] or 0, 4
            )
        }

# Instância global do banco de dados
db = DatabaseManager()

# ====================================================================================
# BUSCA WEB v7.0 - DuckDuckGo Aprimorado
# ====================================================================================

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

class WebSearchEngine:
    """Motor de busca DuckDuckGo com múltiplas estratégias e cache inteligente"""
    
    DDG_URLS = [
        "https://html.duckduckgo.com/html/?q={query}",
        "https://lite.duckduckgo.com/lite/?q={query}",
    ]
    
    HEADERS_LIST = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
        },
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        }
    ]
    
    def __init__(self):
        self.enabled = CONFIG.WEB_SEARCH_ENABLED and REQUESTS_AVAILABLE
        self.timeout = CONFIG.WEB_SEARCH_TIMEOUT
        self.max_resultados = CONFIG.MAX_RESULTADOS_WEB
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
            self.session.headers.update(self.HEADERS_LIST[0])
        else:
            self.session = None
    
    def buscar(self, query: str, use_cache: bool = True) -> List[Dict]:
        """Busca no DuckDuckGo com cache e múltiplas estratégias"""
        if not self.enabled:
            logger.warning("Busca web desabilitada")
            return []
        
        if use_cache:
            cached = self._get_cache_busca(query)
            if cached:
                logger.info(f"Cache hit: {query[:50]}...")
                return cached
        
        query_encoded = requests.utils.quote(query)
        resultados = []
        
        for url_template in self.DDG_URLS:
            url = url_template.format(query=query_encoded)
            for headers in self.HEADERS_LIST:
                try:
                    logger.info(f"Buscando: {query[:50]}...")
                    resp = self.session.get(url, headers=headers, timeout=self.timeout)
                    resp.raise_for_status()
                    
                    resultados = self._parse_automatico(resp.text, url)
                    if resultados:
                        break
                    time.sleep(0.5)
                except Exception as e:
                    logger.warning(f"Erro de busca: {type(e).__name__}: {e}")
            
            if resultados:
                break
        
        if resultados and use_cache:
            self._salvar_cache_busca(query, resultados)
        
        return resultados
    
    def _parse_automatico(self, html: str, url: str) -> List[Dict]:
        """Parse automático com múltiplas estratégias"""
        if not html or len(html) < 200:
            return []
        
        if "lite.duckduckgo.com" in url:
            return self._parse_lite(html)
        
        if BS4_AVAILABLE:
            resultados = self._parse_bs4(html)
            if resultados:
                return resultados
        
        return self._parse_regex_robusto(html)
    
    def _parse_bs4(self, html: str) -> List[Dict]:
        """Parse com BeautifulSoup"""
        resultados = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            seletores = [
                ('div', {'class': 'result'}),
                ('div', {'class': 'results_links'}),
                ('article', {}),
            ]
            
            for tag, attrs in seletores:
                items = soup.find_all(tag, attrs)[:self.max_resultados]
                if not items:
                    continue
                for item in items:
                    titulo_tag = (
                        item.find('a', class_='result__a') or
                        item.find('h2') or
                        item.find('a')
                    )
                    snippet_tag = (
                        item.find('a', class_='result__snippet') or
                        item.find('p') or
                        item.find(class_=re.compile(r'snippet|description|abstract'))
                    )
                    if titulo_tag:
                        resultados.append({
                            'titulo': titulo_tag.get_text(strip=True),
                            'url': titulo_tag.get('href', ''),
                            'snippet': snippet_tag.get_text(strip=True) if snippet_tag else ''
                        })
                if resultados:
                    break
        except Exception as e:
            logger.debug(f"BS4 parse error: {e}")
        return resultados
    
    def _parse_regex_robusto(self, html: str) -> List[Dict]:
        """Parse via regex robusto"""
        resultados = []
        html_limpo = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html_limpo = re.sub(r'<style[^>]*>.*?</style>', '', html_limpo, flags=re.DOTALL | re.IGNORECASE)
        
        padroes_titulo = [
            r'class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
            r'<a[^>]+class="[^"]*result[^"]*"[^>]+href="([^"]*)"[^>]*>(.*?)</a>',
        ]
        
        padroes_snippet = [
            r'class="result__snippet"[^>]*>(.*?)</a>',
            r'<a[^>]+class="[^"]*snippet[^"]*"[^>]*>(.*?)</a>',
        ]
        
        titulos_urls = []
        for padrao in padroes_titulo:
            matches = re.findall(padrao, html_limpo, re.DOTALL | re.IGNORECASE)
            if matches:
                titulos_urls = [(url, re.sub(r'<[^>]+>', '', titulo).strip())
                                for url, titulo in matches if titulo.strip()]
                if titulos_urls:
                    break
        
        snippets = []
        for padrao in padroes_snippet:
            matches = re.findall(padrao, html_limpo, re.DOTALL | re.IGNORECASE)
            if matches:
                snippets = [re.sub(r'<[^>]+>', '', s).strip() for s in matches if s.strip()]
                break
        
        for i, (url, titulo) in enumerate(titulos_urls[:self.max_resultados]):
            resultados.append({
                'titulo': titulo[:200],
                'url': url[:500],
                'snippet': snippets[i][:300] if i < len(snippets) else ''
            })
        
        return resultados
    
    def _parse_lite(self, html: str) -> List[Dict]:
        """Parse do DDG Lite"""
        resultados = []
        links = re.findall(
            r'<a[^>]+class="result-link"[^>]+href="([^"]*)"[^>]*>(.*?)</a>',
            html, re.DOTALL | re.IGNORECASE
        )
        snippets = re.findall(
            r'<td[^>]+class="result-snippet"[^>]*>(.*?)</td>',
            html, re.DOTALL | re.IGNORECASE
        )
        
        if not links:
            links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>',
                               html, re.DOTALL | re.IGNORECASE)
        
        for i, (url, titulo) in enumerate(links[:self.max_resultados]):
            titulo_limpo = re.sub(r'<[^>]+>', '', titulo).strip()
            snippet_limpo = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ''
            if titulo_limpo and len(titulo_limpo) > 3:
                resultados.append({
                    'titulo': titulo_limpo[:200],
                    'url': url[:500],
                    'snippet': snippet_limpo[:300]
                })
        
        return resultados
    
    def _get_cache_busca(self, query) -> Optional[List[Dict]]:
        conn = db._get_connection()
        row = conn.execute("SELECT * FROM busca_web_cache WHERE query = ?", (query,)).fetchone()
        if row and (time.time() - row['timestamp'] < row['ttl']):
            conn.execute("UPDATE busca_web_cache SET usos = usos + 1 WHERE id = ?", (row['id'],))
            conn.commit()
            return json.loads(row['resultados'])
        return None
    
    def _salvar_cache_busca(self, query, resultados, ttl=86400):
        cache_id = hashlib.sha256(f"cache_{query}_{time.time()}".encode()).hexdigest()[:16]
        def _op():
            conn = db._get_connection()
            conn.execute("""
            INSERT OR REPLACE INTO busca_web_cache (id, query, resultados, timestamp, ttl)
            VALUES (?, ?, ?, ?, ?)
            """, (cache_id, query, json.dumps(resultados), time.time(), ttl))
            conn.commit()
        db._executar_com_retry(_op)
    
    def buscar_e_resumir(self, query: str, topico: str) -> str:
        """Busca e resume resultados com contexto"""
        resultados = self.buscar(query)
        if not resultados:
            return ""
        
        texto = f"Informações da web sobre {topico}:\n\n"
        for i, r in enumerate(resultados[:3], 1):
            titulo = r.get('titulo', '')
            snippet = r.get('snippet', '')
            if titulo or snippet:
                texto += f"{i}. {titulo}: {snippet}\n"
        
        # Salva na memória global
        conn = db._get_connection()
        mem_id = hashlib.sha256(f"memoria_web_{time.time()}".encode()).hexdigest()[:16]
        conn.execute("""
        INSERT INTO memoria_global (id, tipo, dados, relevancia, tags, topico_relacionado, fonte, ultima_atualizacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (mem_id, 'busca_web', json.dumps({'query': query, 'resultados': resultados}), 
              0.8, 'web,pesquisa', topico, 'duckduckgo', time.time()))
        conn.commit()
        
        return texto

web_search = WebSearchEngine()

# ====================================================================================
# AGENTES v7.0 - 12 Especialistas
# ====================================================================================

@dataclass
class Personalidade:
    criatividade: float = 0.5
    rigor: float = 0.5
    colaboracao: float = 0.5
    foco: str = "geral"

@dataclass
class EstadoAgente:
    parametros_locais: Dict = field(default_factory=dict)
    criticas_geradas: List = field(default_factory=list)
    criticas_recebidas: List = field(default_factory=list)
    opiniao_consenso: Dict = field(default_factory=dict)
    score_credibilidade: float = 1.0
    historico_acertos: int = 0
    historico_erros: int = 0

class AgenteAutonomo:
    """Classe base para todos os agentes"""
    
    def __init__(self, id_agente: int, nome: str, especialidade: str, personalidade: Personalidade = None):
        self.id = id_agente
        self.nome = nome
        self.especialidade = especialidade
        self.personalidade = personalidade or Personalidade()
        self.estado = EstadoAgente()
        self.logger = logging.getLogger(f"agente.{nome}")
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        raise NotImplementedError
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        raise NotImplementedError
    
    def processar(self, conteudo: str, topico: str, memoria: List[Dict] = None) -> Dict:
        self.logger.info(f"{self.nome} processando '{topico}'")
        contexto = {'memoria': memoria or []}
        analise = self.analisar(conteudo, topico, contexto)
        
        score_analise = analise.get('score_principal', 0.5)
        score_base = float(score_analise) * 0.6 + random.uniform(0.35, 0.65) * 0.4
        score_base = max(0.35, min(0.95, score_base * self.estado.score_credibilidade))
        
        self.estado.parametros_locais = {
            'agente_id': self.id,
            'agente_nome': self.nome,
            'especialidade': self.especialidade,
            'topico': topico,
            'analise': analise,
            'timestamp': time.time(),
            'score_inicial': score_base
        }
        return self.estado.parametros_locais
    
    def criticar(self, agente_outro: 'AgenteAutonomo') -> Dict:
        critica = self.gerar_critica(agente_outro.estado.parametros_locais, agente_outro)
        self.estado.criticas_geradas.append(critica)
        return critica
    
    def receber_critica(self, critica: Dict):
        self.estado.criticas_recebidas.append(critica)
    
    def formar_consenso(self) -> Dict:
        score_total = self.estado.parametros_locais.get('score_inicial', 0.55)
        ajustes = []
        
        for critica in self.estado.criticas_recebidas:
            peso = min(1.0, max(0.1, critica.get('score_qualidade', 0.5)))
            n_neg = len(critica.get('pontos_negativos', []))
            n_pos = len(critica.get('pontos_positivos', []))
            
            impacto_neg = min(0.03, n_neg * peso * 0.008)
            impacto_pos = min(0.02, n_pos * peso * 0.005)
            
            score_total -= impacto_neg
            score_total += impacto_pos
            
            if n_neg > 0:
                ajustes.append(f"{critica['de_agente']}: -{impacto_neg:.4f}")
        
        score_total = max(0.30, min(0.97, score_total))
        
        self.estado.opiniao_consenso = {
            'agente': self.nome,
            'score_final': round(score_total, 4),
            'ajustes_aplicados': len(ajustes),
            'credibilidade': self.estado.score_credibilidade,
            'detalhes_ajustes': ajustes[:5]
        }
        return self.estado.opiniao_consenso

# AGENTE 1: ENGENHEIRO DE SOFTWARE
class AgenteEngenheiro(AgenteAutonomo):
    def __init__(self):
        super().__init__(1, "Engenheiro", "Arquitetura de software", 
                        Personalidade(criatividade=0.65, rigor=0.95, foco="arquitetura"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        patterns = ['singleton', 'factory', 'observer', 'strategy']
        found_patterns = [p for p in patterns if p in conteudo.lower()]
        modulos = conteudo.count('def ') + conteudo.count('class ')
        score = min(1.0, max(0.30, len(found_patterns) * 0.15 + min(1.0, modulos / 5) * 0.4 + 0.3))
        
        return {
            'design_patterns': found_patterns,
            'modularidade': min(1.0, modulos / 5),
            'score_principal': round(score, 4),
            'recomendacoes': [f"Aplicar {p}" for p in patterns if p not in found_patterns][:2]
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        pos, neg, sug = [], [], []
        score = analise.get('score_principal', 0.5)
        
        if score > 0.6:
            pos.append(f"Arquitetura sólida ({score:.0%})")
        else:
            neg.append(f"Arquitetura precisa de melhorias ({score:.0%})")
            sug.append("Aplicar mais design patterns")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 2: CIENTISTA DE DADOS
class AgenteCientistaDados(AgenteAutonomo):
    def __init__(self):
        super().__init__(2, "CientistaDados", "Análise estatística",
                        Personalidade(criatividade=0.5, rigor=0.98, foco="dados"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        termos = ['media', 'mediana', 'correlacao', 'regressao']
        found = [t for t in termos if t in conteudo.lower()]
        palavras = conteudo.split()
        ttr = len(set(p.lower() for p in palavras)) / max(1, len(palavras))
        score = min(1.0, max(0.30, ttr * 0.35 + len(found) * 0.1 + 0.25))
        
        return {
            'termos_estatisticos': found,
            'type_token_ratio': round(ttr, 4),
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f"Rigor estatístico adequado ({score:.0%})")
        else:
            neg.append(f"Rigor estatístico baixo ({score:.0%})")
            sug.append("Incluir métricas quantitativas")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 3: CISO
class AgenteCISO(AgenteAutonomo):
    def __init__(self):
        super().__init__(3, "CISO", "Segurança e riscos",
                        Personalidade(criatividade=0.7, rigor=0.98, foco="seguranca"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        palavras_risco = ['senha', 'token', 'api_key', 'criptograf']
        controles = ['autenticacao', 'autorizacao', 'audit']
        riscos = [p for p in palavras_risco if p in conteudo.lower()]
        ctrls = [c for c in controles if c in conteudo.lower()]
        score = min(1.0, max(0.30, len(ctrls) * 0.15 + (0.3 if not riscos else 0.1) + 0.3))
        
        return {
            'dados_sensiveis': riscos,
            'controles': ctrls,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f"Postura de segurança adequada ({score:.0%})")
        else:
            neg.append(f"Riscos de segurança identificados ({score:.0%})")
            sug.append("Implementar controles de segurança")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 4: ECONOMISTA
class AgenteEconomista(AgenteAutonomo):
    def __init__(self):
        super().__init__(4, "Economista", "Viabilidade financeira",
                        Personalidade(criatividade=0.6, rigor=0.92, foco="economia"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        termos = ['roi', 'custo', 'lucro', 'investimento']
        found = [t for t in termos if t in conteudo.lower()]
        score = min(1.0, max(0.30, len(found) * 0.15 + 0.4))
        
        return {
            'termos_economicos': found,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f"Viabilidade econômica positiva ({score:.0%})")
        else:
            neg.append(f"Viabilidade econômica questionável ({score:.0%})")
            sug.append("Mapear custos e retornos")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 5: PSICÓLOGO/UX
class AgentePsicologo(AgenteAutonomo):
    def __init__(self):
        super().__init__(5, "Psicologo", "Experiência do usuário",
                        Personalidade(criatividade=0.8, rigor=0.82, foco="ux"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        indicadores = ['simples', 'claro', 'intuitivo']
        found = [i for i in indicadores if i in conteudo.lower()]
        score = min(1.0, max(0.30, len(found) * 0.2 + 0.4))
        
        return {
            'indicadores_ux': found,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f"Boa experiência do usuário ({score:.0%})")
        else:
            neg.append(f"Experiência do usuário pode melhorar ({score:.0%})")
            sug.append("Simplificar interface e fluxos")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 6: FILÓSOFO
class AgenteFilosofo(AgenteAutonomo):
    def __init__(self):
        super().__init__(6, "Filosofo", "Ética e lógica",
                        Personalidade(criatividade=0.75, rigor=0.93, foco="etica"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        termos = ['etico', 'moral', 'responsabilidade', 'justo']
        found = [t for t in termos if t in conteudo.lower()]
        score = min(1.0, max(0.25, len(found) * 0.15 + 0.4))
        
        return {
            'consideracoes_eticas': found,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.5:
            pos.append(f"Dimensão ética considerada ({score:.0%})")
        else:
            neg.append(f"Aspectos éticos não abordados ({score:.0%})")
            sug.append("Incluir análise de impacto ético")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 7: CPO
class AgenteCPO(AgenteAutonomo):
    def __init__(self):
        super().__init__(7, "CPO", "Estratégia de produto",
                        Personalidade(criatividade=0.88, rigor=0.78, foco="produto"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        termos = ['produto', 'usuario', 'mercado', 'feature']
        found = [t for t in termos if t in conteudo.lower()]
        score = min(1.0, max(0.30, len(found) * 0.15 + 0.35))
        
        return {
            'termos_produto': found,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f"Boa visão de produto ({score:.0%})")
        else:
            neg.append(f"Visão de produto insuficiente ({score:.0%})")
            sug.append("Definir problema e mercado-alvo")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 8: PESQUISADOR ML
class AgentePesquisadorML(AgenteAutonomo):
    def __init__(self):
        super().__init__(8, "PesquisadorML", "Machine Learning",
                        Personalidade(criatividade=0.82, rigor=0.96, foco="ml"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        termos = ['modelo', 'treino', 'dataset', 'feature']
        found = [t for t in termos if t in conteudo.lower()]
        score = min(1.0, max(0.30, len(found) * 0.15 + 0.35))
        
        return {
            'termos_ml': found,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f"Boa abordagem de ML ({score:.0%})")
        else:
            neg.append(f("Abordagem de ML pode melhorar ({score:.0%})"))
            sug.append("Definir métricas e baseline")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 9: DEVOPS ENGINEER (NOVO)
class AgenteDevOps(AgenteAutonomo):
    def __init__(self):
        super().__init__(9, "DevOps", "Infraestrutura e CI/CD",
                        Personalidade(criatividade=0.7, rigor=0.9, foco="devops"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        termos = ['docker', 'kubernetes', 'ci/cd', 'pipeline', 'deploy']
        found = [t for t in termos if t in conteudo.lower()]
        score = min(1.0, max(0.30, len(found) * 0.15 + 0.35))
        
        return {
            'termos_devops': found,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f"Boa prática DevOps ({score:.0%})")
        else:
            neg.append(f"Práticas DevOps insuficientes ({score:.0%})")
            sug.append("Implementar CI/CD e automação")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 10: BLOCKCHAIN SPECIALIST (NOVO)
class AgenteBlockchain(AgenteAutonomo):
    def __init__(self):
        super().__init__(10, "Blockchain", "Tecnologia blockchain",
                        Personalidade(criatividade=0.75, rigor=0.88, foco="blockchain"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        termos = ['blockchain', 'smart_contract', 'defi', 'nft', 'consensus']
        found = [t for t in termos if t in conteudo.lower()]
        score = min(1.0, max(0.30, len(found) * 0.15 + 0.35))
        
        return {
            'termos_blockchain': found,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f("Boa abordagem blockchain ({score:.0%})"))
        else:
            neg.append(f("Abordagem blockchain pode melhorar ({score:.0%})"))
            sug.append("Considerar governança e segurança")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 11: CLOUD ARCHITECT (NOVO)
class AgenteCloud(AgenteAutonomo):
    def __init__(self):
        super().__init__(11, "CloudArchitect", "Computação em nuvem",
                        Personalidade(criatividade=0.72, rigor=0.9, foco="cloud"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        termos = ['aws', 'azure', 'gcp', 'serverless', 'scalable']
        found = [t for t in termos if t in conteudo.lower()]
        score = min(1.0, max(0.30, len(found) * 0.15 + 0.35))
        
        return {
            'termos_cloud': found,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f("Boa arquitetura cloud ({score:.0%})"))
        else:
            neg.append(f("Arquitetura cloud pode melhorar ({score:.0%})"))
            sug.append("Considerar multi-cloud e auto-scaling")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# AGENTE 12: DATA ENGINEER (NOVO)
class AgenteDataEngineer(AgenteAutonomo):
    def __init__(self):
        super().__init__(12, "DataEngineer", "Engenharia de dados",
                        Personalidade(criatividade=0.68, rigor=0.92, foco="data_engineering"))
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        termos = ['etl', 'pipeline', 'data_warehouse', 'streaming', 'batch']
        found = [t for t in termos if t in conteudo.lower()]
        score = min(1.0, max(0.30, len(found) * 0.15 + 0.35))
        
        return {
            'termos_data': found,
            'score_principal': round(score, 4)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        analise = param_outro.get('analise', {})
        score = analise.get('score_principal', 0.5)
        pos, neg, sug = [], [], []
        
        if score > 0.6:
            pos.append(f("Boa engenharia de dados ({score:.0%})"))
        else:
            neg.append(f("Engenharia de dados pode melhorar ({score:.0%})"))
            sug.append("Implementar pipelines e governança")
        
        return {
            'de_agente': self.nome, 'para_agente': agente_outro.nome,
            'pontos_positivos': pos, 'pontos_negativos': neg, 'sugestoes': sug,
            'score_qualidade': max(0.35, min(0.95, score))
        }

# ====================================================================================
# FÁBRICA DE AGENTES v7.0
# ====================================================================================

class AgentFactory:
    AGENTES = {
        1: AgenteEngenheiro, 2: AgenteCientistaDados, 3: AgenteCISO,
        4: AgenteEconomista, 5: AgentePsicologo, 6: AgenteFilosofo,
        7: AgenteCPO, 8: AgentePesquisadorML, 9: AgenteDevOps,
        10: AgenteBlockchain, 11: AgenteCloud, 12: AgenteDataEngineer
    }
    
    @classmethod
    def criar_todos(cls) -> List[AgenteAutonomo]:
        return [cls.criar(i) for i in range(1, 13)]
    
    @classmethod
    def criar(cls, agente_id: int) -> AgenteAutonomo:
        if agente_id not in cls.AGENTES:
            raise ValueError(f"Agente {agente_id} inválido. IDs: 1-12")
        return cls.AGENTES[agente_id]()

# ====================================================================================
# SALA DE DEBATE v7.0
# ====================================================================================

class SalaDebate:
    def __init__(self, usar_web_search: bool = True):
        self.agentes = AgentFactory.criar_todos()
        self.historico_criticas = []
        self.consenso_global = None
        self.rodada_atual = 0
        self.usar_web_search = usar_web_search
        self.debate_id = None
    
    def iniciar_debate(self, conteudo: str, topico: str, num_rodadas: int = 20) -> Dict:
        logger.info(f"Debate: '{topico}' ({num_rodadas} rodadas, 12 agentes)")
        
        # Busca web para enriquecer contexto
        if self.usar_web_search:
            logger.info("Buscando informações na web...")
            info_web = web_search.buscar_e_resumir(topico, topico)
            if info_web:
                conteudo += f"\n\n[Web]:\n{info_web}"
        
        # Recupera memória
        conn = db._get_connection()
        memoria = conn.execute(
            "SELECT * FROM memoria_global WHERE topico_relacionado = ? ORDER BY relevancia DESC LIMIT 20",
            (topico,)
        ).fetchall()
        memoria = [{'tipo': m['tipo'], 'dados': json.loads(m['dados'])} for m in memoria]
        
        # Fase 1: Processamento paralelo
        logger.info("[Fase 1] Processamento paralelo dos 12 agentes...")
        self._fase_processamento(conteudo, topico, memoria)
        
        # Fase 2: Ciclos de crítica
        logger.info("[Fase 2] Ciclos de crítica...")
        self._fase_criticas(num_rodadas)
        
        # Fase 3: Consenso
        logger.info("[Fase 3] Formação de consenso...")
        self._fase_consenso(topico)
        
        logger.info(f"Debate concluído: {len(self.historico_criticas)} críticas totais")
        return self.consenso_global
    
    def _fase_processamento(self, conteudo: str, topico: str, memoria: List[Dict]):
        def processar(agente):
            try:
                return agente.processar(conteudo, topico, memoria)
            except Exception as e:
                logger.error(f"Erro em {agente.nome}: {e}")
                return None
        
        with ThreadPoolExecutor(max_workers=CONFIG.MAX_WORKERS) as ex:
            futures = {ex.submit(processar, a): a for a in self.agentes}
            for f in as_completed(futures):
                agente = futures[f]
                if f.result():
                    logger.info(f"  ✓ {agente.nome} processou")
    
    def _fase_criticas(self, num_rodadas: int):
        for rodada in range(num_rodadas):
            self.rodada_atual = rodada + 1
            
            # Verifica convergência após rodada 10
            if CONFIG.PARADA_ANTECIPADA and rodada >= 10:
                scores = [a.estado.parametros_locais.get('score_inicial', 0.5) for a in self.agentes]
                score_medio = sum(scores) / len(scores)
                if score_medio > CONFIG.SCORE_CONVERGENCIA:
                    logger.info(f"  Convergência na rodada {rodada + 1} (score={score_medio:.2%})")
                    break
            
            criticas_rodada = []
            for a1 in self.agentes:
                for a2 in self.agentes:
                    if a1.id != a2.id:
                        critica = a1.criticar(a2)
                        a2.receber_critica(critica)
                        criticas_rodada.append(critica)
            
            self.historico_criticas.extend(criticas_rodada)
            if (rodada + 1) % 5 == 0:
                logger.info(f"  ✓ Rodada {rodada + 1}: {len(criticas_rodada)} críticas")
    
    def _fase_consenso(self, topico: str):
        consensos = []
        for agente in self.agentes:
            opiniao = agente.formar_consenso()
            consensos.append(opiniao)
        
        scores = [c['score_final'] for c in consensos]
        score_medio = sum(scores) / len(scores) if scores else 0.5
        
        self.consenso_global = {
            'topico': topico,
            'score_medio': score_medio,
            'consensos_agentes': consensos,
            'num_criticas_totais': len(self.historico_criticas),
            'num_agentes': 12,
            'timestamp': time.time()
        }

# ====================================================================================
# ORQUESTRADOR PRINCIPAL v7.0
# ====================================================================================

class OrquestradorBRX:
    """Orquestrador principal do sistema BRX v7.0"""
    
    TOPICOS_PADRAO = [
        "python_avancado", "docker_kubernetes", "aws_cloud",
        "machine_learning", "sql_otimizado", "blockchain_cripto",
        "cybersecurity_defesa", "api_rest_graphql", "arquitetura_software",
        "performance_tuning", "devops_ci_cd", "microservicos",
        "data_engineering", "cloud_native", "ethical_ai"
    ]
    
    def __init__(self, usar_web_search: bool = True):
        self.usar_web_search = usar_web_search
    
    def executar(self, topicos: List[str] = None, num_rodadas: int = 20) -> List[Dict]:
        topicos = topicos or self.TOPICOS_PADRAO
        
        self._mostrar_banner()
        
        stats = db.get_estatisticas()
        logger.info(f"BD: {stats['total_parametros']} parâmetros | {stats['total_tokens']} tokens")
        
        resultados = []
        with ThreadPoolExecutor(max_workers=CONFIG.PARALELISMO_TOPICO) as ex:
            futures = {ex.submit(self._processar_topico, t, num_rodadas): t for t in topicos}
            for f in as_completed(futures):
                topico = futures[f]
                try:
                    resultado = f.result()
                    resultados.append(resultado)
                    logger.info(f"\nCONCLUÍDO: {topico.upper()} | Score: {resultado['score_consenso']:.2%}")
                except Exception as e:
                    logger.error(f"\nERRO em {topico}: {e}")
        
        self._salvar_tokens_treinamento(resultados)
        return resultados
    
    def _processar_topico(self, topico: str, num_rodadas: int) -> Dict:
        sala = SalaDebate(usar_web_search=self.usar_web_search)
        consenso = sala.iniciar_debate(self._gerar_conteudo_base(topico), topico, num_rodadas)
        
        # Classifica parâmetros
        positivos, negativos, incertos = [], [], []
        for agente in sala.agentes:
            opiniao = agente.estado.opiniao_consenso
            score = opiniao.get('score_final', 0.5)
            p = {
                'agente': agente.nome, 'agente_id': agente.id,
                'topico': topico, 'score': score
            }
            
            if score >= CONFIG.THRESHOLD_POSITIVO:
                p['tipo'] = 'positivo'
                positivos.append(p)
            elif score <= CONFIG.THRESHOLD_NEGATIVO:
                p['tipo'] = 'negativo'
                negativos.append(p)
            else:
                p['tipo'] = 'incerto'
                incertos.append(p)
        
        # Salva parâmetros no banco
        for p in positivos:
            db.salvar_parametro(topico, 'positivo', p, p['score'], [p['agente']], 
                              tags=['positivo', p['agente']], confianca=0.8)
        for n in negativos:
            db.salvar_parametro(topico, 'negativo', n, n['score'], [n['agente']], 
                              tags=['negativo', n['agente']], confianca=0.6)
        for i in incertos:
            db.salvar_parametro(topico, 'incerto', i, i['score'], [i['agente']], 
                              tags=['incerto', i['agente']], confianca=0.4)
        
        return {
            'topico': topico,
            'status': 'sucesso',
            'score_consenso': consenso['score_medio'],
            'parametros': {
                'positivos': len(positivos),
                'negativos': len(negativos),
                'incertos': len(incertos)
            }
        }
    
    def _gerar_conteudo_base(self, topico: str) -> str:
        """Gera conteúdo base rico para análise"""
        return f"""
        Análise aprofundada sobre {topico.replace('_', ' ')}.
        
        Este tópico é estratégico e requer abordagem multidisciplinar com 12 especialistas.
        Objetivo: melhorar qualidade, eficiência e inovação dos processos relacionados.
        
        Aspectos técnicos:
        - Arquitetura modular com separação clara de responsabilidades e microserviços
        - Implementação com testes automatizados, CI/CD e validação contínua
        - Tratamento de erros e exceções em todas as camadas com logging estruturado
        - Documentação técnica para reutilização futura e onboarding
        - Otimização de performance com cache, processamento assíncrono e lazy loading
        
        Segurança:
        - Autenticação e autorização implementadas com MFA e RBAC
        - Criptografia de dados sensíveis em trânsito (TLS 1.3) e repouso (AES-256)
        - Validação e sanitização de entradas com WAF
        - Logs de auditoria para rastreabilidade e conformidade
        
        Viabilidade econômica:
        - ROI estimado positivo com payback em 12-18 meses
        - Custos mapeados e métricas de sucesso definidas (KPIs, OKRs)
        - Modelo de precificação flexível e escalável
        
        Experiência do usuário:
        - Interface simples, intuitiva e acessível reduz carga cognitiva
        - Feedback claro em cada etapa do processo
        - Design responsivo e inclusivo
        
        Ética e responsabilidade:
        - Transparência sobre uso de dados do usuário
        - Consentimento explícito para coleta de informações
        - Impacto social e ambiental avaliado
        
        Produto e mercado:
        - Problema claramente definido com solução validada (Jobs-to-be-Done)
        - Segmento de mercado identificado e mapeado
        - Roadmap com prioridades baseadas em impacto e esforço
        
        Machine Learning:
        - Dataset estruturado e limpo disponível para treinamento
        - Métricas de avaliação: accuracy, precision, recall, f1, AUC-ROC
        - Framework PyTorch/sklearn adequado para o caso de uso
        - Pipeline de dados com validação, teste e monitoramento
        
        DevOps:
        - CI/CD com GitHub Actions/GitLab CI
        - Infraestrutura como código com Terraform
        - Monitoramento com Prometheus e Grafana
        - Deploy automatizado com rollback
        
        Blockchain (se aplicável):
        - Smart contracts auditados
        - Consenso e governança definidos
        - Integração com oráculos
        
        Cloud:
        - Arquitetura multi-cloud híbrida
        - Auto-scaling e load balancing
        - Disaster recovery e backup
        
        Data Engineering:
        - Pipelines ETL/ELT robustos
        - Data warehouse e data lake
        - Streaming e processamento em batch
        - Governança e qualidade de dados
        
        Portanto, a abordagem proposta é tecnicamente sólida, economicamente
        viável, eticamente responsável e pronta para implementação em produção.
        """
    
    def _salvar_tokens_treinamento(self, resultados: List[Dict]):
        """Salva tokens de treinamento no banco de dados"""
        for resultado in resultados:
            topico = resultado['topico']
            score = resultado['score_consenso']
            
            # Token de consenso
            db.salvar_token_treinamento(
                'consenso',
                {'topico': topico, 'score': score, 'parametros': resultado['parametros']},
                topico=topico,
                score=score
            )
            
            # Tokens por tipo de parâmetro
            for tipo, count in resultado['parametros'].items():
                if count > 0:
                    db.salvar_token_treinamento(
                        f'parametro_{tipo}',
                        {'topico': topico, 'tipo': tipo, 'quantidade': count},
                        topico=topico,
                        score=score
                    )
        
        logger.info(f"Tokens de treinamento salvos: {len(resultados)} tópicos")
    
    def _mostrar_banner(self):
        banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  {CONFIG.NAME:<76}║
║  Versão {CONFIG.VERSION:<70}║
║                                                                              ║
║  12 Mentes: Engenheiro | CientistaDados | CISO | Economista | Psicólogo     ║
║             Filósofo | CPO | PesquisadorML | DevOps | Blockchain            ║
║             CloudArchitect | DataEngineer                                    ║
║                                                                              ║
║  [v7.0] SQLite WAL | 12 Agentes | DDG Multi-camada | Tokens Persistentes   ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        logger.info(f"Base: {CONFIG.BASE_DIR}")
        logger.info(f"Banco (WAL): {CONFIG.DB_PATH}")
        logger.info(f"Web Search: {'Ativo' if self.usar_web_search else 'Desativado'}")

# ====================================================================================
# FUNÇÃO PRINCIPAL
# ====================================================================================

def main(topicos: List[str] = None, num_rodadas: int = 20, usar_web_search: bool = True) -> List[Dict]:
    """
    Executa o sistema BRX-Agent v7.0
    
    Args:
        topicos: Lista de tópicos (None = usar 15 padrões)
        num_rodadas: Rodadas de debate por tópico (padrão: 20)
        usar_web_search: Busca DuckDuckGo (padrão: True)
    
    Returns:
        Lista de resultados por tópico
    """
    try:
        orquestrador = OrquestradorBRX(usar_web_search=usar_web_search)
        return orquestrador.executar(topicos, num_rodadas)
    except KeyboardInterrupt:
        logger.warning("\nInterrompido pelo usuário")
        return []
    except Exception as e:
        logger.error(f"\nErro crítico: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    resultados = main()
    
    print("\n" + "="*70)
    print("RESUMO DOS RESULTADOS:")
    print("="*70)
    for r in resultados:
        p = r['parametros']
        print(f"   {r['topico']:<30} {r['score_consenso']:.2%}  +{p['positivos']} -{p['negativos']} ?{p['incertos']}")
