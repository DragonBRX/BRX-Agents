# BRX-AGENT v3.0 - Analisador de Tarefas
# Analisa a solicitacao do usuario e determina quais agentes devem ser ativados

import re
from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass, field

from core.types import (
    TaskAnalysis, AgentCategory, AgentRegistry,
    SpecializedAgent
)
from agents.agent_catalog import get_agent_registry


class TaskAnalyzer:
    """
    Analisador inteligente de tarefas
    Determina quais categorias e agentes sao necessarios para uma solicitacao
    """
    
    # Mapeamento de palavras-chave para categorias
    CATEGORY_KEYWORDS = {
        AgentCategory.DEVELOPMENT: [
            "codigo", "programar", "desenvolver", "sistema", "app", "aplicacao",
            "software", "backend", "frontend", "fullstack", "api", "banco de dados",
            "website", "site", "web", "mobile", "flutter", "react", "vue", "angular",
            "python", "javascript", "java", "c#", "php", "ruby", "go", "rust",
            "automation", "script", "bot", "crawler", "scraper", "integracao",
            "deploy", "ci/cd", "docker", "kubernetes", "microservico",
            "jogo", "game", "blockchain", "smart contract", "web3", "nft",
            "embedded", "arduino", "raspberry", "iot", "sensor",
            "compilador", "linguagem", "interpreter", "runtime",
            "ecommerce", "loja virtual", "shopify", "vtex", "woocommerce",
            "saas", "multi-tenant", "white-label",
            "robotica", "ros", "drone", "autonomo",
            "ar", "vr", "realidade aumentada", "realidade virtual",
            "chatbot", "conversacional", "nlu", "dialogo",
            "machine learning", "ml", "ia", "inteligencia artificial", "llm",
            "crm", "salesforce", "hubspot",
            "quant", "quantitativo", "trading", "financeiro",
            "crm", "erp", "sistema legado"
        ],
        
        AgentCategory.DESIGN: [
            "design", "interface", "ui", "ux", "user experience", "user interface",
            "layout", "figma", "sketch", "adobe", "photoshop", "illustrator",
            "prototipo", "wireframe", "mockup", "design system", "componente",
            "logo", "identidade visual", "branding", "marca",
            "ilustracao", "ilustracao", "vetor", "icone", "mascote",
            "animacao", "motion", "after effects", "lottie", "microinteracao",
            "3d", "modelagem", "blender", "three.js", "webgl",
            "apresentacao", "slide", "pitch deck", "powerpoint",
            "tipografia", "fonte", "lettering",
            "game ui", "hud", "interface de jogo",
            "acessibilidade", "wcag", "a11y", "acessivel",
            "vui", "voice ui", "alexa", "google assistant",
            "data visualization", "visualizacao de dados", "dashboard design"
        ],
        
        AgentCategory.CONTENT: [
            "conteudo", "texto", "artigo", "blog", "post", "redacao",
            "copywriting", "copy", "marketing", "seo", "email marketing",
            "documentacao", "documentar", "readme", "wiki", "manual",
            "tutorial", "guia", "how-to", "passo a passo",
            "podcast", "audio", "roteiro", "script",
            "whitepaper", "paper", "artigo cientifico",
            "newsletter", "email", "campanha",
            "localizacao", "traducao", "i18n", "l10n", "multilingue",
            "curso", "educacional", "elearning", "treinamento",
            "social media", "redes sociais", "instagram", "tiktok", "youtube",
            "review", "analise critica", "opiniao"
        ],
        
        AgentCategory.DATA: [
            "dados", "data", "analytics", "analise de dados", "dashboard",
            "etl", "pipeline", "data warehouse", "data lake", "lakehouse",
            "sql", "query", "banco de dados", "database", "schema",
            "machine learning", "modelo", "predicao", "classificacao",
            "visualizacao", "grafico", "chart", "power bi", "tableau",
            "big data", "spark", "hadoop", "kafka",
            "governanca", "data quality", "data catalog", "lineage",
            "mlops", "feature store", "model serving",
            "estatistica", "estatistico", "hipotese", "teste a/b",
            "bi", "business intelligence", "kpi", "metrica",
            "elasticsearch", "solr", "busca"
        ],
        
        AgentCategory.SECURITY: [
            "seguranca", "security", "proteger", "vulnerabilidade", "brecha",
            "penetration test", "pentest", "ethical hacking", "hacker",
            "owasp", "injection", "xss", "csrf", "autenticacao", "auth",
            "criptografia", "encryption", "ssl", "tls", "certificado",
            "compliance", "lgpd", "gdpr", "iso 27001", "soc2", "auditoria",
            "firewall", "waf", "ddos", "intrusion detection",
            "forense", "investigacao", "incidente",
            "iam", "acesso", "permissao", "role",
            "blockchain", "smart contract audit",
            "cloud security", "container security",
            "threat intelligence", "soc", "siem"
        ],
        
        AgentCategory.INFRASTRUCTURE: [
            "infraestrutura", "infra", "devops", "sre", "cloud",
            "servidor", "server", "hosting", "hospedagem",
            "docker", "container", "kubernetes", "k8s", "helm",
            "ci/cd", "pipeline", "jenkins", "github actions", "gitlab ci",
            "terraform", "iac", "cloudformation", "pulumi",
            "aws", "azure", "gcp", "google cloud", "amazon",
            "monitoramento", "monitoring", "observability", "logs", "tracing",
            "backup", "disaster recovery", "dr",
            "rede", "network", "cdn", "dns", "load balancer",
            "custo", "cost optimization", "finops",
            "plataforma", "idp", "developer platform", "backstage",
            "gitops", "argocd", "flux",
            "database", "dba", "postgres", "mysql", "mongodb",
            "edge", "cdn", "cloudflare", "vercel"
        ],
        
        AgentCategory.BUSINESS: [
            "negocio", "business", "produto", "product", "estrategia",
            "startup", "empreendedorismo", "mvp", "pitch", "investimento",
            "agil", "scrum", "kanban", "sprint", "cerimonia",
            "roadmap", "priorizacao", "backlog", "user story",
            "metrica", "kpi", "okrs", "indicador",
            "crescimento", "growth", "aquisicao", "retencao",
            "vendas", "sales", "proposta", "rfp", "licitacao",
            "financeiro", "orcamento", "custo", "receita", "unit economics",
            "processo", "bpm", "workflow", "automatizacao de processos",
            "analise de negocio", "requisitos", "brd", "frd",
            "recursos humanos", "rh", "contratacao", "recrutamento",
            "legal", "contrato", "propriedade intelectual", "ip"
        ],
        
        AgentCategory.RESEARCH: [
            "pesquisa", "research", "estudo", "analise", "survey",
            "inovacao", "innovation", "tendencia", "trend",
            "inteligencia artificial", "ia", "ai", "llm", "transformer",
            "academico", "cientifico", "paper", "publicacao", "journal",
            "usuario", "user research", "entrevista", "focus group",
            "mercado", "market research", "concorrencia", "competitivo",
            "tecnologia", "tech radar", "proof of concept", "poc",
            "bioinformatica", "genomica", "proteomica",
            "cybersecurity research", "vulnerability research",
            "policy", "politica publica", "regulacao",
            "metodologia", "systematic review", "meta-analysis"
        ],
        
        AgentCategory.CREATIVE: [
            "arte", "artistico", "criativo", "creative", "ilustracao",
            "musica", "music", "producao musical", "composicao", "audio",
            "video", "filme", "cinema", "edicao", "color grading",
            "fotografia", "photo", "edicao de foto", "retouching",
            "design grafico", "graphic design", "poster", "flyer",
            "caligrafia", "lettering", "tipografia art",
            "tattoo", "tatuagem", "design de tattoo",
            "moda", "fashion", "styling", "consultoria de estilo",
            "maquiagem", "makeup", "beauty",
            "ceramica", "artesanato", "handmade",
            "evento", "decoracao", "cenografia",
            "paisagismo", "jardinagem", "floral",
            "joias", "jewelry", "design de joias",
            "mural", "street art", "graffiti",
            "animacao", "animation", "2d", "3d",
            "storyboard", "concept art", "arte conceitual",
            "direcao", "direction", "film direction",
            "sound design", "design sonoro", "foley",
            "roteiro", "screenplay", "narrativa", "narrative"
        ],
        
        AgentCategory.COMMUNICATION: [
            "suporte", "support", "atendimento", "customer service",
            "comunidade", "community", "forum", "discord",
            "redes sociais", "social media", "engajamento",
            "comunicacao", "comunicar", "divulgacao", "marketing",
            "relacoes publicas", "pr", "imprensa",
            "recrutamento", "recruiting", "talent acquisition",
            "onboarding", "integracao", "treinamento"
        ],
        
        AgentCategory.QUALITY: [
            "qualidade", "quality", "teste", "testing", "qa",
            "bug", "defeito", "issue", "problema",
            "automation", "automacao", "selenium", "cypress", "playwright",
            "performance", "carga", "load testing", "stress test",
            "seguranca", "security testing", "pentest",
            "acessibilidade", "a11y testing", "wcag test",
            "regressao", "regression", "smoke test",
            "usuario", "user acceptance", "uat",
            "junit", "pytest", "unit test", "integracao", "integration test"
        ],
        
        AgentCategory.PROJECT: [
            "projeto", "project", "gestao", "management",
            "cronograma", "schedule", "timeline", "prazo", "deadline",
            "risco", "risk", "mitigacao", "plano",
            "escopo", "scope", "change request", "mudanca",
            "stakeholder", "parte interessada",
            "scrum master", "product owner", "agile coach",
            "pmo", "portfolio", "programa",
            "orcamento", "budget", "custo", "baseline",
            "recurso", "resource", "alocacao", "capacidade"
        ]
    }
    
    # Mapeamento de tarefas especificas para agentes diretos
    TASK_AGENT_MAPPING = {
        # Desenvolvimento
        "api": ["dev_api", "dev_backend"],
        "backend": ["dev_backend"],
        "frontend": ["dev_frontend"],
        "website": ["dev_frontend", "dev_backend", "design_ui", "design_ux"],
        "site": ["dev_frontend", "dev_backend", "design_ui"],
        "mobile": ["dev_mobile"],
        "app": ["dev_mobile", "dev_fullstack"],
        "jogo": ["dev_game", "creative_concept", "design_games"],
        "game": ["dev_game", "creative_concept", "design_games"],
        "blockchain": ["dev_blockchain", "sec_appsec"],
        "smart contract": ["dev_blockchain", "sec_appsec"],
        "ecommerce": ["dev_ecommerce", "design_ui"],
        "loja virtual": ["dev_ecommerce", "design_ui"],
        "saas": ["dev_saas", "dev_backend"],
        "ia": ["dev_ai_ml", "dev_nlp", "research_ai"],
        "machine learning": ["dev_ai_ml", "data_scientist"],
        "chatbot": ["dev_chatbot", "dev_nlp"],
        "crm": ["dev_crm", "biz_product"],
        "robotica": ["dev_robotics"],
        "ar": ["dev_arvr", "design_3d"],
        "vr": ["dev_arvr", "design_3d"],
        "database": ["dev_database", "data_engineer"],
        "teste": ["qa_manual", "qa_auto"],
        "testes": ["qa_manual", "qa_auto"],
        
        # Design
        "design system": ["design_ui", "design_ux"],
        "logo": ["design_graphic"],
        "identidade visual": ["design_graphic", "design_ui"],
        "branding": ["design_graphic", "content_copy"],
        "ui": ["design_ui"],
        "ux": ["design_ux", "research_user"],
        "ilustracao": ["design_illustration"],
        "animacao": ["design_motion"],
        "3d": ["design_3d", "dev_arvr"],
        "motion": ["design_motion"],
        "apresentacao": ["design_presentation"],
        
        # Infra
        "devops": ["infra_devops", "infra_sre"],
        "cloud": ["infra_cloud"],
        "kubernetes": ["infra_k8s", "infra_devops"],
        "docker": ["infra_devops"],
        "ci/cd": ["infra_devops"],
        "monitoramento": ["infra_sre"],
        "seguranca cloud": ["sec_cloud", "infra_cloud"],
        
        # Dados
        "dados": ["data_analyst", "data_engineer"],
        "analytics": ["data_analyst", "data_scientist"],
        "etl": ["data_engineer"],
        "pipeline": ["data_engineer"],
        "dashboard": ["data_analyst", "data_visualization"],
        "visualizacao": ["data_visualization"],
        
        # Seguranca
        "seguranca": ["sec_appsec", "sec_pentest"],
        "pentest": ["sec_pentest"],
        "compliance": ["sec_compliance"],
        "lgpd": ["sec_compliance"],
        "gdpr": ["sec_compliance"],
        "forense": ["sec_forensic"],
        
        # Negocios
        "produto": ["biz_product", "design_product"],
        "agil": ["biz_agile", "pm_scrum"],
        "scrum": ["pm_scrum"],
        "startup": ["biz_startup", "biz_growth"],
        
        # Qualidade
        "qa": ["qa_manual", "qa_auto"],
        "performance": ["qa_perf", "infra_sre"],
        "automation": ["qa_auto"],
    }
    
    def __init__(self, max_agents: int = 8):
        self.max_agents = max_agents
        self.registry = get_agent_registry()
    
    def analyze(self, task_description: str) -> TaskAnalysis:
        """
        Analisa uma tarefa e retorna quais agentes devem ser ativados
        """
        task_lower = task_description.lower()
        
        # 1. Detecta categorias relevantes
        detected_categories = self._detect_categories(task_lower)
        
        # 2. Detecta skills necessarias
        required_skills = self._detect_skills(task_lower)
        
        # 3. Encontra agentes especificos pela tarefa
        specific_agents = self._detect_specific_agents(task_lower)
        
        # 4. Se nao encontrou agentes especificos, busca por categorias
        if not specific_agents:
            specific_agents = self._get_agents_by_categories(detected_categories)
        
        # 5. Calcula complexidade
        complexity = self._calculate_complexity(task_lower, len(specific_agents))
        
        # 6. Estima rodadas de debate
        estimated_rounds = self._estimate_rounds(complexity, len(specific_agents))
        
        # 7. Limita ao maximo de agentes permitido
        final_agents = specific_agents[:self.max_agents]
        
        # 8. Detecta requisitos especiais
        special_requirements = self._detect_special_requirements(task_lower)
        
        # 9. Gera dicas de contexto
        context_hints = self._generate_context_hints(task_lower, detected_categories)
        
        return TaskAnalysis(
            task_description=task_description,
            detected_categories=detected_categories,
            required_skills=required_skills,
            recommended_agents=final_agents,
            agent_count=len(final_agents),
            complexity=complexity,
            estimated_rounds=estimated_rounds,
            special_requirements=special_requirements,
            context_hints=context_hints
        )
    
    def _detect_categories(self, task_lower: str) -> List[AgentCategory]:
        """Detecta categorias relevantes baseado em palavras-chave"""
        detected = []
        category_scores = {}
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in task_lower:
                    score += 1
            if score > 0:
                category_scores[category] = score
        
        # Ordena por relevancia e pega as top categorias
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Pega categorias com score significativo
        for cat, score in sorted_categories:
            if score >= 1:
                detected.append(cat)
        
        # Se nao detectou nada, usa categorias genericas
        if not detected:
            detected = [AgentCategory.DEVELOPMENT, AgentCategory.RESEARCH]
        
        return detected[:5]  # Max 5 categorias
    
    def _detect_skills(self, task_lower: str) -> List[str]:
        """Detecta skills especificas mencionadas na tarefa"""
        skill_keywords = [
            "python", "javascript", "typescript", "react", "vue", "angular",
            "node.js", "docker", "kubernetes", "aws", "azure", "gcp",
            "sql", "nosql", "mongodb", "postgres", "mysql",
            "machine learning", "deep learning", "nlp", "computer vision",
            "blockchain", "solidity", "smart contract",
            "ci/cd", "devops", "terraform", "ansible",
            "figma", "sketch", "adobe", "ui/ux",
            "seo", "marketing", "copywriting",
            "agile", "scrum", "kanban",
            "teste", "qa", "automation",
            "api", "rest", "graphql", "grpc",
            "mobile", "flutter", "react native", "ios", "android"
        ]
        
        detected_skills = []
        for skill in skill_keywords:
            if skill in task_lower:
                detected_skills.append(skill)
        
        return detected_skills
    
    def _detect_specific_agents(self, task_lower: str) -> List[str]:
        """Detecta agentes especificos pelo mapeamento de tarefas"""
        detected = set()
        
        for keyword, agents in self.TASK_AGENT_MAPPING.items():
            if keyword in task_lower:
                for agent_id in agents:
                    detected.add(agent_id)
        
        return list(detected)
    
    def _get_agents_by_categories(self, categories: List[AgentCategory]) -> List[str]:
        """Retorna agentes baseado nas categorias detectadas"""
        agents = []
        for category in categories:
            category_agents = self.registry.get_by_category(category)
            for agent in category_agents:
                if agent.id not in agents:
                    agents.append(agent.id)
        return agents
    
    def _calculate_complexity(self, task_lower: str, num_agents: int) -> str:
        """Calcula a complexidade da tarefa"""
        # Palavras indicadoras de complexidade
        high_complexity = ["arquitetura", "plataforma", "sistema completo", "enterprise",
                          "microservico", "escalavel", "distribuido", "real-time"]
        medium_complexity = ["aplicacao", "website", "api", "dashboard", "integracao"]
        
        complexity_score = 0
        for word in high_complexity:
            if word in task_lower:
                complexity_score += 2
        for word in medium_complexity:
            if word in task_lower:
                complexity_score += 1
        
        # Ajusta pelo numero de agentes necessarios
        if num_agents >= 6:
            complexity_score += 2
        elif num_agents >= 4:
            complexity_score += 1
        
        if complexity_score >= 4:
            return "expert"
        elif complexity_score >= 2:
            return "high"
        elif complexity_score >= 1:
            return "medium"
        else:
            return "low"
    
    def _estimate_rounds(self, complexity: str, num_agents: int) -> int:
        """Estima numero de rodadas de debate necessarias"""
        base_rounds = {
            "low": 2,
            "medium": 3,
            "high": 4,
            "expert": 5
        }
        
        rounds = base_rounds.get(complexity, 3)
        
        # Ajusta pelo numero de agentes
        if num_agents > 6:
            rounds += 1
        
        return min(rounds, 8)  # Max 8 rodadas
    
    def _detect_special_requirements(self, task_lower: str) -> List[str]:
        """Detecta requisitos especiais da tarefa"""
        requirements = []
        
        if any(word in task_lower for word in ["rapido", "urgente", "asap"]):
            requirements.append("entrega_rapida")
        if any(word in task_lower for word in ["escalavel", "escala", "milhoes"]):
            requirements.append("escalabilidade")
        if any(word in task_lower for word in ["seguro", "seguranca", "protegido"]):
            requirements.append("seguranca_reforcada")
        if any(word in task_lower for word in ["acessivel", "a11y", "wcag"]):
            requirements.append("acessibilidade")
        if any(word in task_lower for word in ["multi-idioma", "internacional", "i18n"]):
            requirements.append("internacionalizacao")
        if any(word in task_lower for word in ["mobile first", "responsivo", "mobile"]):
            requirements.append("mobile_first")
        if any(word in task_lower for word in ["real-time", "tempo real", "websocket"]):
            requirements.append("tempo_real")
        if any(word in task_lower for word in ["lgpd", "gdpr", "compliance"]):
            requirements.append("conformidade_regulatoria")
        
        return requirements
    
    def _generate_context_hints(self, task_lower: str, categories: List[AgentCategory]) -> Dict[str, Any]:
        """Gera dicas de contexto para os agentes"""
        hints = {
            "categories": [c.value for c in categories],
            "language_preference": "portuguese",
            "estimated_scope": "medium"
        }
        
        # Detecta preferencia de linguagem
        if any(word in task_lower for word in ["ingles", "english"]):
            hints["language_preference"] = "english"
        
        # Detecta escopo
        if any(word in task_lower for word in ["completo", "full", "total", "end-to-end"]):
            hints["estimated_scope"] = "full_project"
        elif any(word in task_lower for word in ["prototipo", "prototype", "mvp", "basico"]):
            hints["estimated_scope"] = "prototype"
        elif any(word in task_lower for word in ["melhoria", "improvement", "refactor", "otimizacao"]):
            hints["estimated_scope"] = "improvement"
        
        # Detecta plataforma alvo
        if "web" in task_lower:
            hints["target_platform"] = "web"
        elif any(word in task_lower for word in ["mobile", "app", "ios", "android"]):
            hints["target_platform"] = "mobile"
        elif any(word in task_lower for word in ["desktop", "windows", "mac", "linux"]):
            hints["target_platform"] = "desktop"
        
        return hints
    
    def get_suggested_team_summary(self, analysis: TaskAnalysis) -> str:
        """Gera um resumo legivel da equipe sugerida"""
        lines = [
            f"\n{'='*60}",
            "EQUIPE DE AGENTES SELECIONADA",
            f"{'='*60}",
            f"\nTarefa: {analysis.task_description[:80]}...",
            f"Complexidade: {analysis.complexity.upper()}",
            f"Agentes: {analysis.agent_count}",
            f"Rodadas estimadas: {analysis.estimated_rounds}",
            "",
            "Categorias detectadas:"
        ]
        
        for cat in analysis.detected_categories:
            lines.append(f"  - {cat.value}")
        
        lines.extend(["", "Agentes selecionados:"])
        
        for agent_id in analysis.recommended_agents:
            agent = self.registry.agents.get(agent_id)
            if agent:
                traits = ", ".join([t.value for t in agent.personality_traits[:2]])
                lines.append(f"  [{agent_id}] {agent.name} - {agent.role}")
                lines.append(f"     Especialidade: {agent.specialty}")
                lines.append(f"     Personalidade: {traits}")
        
        if analysis.special_requirements:
            lines.extend(["", "Requisitos especiais:"])
            for req in analysis.special_requirements:
                lines.append(f"  - {req}")
        
        lines.append(f"\n{'='*60}")
        
        return "\n".join(lines)
