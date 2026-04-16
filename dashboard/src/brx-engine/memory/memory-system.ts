// BRX-ENGINE - Sistema de Memória
// Gerenciamento de memória de curto, médio e longo prazo

import type { MemoryEntry } from '../types';

interface MemoryTier {
  name: 'short' | 'medium' | 'long';
  maxSize: number;
  retentionRate: number;
  decayRate: number;
}

export class BRXMemorySystem {
  private shortTerm: Map<string, MemoryEntry>;
  private mediumTerm: Map<string, MemoryEntry>;
  private longTerm: Map<string, MemoryEntry>;
  private tiers: Record<string, MemoryTier>;
  private accessPatterns: Map<string, number[]>;

  constructor() {
    this.shortTerm = new Map();
    this.mediumTerm = new Map();
    this.longTerm = new Map();
    this.accessPatterns = new Map();
    
    this.tiers = {
      short: { name: 'short', maxSize: 100, retentionRate: 0.9, decayRate: 0.1 },
      medium: { name: 'medium', maxSize: 500, retentionRate: 0.7, decayRate: 0.05 },
      long: { name: 'long', maxSize: 10000, retentionRate: 0.95, decayRate: 0.01 }
    };
  }

  // Armazena informação na memória
  store(content: string, context: string, importance: number = 0.5, type?: 'short' | 'medium' | 'long'): MemoryEntry {
    const entry: MemoryEntry = {
      id: `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type: type || this.determineMemoryType(importance),
      content,
      context,
      importance: Math.max(0, Math.min(1, importance)),
      timestamp: Date.now(),
      accessCount: 0,
      lastAccess: Date.now(),
      associations: []
    };

    // Armazena na tier apropriada
    switch (entry.type) {
      case 'short':
        this.shortTerm.set(entry.id, entry);
        this.enforceTierLimit('short');
        break;
      case 'medium':
        this.mediumTerm.set(entry.id, entry);
        this.enforceTierLimit('medium');
        break;
      case 'long':
        this.longTerm.set(entry.id, entry);
        this.enforceTierLimit('long');
        break;
    }

    return entry;
  }

  // Recupera informação da memória
  retrieve(id: string): MemoryEntry | undefined {
    // Busca em todas as tiers
    let entry = this.shortTerm.get(id) || this.mediumTerm.get(id) || this.longTerm.get(id);
    
    if (entry) {
      entry.accessCount++;
      entry.lastAccess = Date.now();
      
      // Registra padrão de acesso
      this.recordAccessPattern(id);
      
      // Promove memória frequentemente acessada
      this.considerPromotion(entry);
    }
    
    return entry;
  }

  // Busca por conteúdo similar
  search(query: string, type?: 'short' | 'medium' | 'long'): MemoryEntry[] {
    const results: MemoryEntry[] = [];
    const queryLower = query.toLowerCase();
    
    const searchInTier = (tier: Map<string, MemoryEntry>) => {
      tier.forEach(entry => {
        const similarity = this.calculateSimilarity(queryLower, entry.content.toLowerCase());
        if (similarity > 0.3) {
          results.push({ ...entry, importance: entry.importance * similarity });
        }
      });
    };
    
    if (!type || type === 'short') searchInTier(this.shortTerm);
    if (!type || type === 'medium') searchInTier(this.mediumTerm);
    if (!type || type === 'long') searchInTier(this.longTerm);
    
    return results.sort((a, b) => b.importance - a.importance);
  }

  // Recupera contexto relevante
  getRelevantContext(currentContext: string, maxEntries: number = 5): MemoryEntry[] {
    const allMemories = [
      ...Array.from(this.shortTerm.values()),
      ...Array.from(this.mediumTerm.values()),
      ...Array.from(this.longTerm.values())
    ];
    
    // Calcula relevância baseada em contexto e importância
    const scored = allMemories.map(entry => ({
      entry,
      score: this.calculateRelevanceScore(entry, currentContext)
    }));
    
    return scored
      .sort((a, b) => b.score - a.score)
      .slice(0, maxEntries)
      .map(s => s.entry);
  }

  // Cria associação entre memórias
  createAssociation(id1: string, id2: string): boolean {
    const entry1 = this.retrieve(id1);
    const entry2 = this.retrieve(id2);
    
    if (entry1 && entry2) {
      if (!entry1.associations.includes(id2)) {
        entry1.associations.push(id2);
      }
      if (!entry2.associations.includes(id1)) {
        entry2.associations.push(id1);
      }
      return true;
    }
    
    return false;
  }

  // Executa ciclo de consolidação de memória
  consolidate(): void {
    // Promove memórias de curto prazo frequentemente acessadas
    this.shortTerm.forEach((entry, id) => {
      if (entry.accessCount > 5 && entry.importance > 0.7) {
        this.promoteToMedium(id);
      }
    });
    
    // Promove memórias de médio prazo para longo prazo
    this.mediumTerm.forEach((entry, id) => {
      if (entry.accessCount > 20 && entry.importance > 0.8) {
        this.promoteToLong(id);
      }
    });
    
    // Remove memórias antigas de curto prazo
    this.pruneShortTerm();
    
    // Decai importância de memórias não acessadas
    this.decayMemories();
  }

  // Determina tipo de memória baseado na importância
  private determineMemoryType(importance: number): 'short' | 'medium' | 'long' {
    if (importance > 0.8) return 'long';
    if (importance > 0.5) return 'medium';
    return 'short';
  }

  // Calcula similaridade simples entre strings
  private calculateSimilarity(a: string, b: string): number {
    const wordsA = new Set(a.split(/\s+/));
    const wordsB = new Set(b.split(/\s+/));
    
    const intersection = new Set([...wordsA].filter(x => wordsB.has(x)));
    const union = new Set([...wordsA, ...wordsB]);
    
    return intersection.size / union.size;
  }

  // Calcula score de relevância
  private calculateRelevanceScore(entry: MemoryEntry, context: string): number {
    const contextSimilarity = this.calculateSimilarity(entry.context.toLowerCase(), context.toLowerCase());
    const recency = Math.exp(-(Date.now() - entry.timestamp) / (24 * 60 * 60 * 1000)); // Decaimento diário
    const accessFrequency = Math.log(entry.accessCount + 1);
    
    return (
      entry.importance * 0.4 +
      contextSimilarity * 0.3 +
      recency * 0.2 +
      Math.min(accessFrequency / 5, 0.1)
    );
  }

  // Registra padrão de acesso
  private recordAccessPattern(id: string): void {
    const pattern = this.accessPatterns.get(id) || [];
    pattern.push(Date.now());
    
    // Mantém apenas últimos 20 acessos
    if (pattern.length > 20) {
      pattern.shift();
    }
    
    this.accessPatterns.set(id, pattern);
  }

  // Considera promoção de memória
  private considerPromotion(entry: MemoryEntry): void {
    const pattern = this.accessPatterns.get(entry.id) || [];
    
    if (pattern.length < 3) return;
    
    // Verifica se houve acessos frequentes recentemente
    const recentAccesses = pattern.filter(t => Date.now() - t < 60000).length;
    
    if (recentAccesses >= 3) {
      if (entry.type === 'short') {
        this.promoteToMedium(entry.id);
      } else if (entry.type === 'medium') {
        this.promoteToLong(entry.id);
      }
    }
  }

  // Promove memória de curto para médio prazo
  private promoteToMedium(id: string): void {
    const entry = this.shortTerm.get(id);
    if (entry) {
      entry.type = 'medium';
      this.mediumTerm.set(id, entry);
      this.shortTerm.delete(id);
      this.enforceTierLimit('medium');
    }
  }

  // Promove memória de médio para longo prazo
  private promoteToLong(id: string): void {
    const entry = this.mediumTerm.get(id);
    if (entry) {
      entry.type = 'long';
      this.longTerm.set(id, entry);
      this.mediumTerm.delete(id);
      this.enforceTierLimit('long');
    }
  }

  // Remove memórias antigas de curto prazo
  private pruneShortTerm(): void {
    const now = Date.now();
    const maxAge = 5 * 60 * 1000; // 5 minutos
    
    this.shortTerm.forEach((entry, id) => {
      if (now - entry.timestamp > maxAge && entry.accessCount < 2) {
        this.shortTerm.delete(id);
      }
    });
  }

  // Decai importância de memórias não acessadas
  private decayMemories(): void {
    const now = Date.now();
    
    [this.shortTerm, this.mediumTerm, this.longTerm].forEach(tier => {
      tier.forEach(entry => {
        const timeSinceAccess = now - entry.lastAccess;
        const decayFactor = Math.exp(-timeSinceAccess / (60 * 60 * 1000)); // Decaimento por hora
        entry.importance *= decayFactor;
        
        // Remove memórias com importância muito baixa
        if (entry.importance < 0.1) {
          tier.delete(entry.id);
        }
      });
    });
  }

  // Força limite de tier
  private enforceTierLimit(tierName: 'short' | 'medium' | 'long'): void {
    const tier = tierName === 'short' ? this.shortTerm : 
                 tierName === 'medium' ? this.mediumTerm : this.longTerm;
    const limit = this.tiers[tierName].maxSize;
    
    if (tier.size > limit) {
      // Remove entradas menos importantes
      const entries = Array.from(tier.entries());
      entries.sort((a, b) => a[1].importance - b[1].importance);
      
      const toRemove = entries.slice(0, tier.size - limit);
      toRemove.forEach(([id]) => tier.delete(id));
    }
  }

  // Getters
  getStats(): { short: number; medium: number; long: number; total: number } {
    return {
      short: this.shortTerm.size,
      medium: this.mediumTerm.size,
      long: this.longTerm.size,
      total: this.shortTerm.size + this.mediumTerm.size + this.longTerm.size
    };
  }

  getAllMemories(): MemoryEntry[] {
    return [
      ...Array.from(this.shortTerm.values()),
      ...Array.from(this.mediumTerm.values()),
      ...Array.from(this.longTerm.values())
    ];
  }

  getMemoriesByType(type: 'short' | 'medium' | 'long'): MemoryEntry[] {
    const tier = type === 'short' ? this.shortTerm : 
                 type === 'medium' ? this.mediumTerm : this.longTerm;
    return Array.from(tier.values());
  }

  clear(): void {
    this.shortTerm.clear();
    this.mediumTerm.clear();
    this.longTerm.clear();
    this.accessPatterns.clear();
  }

  // Exporta memórias para persistência
  exportMemories(): string {
    return JSON.stringify({
      timestamp: Date.now(),
      short: Array.from(this.shortTerm.values()),
      medium: Array.from(this.mediumTerm.values()),
      long: Array.from(this.longTerm.values())
    }, null, 2);
  }

  // Importa memórias de persistência
  importMemories(data: string): void {
    try {
      const parsed = JSON.parse(data);
      
      if (parsed.short) {
        parsed.short.forEach((entry: MemoryEntry) => {
          this.shortTerm.set(entry.id, entry);
        });
      }
      if (parsed.medium) {
        parsed.medium.forEach((entry: MemoryEntry) => {
          this.mediumTerm.set(entry.id, entry);
        });
      }
      if (parsed.long) {
        parsed.long.forEach((entry: MemoryEntry) => {
          this.longTerm.set(entry.id, entry);
        });
      }
    } catch (error) {
      console.error('Erro ao importar memorias:', error);
    }
  }
}

export const createMemorySystem = () => {
  return new BRXMemorySystem();
};
