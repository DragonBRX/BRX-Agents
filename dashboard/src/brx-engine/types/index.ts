// BRX-ENGINE - Tipos Fundamentais
// Sistema de IA Auto-Evolutiva e Soberana

export interface MindConfig {
  name: string;
  specialty: string;
  objective: string;
  focus: string;
  weight: number;
  active: boolean;
}

export interface AgentParameter {
  id: string;
  name: string;
  value: any;
  type: 'positive' | 'negative' | 'neutral';
  confidence: number;
  source: string;
  timestamp: number;
  context: string;
  evolutionHistory: ParameterEvolution[];
}

export interface ParameterEvolution {
  iteration: number;
  oldValue: any;
  newValue: any;
  reason: string;
  timestamp: number;
  mindSource: string;
}

export interface DebateRound {
  round: number;
  mindName: string;
  input: string;
  output: string;
  parameters: AgentParameter[];
  confidence: number;
  timestamp: number;
}

export interface CircularDebate {
  id: string;
  topic: string;
  rounds: DebateRound[];
  finalConsensus: string;
  parameters: AgentParameter[];
  startTime: number;
  endTime: number;
  iterations: number;
}

export interface ToolDefinition {
  name: string;
  description: string;
  category: 'execution' | 'search' | 'analysis' | 'creation' | 'system';
  parameters: Record<string, any>;
  execute: (input: any) => Promise<ToolResult>;
  requiresApproval: boolean;
  riskLevel: 'low' | 'medium' | 'high';
}

export interface ToolResult {
  success: boolean;
  output: string;
  error?: string;
  executionTime: number;
  data?: any;
}

export interface SkillExecution {
  id: string;
  skillName: string;
  input: string;
  output: string;
  success: boolean;
  timestamp: number;
  executionTime: number;
}

export interface MemoryEntry {
  id: string;
  type: 'short' | 'medium' | 'long';
  content: string;
  context: string;
  importance: number;
  timestamp: number;
  accessCount: number;
  lastAccess: number;
  associations: string[];
}

export interface EvolutionCycle {
  cycle: number;
  parametersBefore: AgentParameter[];
  parametersAfter: AgentParameter[];
  improvements: string[];
  regressions: string[];
  learningPoints: string[];
  timestamp: number;
  selfModification: boolean;
}

export interface BRXEngineState {
  version: string;
  cycle: number;
  minds: MindConfig[];
  parameters: AgentParameter[];
  memory: MemoryEntry[];
  evolutionHistory: EvolutionCycle[];
  isRunning: boolean;
  lastUpdate: number;
  performance: PerformanceMetrics;
}

export interface PerformanceMetrics {
  avgResponseTime: number;
  successRate: number;
  parameterCount: number;
  memoryUsage: number;
  cycleSpeed: number;
  efficiency: number;
}

export interface SandboxEnvironment {
  id: string;
  isolated: boolean;
  tools: string[];
  permissions: string[];
  executionLog: ExecutionLog[];
  active: boolean;
}

export interface ExecutionLog {
  timestamp: number;
  command: string;
  output: string;
  error?: string;
  duration: number;
}

export interface WebSearchResult {
  query: string;
  results: {
    title: string;
    url: string;
    snippet: string;
    relevance: number;
  }[];
  timestamp: number;
}

export interface SelfModification {
  id: string;
  target: string;
  oldCode: string;
  newCode: string;
  reason: string;
  timestamp: number;
  verified: boolean;
  rollbackPoint: string;
}

export interface ConsensusResult {
  agreement: number;
  consensus: string;
  dissentingViews: string[];
  parameters: AgentParameter[];
  confidence: number;
}
