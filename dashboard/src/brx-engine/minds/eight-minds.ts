// BRX-ENGINE - Sistema de 8 Mentes
// Debate Circular e Processamento Multi-Perspectiva

import type { MindConfig, DebateRound, AgentParameter, ConsensusResult } from '../types';

export const DEFAULT_MINDS: MindConfig[] = [
  {
    name: 'Designer',
    specialty: 'Estrutura e Padroes de Dados',
    objective: 'Garantir que os parametros sigam uma arquitetura logica e escalavel',
    focus: 'Estrutura JSON, esquemas de dados, organizacao hierarquica',
    weight: 1.0,
    active: true
  },
  {
    name: 'Analista',
    specialty: 'Logica e Consistencia Tecnica',
    objective: 'Validar a precisao tecnica e a fundamentacao logica das informacoes',
    focus: 'Calculos, fatos cientificos, rigor logico, consistencia interna',
    weight: 1.0,
    active: true
  },
  {
    name: 'Inovador',
    specialty: 'Abordagens Criativas e Novas Perspectivas',
    objective: 'Expandir o conhecimento para alem do obvio, sugerindo novas conexoes',
    focus: 'Brainstorming, associacoes nao obvias, originalidade, tendencias futuras',
    weight: 1.0,
    active: true
  },
  {
    name: 'Critico',
    specialty: 'Identificacao de Falhas e Riscos (Red Teaming)',
    objective: 'Atuar como o advogado do diabo, encontrando erros e pontos fracos',
    focus: 'Contradicoes, vieses, erros de seguranca, excecoes nao tratadas',
    weight: 1.0,
    active: true
  },
  {
    name: 'Revisor',
    specialty: 'Qualidade Textual e Clareza de Comunicacao',
    objective: 'Refinar a linguagem para que seja clara, profissional e sem ambiguidades',
    focus: 'Gramatica, tom de voz, coesao, fluidez textual, terminologia',
    weight: 1.0,
    active: true
  },
  {
    name: 'Validador',
    specialty: 'Coerencia Tematica e Precisao de Dados',
    objective: 'Garantir que o conteudo esteja alinhado com o topico central e objetivos',
    focus: 'Relevancia, veracidade, alinhamento com a meta, utilidade pratica',
    weight: 1.0,
    active: true
  },
  {
    name: 'Estrategista',
    specialty: 'Planejamento e Utilidade dos Parametros',
    objective: 'Garantir que o parametro gerado tenha valor estrategico para o modelo',
    focus: 'Aplicacao pratica, escalabilidade, impacto no treinamento, visao macro',
    weight: 1.0,
    active: true
  },
  {
    name: 'Memoria',
    specialty: 'Contexto Historico e Persistencia de Dados',
    objective: 'Manter a continuidade do conhecimento entre os ciclos de debate',
    focus: 'Historico de parametros, referencias cruzadas, armazenamento, recuperacao',
    weight: 1.0,
    active: true
  }
];

export class EightMindsSystem {
  private minds: MindConfig[];
  private debateHistory: DebateRound[];
  private consensusThreshold: number;

  constructor(minds: MindConfig[] = DEFAULT_MINDS, consensusThreshold: number = 0.75) {
    this.minds = minds;
    this.debateHistory = [];
    this.consensusThreshold = consensusThreshold;
  }

  async conductDebate(topic: string, initialInput: string, maxRounds: number = 3): Promise<ConsensusResult> {
    this.debateHistory = [];
    
    let currentInput = initialInput;
    let allParameters: AgentParameter[] = [];
    
    for (let round = 0; round < maxRounds; round++) {
      
      for (const mind of this.minds.filter(m => m.active)) {
        const roundResult = await this.processMindRound(mind, topic, currentInput, round);
        this.debateHistory.push(roundResult);
        currentInput = roundResult.output;
        allParameters = [...allParameters, ...roundResult.parameters];
      }
      
      const consensus = this.calculateConsensus(allParameters);
      if (consensus.agreement >= this.consensusThreshold) {
        return consensus;
      }
    }
    
    return this.calculateConsensus(allParameters);
  }

  private async processMindRound(
    mind: MindConfig,
    topic: string,
    input: string,
    round: number
  ): Promise<DebateRound> {
    
    // Simulação do processamento da mente
    const processedOutput = this.simulateMindProcessing(mind, topic, input);
    
    // Gera parâmetros baseados no processamento
    const parameters = this.generateParametersFromMind(mind, processedOutput, topic);
    
    return {
      round,
      mindName: mind.name,
      input,
      output: processedOutput,
      parameters,
      confidence: this.calculateConfidence(mind, parameters),
      timestamp: Date.now()
    };
  }

  private simulateMindProcessing(mind: MindConfig, topic: string, _input: string): string {
    const perspectives: Record<string, string> = {
      Designer: `[Designer] Estruturando dados para "${topic}": Organizando hierarquias e padroes...`,
      Analista: `[Analista] Analisando logica de "${topic}": Verificando consistencia tecnica...`,
      Inovador: `[Inovador] Explorando inovacoes para "${topic}": Gerando novas conexoes...`,
      Critico: `[Critico] Critica construtiva de "${topic}": Identificando falhas potenciais...`,
      Revisor: `[Revisor] Refinando comunicacao de "${topic}": Melhorando clareza...`,
      Validador: `[Validador] Validando "${topic}": Verificando coerencia tematica...`,
      Estrategista: `[Estrategista] Estrategia para "${topic}": Maximizando valor pratico...`,
      Memoria: `[Memoria] Contextualizando "${topic}": Integrando conhecimento historico...`
    };

    return perspectives[mind.name] || `[${mind.name}] Processando "${topic}"...`;
  }

