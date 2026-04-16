// BRX-ENGINE - Núcleo Principal
// Sistema de IA Auto-Evolutiva e Soberana

import type { 
  BRXEngineState, 
  PerformanceMetrics, 
  AgentParameter,
  CircularDebate,
  ToolResult 
} from '../types';
import { EightMindsSystem, DEFAULT_MINDS } from '../minds/eight-minds';
import { EvolutionEngine } from './evolution-engine';
import { BRXToolkit } from '../tools/toolkit';
import { BRXSandbox } from '../sandbox/sandbox';
import { BRXMemorySystem } from '../memory/memory-system';

export class BRXEngine {
  private version: string = '1.0.0';
  private state: BRXEngineState;
  private minds: EightMindsSystem;
  private evolution: EvolutionEngine;
  private toolkit: BRXToolkit;
  private sandbox: BRXSandbox;
  private memory: BRXMemorySystem;
  private running: boolean;
  private evolutionInterval: number | null;
  private metricsHistory: PerformanceMetrics[];

  constructor() {
    this.minds = new EightMindsSystem(DEFAULT_MINDS);
    this.evolution = new EvolutionEngine(true);
    this.toolkit = new BRXToolkit();
    this.sandbox = new BRXSandbox(true);
    this.memory = new BRXMemorySystem();
    this.running = false;
    this.evolutionInterval = null;
    this.metricsHistory = [];
    
    // Inicializa estado
    this.state = {
      version: this.version,
      cycle: 0,
      minds: DEFAULT_MINDS,
      parameters: [],
      memory: [],
      evolutionHistory: [],
      isRunning: false,
      lastUpdate: Date.now(),
      performance: this.getInitialMetrics()
    };
    
    // Inicializa parâmetros padrão
    this.evolution.initializeDefaultParameters();
    
    // Cria ambiente sandbox padrão
    this.sandbox.createEnvironment('default');
    
    console.log(`[BRX-ENGINE v${this.version}] Inicializado com sucesso`);
    console.log(`[BRX-ENGINE] 8 Mentes ativas | 45+ Ferramentas | Sandbox isolado`);
  }

  private getInitialMetrics(): PerformanceMetrics {
    return {
      avgResponseTime: 0,
      successRate: 1.0,
      parameterCount: 0,
      memoryUsage: 0,
      cycleSpeed: 0,
      efficiency: 1.0
    };
  }

  // Inicia o motor de auto-evolução
  start(): void {
    if (this.running) return;
    
    this.running = true;
    this.state.isRunning = true;
    
    console.log('[BRX-ENGINE] Motor de auto-evolucao iniciado');
    
    // Ciclo de evolução automática
    this.evolutionInterval = window.setInterval(() => {
      this.runEvolutionCycle();
    }, 30000); // A cada 30 segundos
    
    // Ciclo de consolidação de memória
    window.setInterval(() => {
      this.memory.consolidate();
    }, 60000); // A cada minuto
  }

  // Para o motor
  stop(): void {
    this.running = false;
    this.state.isRunning = false;
    
    if (this.evolutionInterval) {
      clearInterval(this.evolutionInterval);
      this.evolutionInterval = null;
    }
    
    console.log('[BRX-ENGINE] Motor parado');
  }

  // Executa um ciclo completo de evolução
  private async runEvolutionCycle(): Promise<void> {
    this.state.cycle++;
    
    // Coleta métricas atuais
    const metrics = this.collectMetrics();
    this.metricsHistory.push(metrics);
    
    // Mantém apenas últimas 100 métricas
    if (this.metricsHistory.length > 100) {
      this.metricsHistory = this.metricsHistory.slice(-100);
    }
    
    // Executa evolução
    const cycle = await this.evolution.evolveCycle(metrics);
    
    // Atualiza estado
    this.state.parameters = this.evolution.getParameters();
    this.state.evolutionHistory.push(cycle);
    this.state.performance = metrics;
    this.state.lastUpdate = Date.now();
    
    // Armazena na memória
    this.memory.store(
      `Ciclo de evolucao ${this.state.cycle} completado. ${cycle.improvements.length} melhorias, ${cycle.regressions.length} regressoes.`,
      'evolution_cycle',
      0.7
    );
    
    console.log(`[BRX-ENGINE] Ciclo ${this.state.cycle} completado | Eficiencia: ${(metrics.efficiency * 100).toFixed(1)}%`);
  }

  // Coleta métricas de desempenho
  private collectMetrics(): PerformanceMetrics {
    const params = this.evolution.getParameters();
    const memories = this.memory.getStats();
    const tools = this.toolkit.getExecutionLog();
    
    const recentTools = tools.slice(-10);
    const avgResponseTime = recentTools.length > 0 
      ? recentTools.reduce((sum, t) => sum + t.duration, 0) / recentTools.length 
      : 0;
    
    const successRate = recentTools.length > 0
      ? recentTools.filter(t => t.success).length / recentTools.length
      : 1.0;
    
    return {
      avgResponseTime,
      successRate,
      parameterCount: params.length,
      memoryUsage: memories.total,
      cycleSpeed: 30000, // ms por ciclo
      efficiency: this.calculateEfficiency(successRate, params.length, memories.total)
    };
  }

  // Calcula eficiência geral
  private calculateEfficiency(successRate: number, paramCount: number, memoryCount: number): number {
    const paramEfficiency = Math.min(paramCount / 100, 1.0);
    const memoryEfficiency = Math.min(memoryCount / 1000, 1.0);
    
    return (successRate * 0.5 + paramEfficiency * 0.25 + memoryEfficiency * 0.25);
  }

