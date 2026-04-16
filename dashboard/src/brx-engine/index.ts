// BRX-ENGINE - Exportações Principais
// Sistema de IA Auto-Evolutiva e Soberana

// Tipos
export * from './types';

// Núcleo
export { BRXEngine, getBRXEngine, createBRXEngine } from './core/brx-engine';
export { EvolutionEngine, createEvolutionEngine } from './core/evolution-engine';

// Mentes
export { EightMindsSystem, DEFAULT_MINDS, createEightMindsSystem } from './minds/eight-minds';

// Ferramentas
export { BRXToolkit, createToolkit } from './tools/toolkit';

// Sandbox
export { BRXSandbox, createSandbox } from './sandbox/sandbox';

// Memória
export { BRXMemorySystem, createMemorySystem } from './memory/memory-system';