  private generateParametersFromMind(mind: MindConfig, _output: string, topic: string): AgentParameter[] {
    const params: AgentParameter[] = [];
    
    // Cada mente gera parâmetros específicos do seu domínio
    switch (mind.name) {
      case 'Designer':
        params.push({
          id: `design_${Date.now()}`,
          name: 'data_structure_quality',
          value: Math.random() * 0.3 + 0.7,
          type: 'positive',
          confidence: 0.85,
          source: mind.name,
          timestamp: Date.now(),
          context: topic,
          evolutionHistory: []
        });
        break;
      case 'Analista':
        params.push({
          id: `anal_${Date.now()}`,
          name: 'logical_consistency',
          value: Math.random() * 0.2 + 0.8,
          type: 'positive',
          confidence: 0.9,
          source: mind.name,
          timestamp: Date.now(),
          context: topic,
          evolutionHistory: []
        });
        break;
      case 'Inovador':
        params.push({
          id: `inov_${Date.now()}`,
          name: 'creativity_score',
          value: Math.random() * 0.4 + 0.6,
          type: 'positive',
          confidence: 0.75,
          source: mind.name,
          timestamp: Date.now(),
          context: topic,
          evolutionHistory: []
        });
        break;
      case 'Critico':
        params.push({
          id: `crit_${Date.now()}`,
          name: 'risk_level',
          value: Math.random() * 0.3,
          type: 'negative',
          confidence: 0.8,
          source: mind.name,
          timestamp: Date.now(),
          context: topic,
          evolutionHistory: []
        });
        break;
      case 'Revisor':
        params.push({
          id: `rev_${Date.now()}`,
          name: 'clarity_score',
          value: Math.random() * 0.2 + 0.8,
          type: 'positive',
          confidence: 0.85,
          source: mind.name,
          timestamp: Date.now(),
          context: topic,
          evolutionHistory: []
        });
        break;
      case 'Validador':
        params.push({
          id: `val_${Date.now()}`,
          name: 'accuracy_score',
          value: Math.random() * 0.2 + 0.8,
          type: 'positive',
          confidence: 0.9,
          source: mind.name,
          timestamp: Date.now(),
          context: topic,
          evolutionHistory: []
        });
        break;
      case 'Estrategista':
        params.push({
          id: `est_${Date.now()}`,
          name: 'strategic_value',
          value: Math.random() * 0.3 + 0.7,
          type: 'positive',
          confidence: 0.8,
          source: mind.name,
          timestamp: Date.now(),
          context: topic,
          evolutionHistory: []
        });
        break;
      case 'Memoria':
        params.push({
          id: `mem_${Date.now()}`,
          name: 'context_preservation',
          value: Math.random() * 0.2 + 0.8,
          type: 'positive',
          confidence: 0.85,
          source: mind.name,
          timestamp: Date.now(),
          context: topic,
          evolutionHistory: []
        });
        break;
    }
    
    return params;
  }

  private calculateConfidence(mind: MindConfig, parameters: AgentParameter[]): number {
    if (parameters.length === 0) return 0.5;
    const avgConfidence = parameters.reduce((sum, p) => sum + p.confidence, 0) / parameters.length;
    return avgConfidence * mind.weight;
  }

  private calculateConsensus(parameters: AgentParameter[]): ConsensusResult {
    if (parameters.length === 0) {
      return {
        agreement: 0,
        consensus: 'Nenhum parametro gerado',
        dissentingViews: [],
        parameters: [],
        confidence: 0
      };
    }

    const positiveParams = parameters.filter(p => p.type === 'positive');
    const negativeParams = parameters.filter(p => p.type === 'negative');
    
    const totalValue = parameters.reduce((sum, p) => sum + (p.value as number), 0);
    const avgValue = totalValue / parameters.length;
    
    const agreement = positiveParams.length / parameters.length;
    
    return {
      agreement,
      consensus: `Consenso atingido com ${(agreement * 100).toFixed(1)}% de acordo. Valor medio: ${avgValue.toFixed(3)}`,
      dissentingViews: negativeParams.map(p => `${p.name}: ${p.value}`),
      parameters,
      confidence: parameters.reduce((sum, p) => sum + p.confidence, 0) / parameters.length
    };
  }

  getDebateHistory(): DebateRound[] {
    return this.debateHistory;
  }

  getActiveMinds(): MindConfig[] {
    return this.minds.filter(m => m.active);
  }

  toggleMind(name: string): void {
    const mind = this.minds.find(m => m.name === name);
    if (mind) {
      mind.active = !mind.active;
    }
  }

  updateMindWeight(name: string, weight: number): void {
    const mind = this.minds.find(m => m.name === name);
    if (mind) {
      mind.weight = Math.max(0, Math.min(2, weight));
    }
  }
}

export const createEightMindsSystem = (customMinds?: MindConfig[]) => {
  return new EightMindsSystem(customMinds);
};