  // Processa uma solicitação usando o sistema de 8 mentes
  async processRequest(request: string, context?: string): Promise<{
    response: string;
    debate: CircularDebate;
    parameters: AgentParameter[];
    toolsUsed: string[];
  }> {
    const startTime = Date.now();
    
    // Armazena contexto na memória
    if (context) {
      this.memory.store(context, 'request_context', 0.6);
    }
    
    // Recupera contexto relevante
    const relevantContext = this.memory.getRelevantContext(request, 3);
    const enrichedRequest = `${request}\n\nContexto relevante: ${relevantContext.map(m => m.content).join('; ')}`;
    
    // Executa debate circular
    const debateResult = await this.minds.conductDebate(request, enrichedRequest);
    
    // Executa ferramentas relevantes
    const toolsUsed: string[] = [];
    
    // Verifica se precisa de busca web
    if (request.toLowerCase().includes('pesquisar') || request.toLowerCase().includes('buscar')) {
      const searchResult = await this.toolkit.executeTool('web_search', { query: request, maxResults: 3 });
      if (searchResult.success) {
        toolsUsed.push('web_search');
        this.memory.store(searchResult.output, 'web_search_result', 0.5);
      }
    }
    
    // Verifica se precisa de análise
    if (request.toLowerCase().includes('analisar') || request.toLowerCase().includes('analise')) {
      const analysisResult = await this.toolkit.executeTool('self_critique', { 
        content: debateResult.consensus,
        criteria: ['accuracy', 'completeness']
      });
      if (analysisResult.success) {
        toolsUsed.push('self_critique');
      }
    }
    
    // Gera parâmetros do debate
    const parameters = debateResult.parameters;
    parameters.forEach(p => this.evolution.addOrUpdateParameter(p));
    
    // Cria registro do debate
    const debate: CircularDebate = {
      id: `debate_${Date.now()}`,
      topic: request,
      rounds: this.minds.getDebateHistory(),
      finalConsensus: debateResult.consensus,
      parameters,
      startTime,
      endTime: Date.now(),
      iterations: this.minds.getDebateHistory().length
    };
    
    // Armazena resultado na memória
    this.memory.store(
      `Processamento: "${request.substring(0, 50)}..." | Consenso: ${debateResult.consensus.substring(0, 100)}...`,
      'processing_result',
      debateResult.confidence
    );
    
    return {
      response: debateResult.consensus,
      debate,
      parameters,
      toolsUsed
    };
  }

  // Executa ferramenta diretamente
  async executeTool(toolName: string, input: any): Promise<ToolResult> {
    return this.toolkit.executeTool(toolName, input);
  }

  // Executa código em sandbox
  async executeInSandbox(envId: string, type: 'python' | 'shell' | 'javascript', code: string): Promise<ToolResult> {
    switch (type) {
      case 'python':
        return this.sandbox.executePython(envId, code);
      case 'shell':
        return this.sandbox.executeShell(envId, code);
      case 'javascript':
        return this.sandbox.executeJavaScript(envId, code);
      default:
        return {
          success: false,
          output: '',
          error: `Tipo de execucao desconhecido: ${type}`,
          executionTime: 0
        };
    }
  }

  // Exporta estado completo para persistência
  exportState(): string {
    return JSON.stringify({
      version: this.version,
      timestamp: Date.now(),
      state: this.state,
      parameters: this.evolution.exportParameters(),
      memories: this.memory.exportMemories()
    }, null, 2);
  }

  // Importa estado completo
  importState(data: string): void {
    try {
      const parsed = JSON.parse(data);
      
      if (parsed.state) {
        this.state = { ...this.state, ...parsed.state };
      }
      
      if (parsed.parameters) {
        this.evolution.importParameters(parsed.parameters);
      }
      
      if (parsed.memories) {
        this.memory.importMemories(parsed.memories);
      }
      
      console.log('[BRX-ENGINE] Estado importado com sucesso');
    } catch (error) {
      console.error('[BRX-ENGINE] Erro ao importar estado:', error);
    }
  }

  // Getters
  getState(): BRXEngineState {
    return { ...this.state };
  }

  getVersion(): string {
    return this.version;
  }

  isRunning(): boolean {
    return this.running;
  }

  getMinds() {
    return this.minds;
  }

  getEvolution() {
    return this.evolution;
  }

  getToolkit() {
    return this.toolkit;
  }

  getSandbox() {
    return this.sandbox;
  }

  getMemory() {
    return this.memory;
  }

  getMetricsHistory(): PerformanceMetrics[] {
    return this.metricsHistory;
  }

  // Estatísticas
  getStats() {
    return {
      version: this.version,
      cycle: this.state.cycle,
      minds: this.minds.getActiveMinds().length,
      parameters: this.evolution.getParameters().length,
      positiveParams: this.evolution.getPositiveParameters().length,
      negativeParams: this.evolution.getNegativeParameters().length,
      tools: this.toolkit.getToolCount(),
      memories: this.memory.getStats(),
      sandboxes: this.sandbox.getEnvironmentCount(),
      performance: this.state.performance
    };
  }
}

// Instância singleton
let engineInstance: BRXEngine | null = null;

export const getBRXEngine = (): BRXEngine => {
  if (!engineInstance) {
    engineInstance = new BRXEngine();
  }
  return engineInstance;
};

export const createBRXEngine = (): BRXEngine => {
  return new BRXEngine();
};
