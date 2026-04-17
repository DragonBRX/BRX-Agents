# BRX-AGENT v7.0 - Gerador de Parâmetros Aprimorado
# Sistema de geração automática com persistência robusta e validação

import os
import sys
import json
import time
import random
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# Setup logging
logger = logging.getLogger("BRXv7.parameters")

# ====================================================================================
# CONFIGURAÇÃO
# ====================================================================================

@dataclass
class ParameterConfig:
    """Configuração para geração de parâmetros"""
    VERSION: str = "7.0.0"
    BASE_DIR: Path = field(default_factory=lambda: Path.home() / "BRX-Agent")
    PARAMS_DIR: Path = None
    TEMPLATES_FILE: Path = None
    
    def __post_init__(self):
        self.PARAMS_DIR = self.BASE_DIR / "parameters"
        self.TEMPLATES_FILE = self.PARAMS_DIR / "templates.json"
        self.PARAMS_DIR.mkdir(parents=True, exist_ok=True)

PARAM_CONFIG = ParameterConfig()

# ====================================================================================
# BANCO DE DADOS DE PARÂMETROS
# ====================================================================================

class ParameterDatabase:
    """Banco de dados JSON para parâmetros com persistência garantida"""
    
    def __init__(self):
        self.db_file = PARAM_CONFIG.PARAMS_DIR / "parameters_db.json"
        self._data = self._load()
    
    def _load(self) -> Dict:
        """Carrega banco de dados ou cria novo"""
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erro ao carregar DB: {e}")
        
        return {
            "metadata": {
                "version": "7.0.0",
                "created": time.time(),
                "last_updated": time.time(),
                "total_parameters": 0
            },
            "parameters": {},
            "templates": {},
            "categories": {
                "technical": [],
                "security": [],
                "business": [],
                "ux": [],
                "ethics": [],
                "ml": [],
                "devops": [],
                "data": []
            }
        }
    
    def _save(self):
        """Salva banco de dados com atomicidade"""
        try:
            self._data["metadata"]["last_updated"] = time.time()
            self._data["metadata"]["total_parameters"] = len(self._data["parameters"])
            
            # Escreve em arquivo temporário primeiro
            temp_file = self.db_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False, default=str)
            
            # Substitui atomicamente
            temp_file.replace(self.db_file)
            logger.debug(f"DB salvo: {len(self._data['parameters'])} parâmetros")
        except Exception as e:
            logger.error(f"Erro ao salvar DB: {e}")
    
    def add_parameter(self, param_id: str, data: Dict) -> bool:
        """Adiciona parâmetro ao banco"""
        try:
            self._data["parameters"][param_id] = {
                **data,
                "created": time.time(),
                "updated": time.time(),
                "access_count": 0
            }
            
            # Adiciona à categoria
            category = data.get("category", "technical")
            if category in self._data["categories"]:
                if param_id not in self._data["categories"][category]:
                    self._data["categories"][category].append(param_id)
            
            self._save()
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar parâmetro: {e}")
            return False
    
    def get_parameter(self, param_id: str) -> Optional[Dict]:
        """Recupera parâmetro por ID"""
        param = self._data["parameters"].get(param_id)
        if param:
            param["access_count"] = param.get("access_count", 0) + 1
            self._save()
        return param
    
    def get_by_category(self, category: str) -> List[Dict]:
        """Recupera parâmetros por categoria"""
        param_ids = self._data["categories"].get(category, [])
        return [self._data["parameters"][pid] for pid in param_ids if pid in self._data["parameters"]]
    
    def get_all(self) -> Dict[str, Dict]:
        """Recupera todos os parâmetros"""
        return self._data["parameters"].copy()
    
    def search(self, query: str) -> List[Dict]:
        """Busca parâmetros por texto"""
        results = []
        query_lower = query.lower()
        
        for param_id, param in self._data["parameters"].items():
            param_str = json.dumps(param, default=str).lower()
            if query_lower in param_str:
                results.append(param)
        
        return results
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do banco"""
        return {
            "total_parameters": len(self._data["parameters"]),
            "categories": {k: len(v) for k, v in self._data["categories"].items()},
            "last_updated": self._data["metadata"]["last_updated"]
        }

# Instância global
param_db = ParameterDatabase()

# ====================================================================================
# GERADOR DE PARÂMETROS
# ====================================================================================

class ParameterGenerator:
    """Gerador de parâmetros com templates e validação"""
    
    # Templates de parâmetros por categoria
    TEMPLATES = {
        "technical": {
            "aspects": [
                "arquitetura_limpa", "codigo_limpo", "testes_automatizados",
                "documentacao", "performance", "escalabilidade", "manutenibilidade"
            ],
            "metrics": ["cobertura_testes", "complexidade_ciclomatica", "debito_tecnico"],
            "patterns": ["mvc", "microservices", "serverless", "event_driven", "cqrs"]
        },
        "security": {
            "aspects": [
                "autenticacao", "autorizacao", "criptografia", "audit_logging",
                "input_validation", "rate_limiting", "vulnerability_management"
            ],
            "standards": ["owasp_top10", "iso27001", "gdpr", "lgpd", "nist_csf"],
            "tools": ["waf", "siem", "dap", "penetration_testing"]
        },
        "business": {
            "aspects": [
                "roi", "payback", "custo_beneficio", "modelo_receita",
                "market_share", "competitive_advantage", "customer_acquisition"
            ],
            "metrics": ["ltv", "cac", "churn_rate", "nps", "mrr"],
            "frameworks": ["bmc", "swot", "pestel", "porter_five_forces"]
        },
        "ux": {
            "aspects": [
                "usabilidade", "acessibilidade", "performance_percebida",
                "satisfacao_usuario", "engajamento", "retencao"
            ],
            "methods": ["user_research", "usability_testing", "a_b_testing", "journey_mapping"],
            "metrics": ["csat", "ces", "task_success_rate", "time_on_task"]
        },
        "ethics": {
            "aspects": [
                "privacidade", "transparencia", "justica", "responsabilidade",
                "consentimento", "inclusao", "sustentabilidade"
            ],
            "frameworks": ["utilitarismo", "deontologia", "virtude_ethics", "care_ethics"],
            "guidelines": ["ai_ethics_guidelines", "data_ethics_framework", "ethical_design"]
        },
        "ml": {
            "aspects": [
                "model_selection", "feature_engineering", "hyperparameter_tuning",
                "model_validation", "deployment", "monitoring", "retraining"
            ],
            "algorithms": ["random_forest", "gradient_boosting", "neural_networks", "transformers"],
            "metrics": ["accuracy", "precision", "recall", "f1", "auc_roc", "mae", "rmse"]
        },
        "devops": {
            "aspects": [
                "ci_cd", "iac", "monitoring", "logging", "containerization",
                "orchestration", "gitops", "chaos_engineering"
            ],
            "tools": ["jenkins", "gitlab_ci", "github_actions", "terraform", "ansible"],
            "platforms": ["kubernetes", "docker", "helm", "argo_cd"]
        },
        "data": {
            "aspects": [
                "data_quality", "data_governance", "data_lineage",
                "etl_pipeline", "data_warehouse", "data_lake", "streaming"
            ],
            "tools": ["airflow", "dbt", "spark", "kafka", "snowflake", "bigquery"],
            "formats": ["parquet", "avro", "json", "csv", "orc"]
        }
    }
    
    def __init__(self):
        self.db = param_db
        self._load_templates()
    
    def _load_templates(self):
        """Carrega ou cria templates"""
        templates_file = PARAM_CONFIG.TEMPLATES_FILE
        
        if templates_file.exists():
            try:
                with open(templates_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.TEMPLATES.update(loaded)
            except Exception as e:
                logger.warning(f"Erro ao carregar templates: {e}")
        else:
            # Salva templates padrão
            try:
                with open(templates_file, 'w', encoding='utf-8') as f:
                    json.dump(self.TEMPLATES, f, indent=2, ensure_ascii=False)
            except Exception as e:
                logger.error(f"Erro ao salvar templates: {e}")
    
    def generate_parameter(self, category: str, topic: str, agent_name: str, 
                          score: float = 0.5) -> Optional[Dict]:
        """Gera um novo parâmetro baseado em template"""
        if category not in self.TEMPLATES:
            logger.warning(f"Categoria desconhecida: {category}")
            return None
        
        template = self.TEMPLATES[category]
        
        # Gera ID único
        param_id = hashlib.sha256(
            f"{category}_{topic}_{agent_name}_{time.time()}".encode()
        ).hexdigest()[:16]
        
        # Cria parâmetro
        parameter = {
            "id": param_id,
            "category": category,
            "topic": topic,
            "agent": agent_name,
            "score": score,
            "aspects": self._select_aspects(template.get("aspects", [])),
            "metrics": self._select_metrics(template.get("metrics", [])),
            "recommendations": self._generate_recommendations(category, topic),
            "confidence": self._calculate_confidence(score),
            "tags": [category, topic, agent_name],
            "version": "7.0.0"
        }
        
        # Adiciona campos específicos por categoria
        if "patterns" in template:
            parameter["patterns"] = random.sample(template["patterns"], 
                                                   min(2, len(template["patterns"])))
        if "standards" in template:
            parameter["standards"] = random.sample(template["standards"], 
                                                    min(2, len(template["standards"])))
        if "frameworks" in template:
            parameter["frameworks"] = random.sample(template["frameworks"], 
                                                     min(2, len(template["frameworks"])))
        if "tools" in template:
            parameter["tools"] = random.sample(template["tools"], 
                                                min(3, len(template["tools"])))
        
        # Salva no banco
        if self.db.add_parameter(param_id, parameter):
            logger.info(f"Parâmetro gerado: {param_id} ({category}/{topic})")
            return parameter
        
        return None
    
    def generate_batch(self, category: str, topic: str, count: int = 5) -> List[Dict]:
        """Gera múltiplos parâmetros"""
        parameters = []
        
        for i in range(count):
            score = random.uniform(0.3, 0.95)
            param = self.generate_parameter(category, topic, "system", score)
            if param:
                parameters.append(param)
        
        return parameters
    
    def _select_aspects(self, aspects: List[str]) -> List[str]:
        """Seleciona aspectos relevantes"""
        if not aspects:
            return []
        count = random.randint(2, min(4, len(aspects)))
        return random.sample(aspects, count)
    
    def _select_metrics(self, metrics: List[str]) -> List[str]:
        """Seleciona métricas relevantes"""
        if not metrics:
            return []
        count = random.randint(1, min(3, len(metrics)))
        return random.sample(metrics, count)
    
    def _generate_recommendations(self, category: str, topic: str) -> List[str]:
        """Gera recomendações baseadas na categoria"""
        recommendations = {
            "technical": [
                f"Implementar arquitetura limpa para {topic}",
                f"Adicionar testes automatizados com cobertura > 80%",
                f"Documentar APIs e componentes principais"
            ],
            "security": [
                f"Realizar auditoria de segurança em {topic}",
                f"Implementar autenticação multi-fator",
                f"Criptografar dados sensíveis em trânsito e repouso"
            ],
            "business": [
                f"Definir KPIs e métricas de sucesso para {topic}",
                f"Realizar análise de custo-benefício detalhada",
                f"Mapear concorrência e diferenciais"
            ],
            "ux": [
                f"Realizar pesquisa com usuários sobre {topic}",
                f"Simplificar fluxos e reduzir carga cognitiva",
                f"Garantir acessibilidade WCAG 2.1 AA"
            ],
            "ethics": [
                f"Avaliar impacto ético de {topic}",
                f"Garantir transparência e consentimento",
                f"Considerar inclusão e diversidade"
            ],
            "ml": [
                f"Definir baseline e métricas de avaliação",
                f"Implementar pipeline de MLOps",
                f"Monitorar drift e performance em produção"
            ],
            "devops": [
                f"Automatizar pipeline CI/CD",
                f"Implementar infraestrutura como código",
                f"Configurar monitoramento e alertas"
            ],
            "data": [
                f"Implementar governança de dados",
                f"Criar pipeline ETL/ELT robusto",
                f"Garantir qualidade e linhagem de dados"
            ]
        }
        
        return recommendations.get(category, ["Avaliar e melhorar continuamente"])
    
    def _calculate_confidence(self, score: float) -> float:
        """Calcula nível de confiança baseado no score"""
        base_confidence = min(1.0, max(0.1, score))
        noise = random.uniform(-0.1, 0.1)
        return round(min(1.0, max(0.1, base_confidence + noise)), 2)
    
    def get_parameter_stats(self) -> Dict:
        """Retorna estatísticas de parâmetros"""
        return self.db.get_stats()

# Instância global
generator = ParameterGenerator()

# ====================================================================================
# FUNÇÕES DE INTERFACE
# ====================================================================================

def generate_parameter(category: str, topic: str, agent_name: str = "system", 
                      score: float = 0.5) -> Optional[Dict]:
    """Gera um parâmetro"""
    return generator.generate_parameter(category, topic, agent_name, score)

def generate_batch(category: str, topic: str, count: int = 5) -> List[Dict]:
    """Gera múltiplos parâmetros"""
    return generator.generate_batch(category, topic, count)

def get_parameter(param_id: str) -> Optional[Dict]:
    """Recupera parâmetro por ID"""
    return param_db.get_parameter(param_id)

def search_parameters(query: str) -> List[Dict]:
    """Busca parâmetros"""
    return param_db.search(query)

def get_stats() -> Dict:
    """Retorna estatísticas"""
    return generator.get_parameter_stats()

# ====================================================================================
# TESTE
# ====================================================================================

if __name__ == "__main__":
    print("BRX-Agent v7.0 - Gerador de Parâmetros")
    print("=" * 50)
    
    # Gera parâmetros de exemplo
    categories = ["technical", "security", "business", "ux", "ml"]
    
    for cat in categories:
        print(f"\nGerando parâmetros para categoria: {cat}")
        params = generate_batch(cat, "exemplo_topico", 3)
        for p in params:
            print(f"  - {p['id']}: score={p['score']:.2f}, aspects={len(p['aspects'])}")
    
    # Estatísticas
    stats = get_stats()
    print(f"\nEstatísticas:")
    print(f"  Total de parâmetros: {stats['total_parameters']}")
    print(f"  Por categoria: {stats['categories']}")
