// BRX-ENGINE - Motor de Auto-Evolução
// Sistema que permite ao modelo evoluir seus próprios parâmetros

import type { 
  AgentParameter, 
  EvolutionCycle, 
  ParameterEvolution,
  PerformanceMetrics,
  SelfModification 
} from '../types';

export class EvolutionEngine {
  private parameters: Map<string, AgentParameter>;
  private evolutionHistory: EvolutionCycle[];
  private currentCycle: number;
  private autoEvolve: boolean;
  private readonly MAX_PARAMETERS = 10000;

  constructor(autoEvolve: boolean = true) {
    this.parameters = new Map();
    this.evolutionHistory = [];
    this.currentCycle = 0;
    this.autoEvolve = autoEvolve;
  }

  // Inicializa parâmetros padrão do sistema
  initializeDefaultParameters(): void {
    const defaults: AgentParameter[] = [
      {
        id: 'param_learning_rate',
        name: 'learning_rate',
        value: 0.001,
        type: 'positive',
        confidence: 0.9,
        source: 'System',
        timestamp: Date.now(),
        context: 'Taxa de aprendizado do modelo',
        evolutionHistory: []
      },
      {
        id: 'param_confidence_threshold',
        name: 'confidence_threshold',
        value: 0.75,
        type: 'positive',
        confidence: 0.95,
        source: 'System',
        timestamp: Date.now(),
        context: 'Limiar minimo de confianca para aceitar parametros',
        evolutionHistory: []
      },
      {
        id: 'param_debate_rounds',
        name: 'debate_rounds',
        value: 3,
        type: 'positive',
        confidence: 0.85,
        source: 'System',
        timestamp: Date.now(),
        context: 'Numero de rodadas de debate circular',
        evolutionHistory: []
      },
      {
        id: 'param_memory_retention',
        name: 'memory_retention',
        value: 0.9,
        type: 'positive',
        confidence: 0.8,
        source: 'System',
        timestamp: Date.now(),
        context: 'Taxa de retencao de memoria de curto prazo',
        evolutionHistory: []
      },
      {
        id: 'param_evolution_aggressiveness',
        name: 'evolution_aggressiveness',
        value: 0.5,
        type: 'neutral',
        confidence: 0.7,
        source: 'System',
        timestamp: Date.now(),
        context: 'Quao agressivamente o modelo evolui (0-1)',
        evolutionHistory: []
      },
      {
        id: 'param_error_tolerance',
        name: 'error_tolerance',
        value: 0.1,
        type: 'negative',
        confidence: 0.85,
        source: 'System',
        timestamp: Date.now(),
        context: 'Tolerancia a erros antes de marcar como negativo',
        evolutionHistory: []
      },
      {
        id: 'param_tool_timeout',
        name: 'tool_timeout',
        value: 30000,
        type: 'positive',
        confidence: 0.9,
        source: 'System',
        timestamp: Date.now(),
        context: 'Timeout padrao para execucao de ferramentas (ms)',
        evolutionHistory: []
      },
      {
        id: 'param_max_concurrent_tasks',
        name: 'max_concurrent_tasks',
        value: 8,
        type: 'positive',
        confidence: 0.8,
        source: 'System',
        timestamp: Date.now(),
        context: 'Maximo de tarefas concorrentes',
        evolutionHistory: []
      },
      {
        id: 'param_self_critique_cycles',
        name: 'self_critique_cycles',
        value: 3,
        type: 'positive',
        confidence: 0.75,
        source: 'System',
        timestamp: Date.now(),
        context: 'Ciclos de auto-critica antes de finalizar resposta',
        evolutionHistory: []
      },
      {
        id: 'param_parameter_decay',
        name: 'parameter_decay',
        value: 0.01,
        type: 'neutral',
        confidence: 0.7,
        source: 'System',
        timestamp: Date.now(),
        context: 'Taxa de decaimento de parametros nao utilizados',
        evolutionHistory: []
      }
    ];

    defaults.forEach(param => {
      this.parameters.set(param.id, param);
    });
  }

  // Adiciona ou atualiza um parâmetro
  addOrUpdateParameter(param: AgentParameter): void {
    const existing = this.parameters.get(param.id);
    
    if (existing) {
      // Evolução do parâmetro existente
      const evolution: ParameterEvolution = {
        iteration: this.currentCycle,
        oldValue: existing.value,
        newValue: param.value,
        reason: `Evolucao ciclo ${this.currentCycle}: ${param.context}`,
        timestamp: Date.now(),
        mindSource: param.source
      };
      
      param.evolutionHistory = [...existing.evolutionHistory, evolution];
    }
    
    this.parameters.set(param.id, param);
    
    // Limita o número total de parâmetros
    if (this.parameters.size > this.MAX_PARAMETERS) {
      this.pruneOldestParameters();
    }
  }

  // Executa um ciclo de evolução
  async evolveCycle(metrics: PerformanceMetrics): Promise<EvolutionCycle> {
    this.currentCycle++;
    
    const paramsBefore = Array.from(this.parameters.values());
    
    // Analisa métricas e ajusta parâmetros
    this.adaptParametersToPerformance(metrics);
    
    // Identifica padrões nos parâmetros
    const patterns = this.identifyPatterns();
    
    // Aplica melhorias baseadas nos padrões
    this.applyPatternImprovements(patterns);
    
    const paramsAfter = Array.from(this.parameters.values());
    
    const cycle: EvolutionCycle = {
      cycle: this.currentCycle,
      parametersBefore: paramsBefore,
      parametersAfter: paramsAfter,
      improvements: this.detectImprovements(paramsBefore, paramsAfter),
      regressions: this.detectRegressions(paramsBefore, paramsAfter),
      learningPoints: patterns,
      timestamp: Date.now(),
      selfModification: this.autoEvolve
    };
    
    this.evolutionHistory.push(cycle);
    
    // Mantém apenas os últimos 100 ciclos no histórico
    if (this.evolutionHistory.length > 100) {
      this.evolutionHistory = this.evolutionHistory.slice(-100);
    }
    
    return cycle;
  }

  // Adapta parâmetros baseado no desempenho
  private adaptParametersToPerformance(metrics: PerformanceMetrics): void {
    // Ajusta learning_rate baseado no successRate
    const learningRate = this.parameters.get('param_learning_rate');
    if (learningRate && metrics.successRate < 0.7) {
      learningRate.value = Math.min(0.01, (learningRate.value as number) * 1.1);
      learningRate.timestamp = Date.now();
    } else if (learningRate && metrics.successRate > 0.95) {
      learningRate.value = Math.max(0.0001, (learningRate.value as number) * 0.95);
      learningRate.timestamp = Date.now();
    }

    // Ajusta debate_rounds baseado no avgResponseTime
    const debateRounds = this.parameters.get('param_debate_rounds');
    if (debateRounds && metrics.avgResponseTime > 5000) {
      debateRounds.value = Math.max(1, (debateRounds.value as number) - 1);
      debateRounds.timestamp = Date.now();
    } else if (debateRounds && metrics.avgResponseTime < 1000) {
      debateRounds.value = Math.min(5, (debateRounds.value as number) + 1);
      debateRounds.timestamp = Date.now();
    }

    // Ajusta confidence_threshold baseado na eficiência
    const confidenceThreshold = this.parameters.get('param_confidence_threshold');
    if (confidenceThreshold && metrics.efficiency < 0.6) {
      confidenceThreshold.value = Math.max(0.5, (confidenceThreshold.value as number) - 0.05);
      confidenceThreshold.timestamp = Date.now();
    }
  }

  // Identifica padrões nos parâmetros
  private identifyPatterns(): string[] {
    const patterns: string[] = [];
    const params = Array.from(this.parameters.values());
    
    // Analisa distribuição de tipos
    const positiveCount = params.filter(p => p.type === 'positive').length;
    const negativeCount = params.filter(p => p.type === 'negative').length;
    
    const total = params.length;
    
    if (positiveCount / total > 0.7) {
      patterns.push('Alta proporcao de parametros positivos - modelo otimista');
    }
    if (negativeCount / total > 0.3) {
      patterns.push('Alta proporcao de parametros negativos - necessario ajuste');
    }
    
    // Analisa confiança média
    const avgConfidence = params.reduce((sum, p) => sum + p.confidence, 0) / total;
    if (avgConfidence < 0.6) {
      patterns.push('Confianca media baixa - necessario mais ciclos de debate');
    }
    
    // Analisa parâmetros mais evoluídos
    const mostEvolved = params.sort((a, b) => b.evolutionHistory.length - a.evolutionHistory.length)[0];
    if (mostEvolved && mostEvolved.evolutionHistory.length > 10) {
      patterns.push(`Parametro ${mostEvolved.name} altamente evolutivo - estabilizar`);
    }
    
    return patterns;
  }

  // Aplica melhorias baseadas nos padrões identificados
  private applyPatternImprovements(patterns: string[]): void {
    patterns.forEach(pattern => {
      if (pattern.includes('Confianca media baixa')) {
        const selfCritique = this.parameters.get('param_self_critique_cycles');
        if (selfCritique) {
          selfCritique.value = (selfCritique.value as number) + 1;
          selfCritique.timestamp = Date.now();
        }
      }
      
      if (pattern.includes('altamente evolutivo')) {
        const evolutionAggressiveness = this.parameters.get('param_evolution_aggressiveness');
        if (evolutionAggressiveness) {
          evolutionAggressiveness.value = Math.max(0.1, (evolutionAggressiveness.value as number) - 0.1);
          evolutionAggressiveness.timestamp = Date.now();
        }
      }
    });
  }

  // Detecta melhorias entre ciclos
  private detectImprovements(before: AgentParameter[], after: AgentParameter[]): string[] {
    const improvements: string[] = [];
    
    after.forEach(afterParam => {
      const beforeParam = before.find(p => p.id === afterParam.id);
      if (beforeParam) {
        if (afterParam.confidence > beforeParam.confidence) {
          improvements.push(`${afterParam.name}: confianca aumentou ${(afterParam.confidence - beforeParam.confidence).toFixed(3)}`);
        }
        if (afterParam.type === 'positive' && beforeParam.type !== 'positive') {
          improvements.push(`${afterParam.name}: convertido para positivo`);
        }
      }
    });
    
    return improvements;
  }

  // Detecta regressões entre ciclos
  private detectRegressions(before: AgentParameter[], after: AgentParameter[]): string[] {
    const regressions: string[] = [];
    
    after.forEach(afterParam => {
      const beforeParam = before.find(p => p.id === afterParam.id);
      if (beforeParam) {
        if (afterParam.confidence < beforeParam.confidence * 0.9) {
          regressions.push(`${afterParam.name}: confianca caiu significativamente`);
        }
        if (afterParam.type === 'negative' && beforeParam.type !== 'negative') {
          regressions.push(`${afterParam.name}: convertido para negativo`);
        }
      }
    });
    
    return regressions;
  }

  // Remove parâmetros mais antigos
  private pruneOldestParameters(): void {
    const sorted = Array.from(this.parameters.entries())
      .sort((a, b) => a[1].timestamp - b[1].timestamp);
    
    const toRemove = sorted.slice(0, Math.floor(this.MAX_PARAMETERS * 0.1));
    toRemove.forEach(([id]) => this.parameters.delete(id));
  }

  // Gera uma modificação de código auto-induzida
  generateSelfModification(target: string, reason: string): SelfModification {
    return {
      id: `mod_${Date.now()}`,
      target,
      oldCode: '',
      newCode: '',
      reason,
      timestamp: Date.now(),
      verified: false,
      rollbackPoint: `cycle_${this.currentCycle}`
    };
  }

  // Getters
  getParameters(): AgentParameter[] {
    return Array.from(this.parameters.values());
  }

  getParameter(id: string): AgentParameter | undefined {
    return this.parameters.get(id);
  }

  getEvolutionHistory(): EvolutionCycle[] {
    return this.evolutionHistory;
  }

  getCurrentCycle(): number {
    return this.currentCycle;
  }

  getPositiveParameters(): AgentParameter[] {
    return Array.from(this.parameters.values()).filter(p => p.type === 'positive');
  }

  getNegativeParameters(): AgentParameter[] {
    return Array.from(this.parameters.values()).filter(p => p.type === 'negative');
  }

  // Exporta todos os parâmetros para persistência
  exportParameters(): string {
    return JSON.stringify({
      cycle: this.currentCycle,
      timestamp: Date.now(),
      parameters: Array.from(this.parameters.values()),
      evolutionHistory: this.evolutionHistory.slice(-10)
    }, null, 2);
  }

  // Importa parâmetros de uma exportação
  importParameters(data: string): void {
    try {
      const parsed = JSON.parse(data);
      if (parsed.parameters) {
        parsed.parameters.forEach((param: AgentParameter) => {
          this.parameters.set(param.id, param);
        });
      }
      if (parsed.cycle) {
        this.currentCycle = parsed.cycle;
      }
    } catch (error) {
      console.error('Erro ao importar parametros:', error);
    }
  }
}

export const createEvolutionEngine = (autoEvolve?: boolean) => {
  return new EvolutionEngine(autoEvolve);
};
