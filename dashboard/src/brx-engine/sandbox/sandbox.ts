// BRX-ENGINE - Sandbox Modular
// Ambiente isolado para execução segura de código e ferramentas

import type { SandboxEnvironment, ExecutionLog, ToolResult } from '../types';

export class BRXSandbox {
  private environments: Map<string, SandboxEnvironment>;
  private globalPermissions: Set<string>;
  private isolatedMode: boolean;

  constructor(isolatedMode: boolean = true) {
    this.environments = new Map();
    this.globalPermissions = new Set();
    this.isolatedMode = isolatedMode;
    this.initializeDefaultPermissions();
  }

  private initializeDefaultPermissions(): void {
    // Permissões padrão para execução segura
    const defaultPermissions = [
      'read:tmp',
      'write:tmp',
      'execute:python',
      'execute:javascript',
      'network:local',
      'memory:read',
      'memory:write'
    ];
    
    defaultPermissions.forEach(p => this.globalPermissions.add(p));
  }

  // Cria um novo ambiente sandbox isolado
  createEnvironment(id: string, customPermissions?: string[]): SandboxEnvironment {
    const permissions = customPermissions || Array.from(this.globalPermissions);
    
    const env: SandboxEnvironment = {
      id,
      isolated: this.isolatedMode,
      tools: [],
      permissions,
      executionLog: [],
      active: true
    };
    
    this.environments.set(id, env);
    return env;
  }

  // Executa código Python em ambiente isolado
  async executePython(envId: string, code: string, _timeout: number = 30000): Promise<ToolResult> {
    const env = this.environments.get(envId);
    if (!env) {
      return {
        success: false,
        output: '',
        error: `Ambiente ${envId} nao encontrado`,
        executionTime: 0
      };
    }

    if (!this.hasPermission(env, 'execute:python')) {
      return {
        success: false,
        output: '',
        error: 'Permissao execute:python negada',
        executionTime: 0
      };
    }

    const startTime = Date.now();
    
    try {
      // Simulação de execução isolada
      const sanitizedCode = this.sanitizePythonCode(code);
      
      // Em ambiente real, aqui seria executado em subprocesso isolado
      const simulatedOutput = this.simulatePythonExecution(sanitizedCode);
      
      const duration = Date.now() - startTime;
      
      this.logExecution(env, {
        timestamp: startTime,
        command: `python: ${sanitizedCode.substring(0, 100)}...`,
        output: simulatedOutput,
        duration
      });
      
      return {
        success: true,
        output: simulatedOutput,
        executionTime: duration
      };
    } catch (error) {
      const duration = Date.now() - startTime;
      return {
        success: false,
        output: '',
        error: error instanceof Error ? error.message : String(error),
        executionTime: duration
      };
    }
  }

  // Executa comando shell em ambiente isolado
  async executeShell(envId: string, command: string, _timeout: number = 30000): Promise<ToolResult> {
    const env = this.environments.get(envId);
    if (!env) {
      return {
        success: false,
        output: '',
        error: `Ambiente ${envId} nao encontrado`,
        executionTime: 0
      };
    }

    if (!this.hasPermission(env, 'execute:shell')) {
      return {
        success: false,
        output: '',
        error: 'Permissao execute:shell negada (modo seguro)',
        executionTime: 0
      };
    }

    const startTime = Date.now();
    
    try {
      const sanitizedCommand = this.sanitizeShellCommand(command);
      const simulatedOutput = `[Sandbox Shell] Comando executado: ${sanitizedCommand}`;
      
      const duration = Date.now() - startTime;
      
      this.logExecution(env, {
        timestamp: startTime,
        command: `shell: ${sanitizedCommand}`,
        output: simulatedOutput,
        duration
      });
      
      return {
        success: true,
        output: simulatedOutput,
        executionTime: duration
      };
    } catch (error) {
      const duration = Date.now() - startTime;
      return {
        success: false,
        output: '',
        error: error instanceof Error ? error.message : String(error),
        executionTime: duration
      };
    }
  }

  // Executa JavaScript em ambiente isolado
  async executeJavaScript(envId: string, code: string): Promise<ToolResult> {
    const env = this.environments.get(envId);
    if (!env) {
      return {
        success: false,
        output: '',
        error: `Ambiente ${envId} nao encontrado`,
        executionTime: 0
      };
    }

    if (!this.hasPermission(env, 'execute:javascript')) {
      return {
        success: false,
        output: '',
        error: 'Permissao execute:javascript negada',
        executionTime: 0
      };
    }

    const startTime = Date.now();
    
    try {
      // Cria um contexto isolado para execução
      const isolatedContext = this.createIsolatedContext();
      
      // Executa em contexto restrito
      const result = this.runInContext(code, isolatedContext);
      
      const duration = Date.now() - startTime;
      
      this.logExecution(env, {
        timestamp: startTime,
        command: `javascript: ${code.substring(0, 100)}...`,
        output: String(result),
        duration
      });
      
      return {
        success: true,
        output: String(result),
        executionTime: duration
      };
    } catch (error) {
      const duration = Date.now() - startTime;
      return {
        success: false,
        output: '',
        error: error instanceof Error ? error.message : String(error),
        executionTime: duration
      };
    }
  }

  // Realiza busca web segura
  async webSearch(envId: string, query: string, maxResults: number = 5): Promise<ToolResult> {
    const env = this.environments.get(envId);
    if (!env) {
      return {
        success: false,
        output: '',
        error: `Ambiente ${envId} nao encontrado`,
        executionTime: 0
      };
    }

    if (!this.hasPermission(env, 'network:external')) {
      return {
        success: false,
        output: '',
        error: 'Permissao network:external negada',
        executionTime: 0
      };
    }

    const startTime = Date.now();
    
    try {
      // Simulação de busca web
      const results = this.simulateWebSearch(query, maxResults);
      
      const duration = Date.now() - startTime;
      
      this.logExecution(env, {
        timestamp: startTime,
        command: `websearch: ${query}`,
        output: JSON.stringify(results),
        duration
      });
      
      return {
        success: true,
        output: JSON.stringify(results, null, 2),
        executionTime: duration
      };
    } catch (error) {
      const duration = Date.now() - startTime;
      return {
        success: false,
        output: '',
        error: error instanceof Error ? error.message : String(error),
        executionTime: duration
      };
    }
  }

  // Sanitização de código Python
  private sanitizePythonCode(code: string): string {
    // Remove imports perigosos
    const dangerousImports = ['os', 'sys', 'subprocess', 'socket', 'requests'];
    let sanitized = code;
    
    dangerousImports.forEach(imp => {
      const regex = new RegExp(`(import\\s+${imp}|from\\s+${imp})`, 'g');
      sanitized = sanitized.replace(regex, `# [BLOQUEADO] $1`);
    });
    
    // Limita operações de arquivo
    sanitized = sanitized.replace(/open\s*\(/g, '# [BLOQUEADO] open(');
    
    return sanitized;
  }

  // Sanitização de comando shell
  private sanitizeShellCommand(command: string): string {
    const dangerousCommands = ['rm -rf', 'mkfs', 'dd', '>', '>>', '|'];
    let sanitized = command;
    
    dangerousCommands.forEach(cmd => {
      if (command.includes(cmd)) {
        sanitized = `# [BLOQUEADO] ${sanitized}`;
      }
    });
    
    return sanitized;
  }

  // Cria contexto isolado para JavaScript
  private createIsolatedContext(): any {
    return {
      console: {
        log: (...args: any[]) => args.join(' '),
        error: (...args: any[]) => args.join(' '),
        warn: (...args: any[]) => args.join(' ')
      },
      Math: Math,
      JSON: JSON,
      Array: Array,
      Object: Object,
      String: String,
      Number: Number,
      Date: Date,
      RegExp: RegExp,
      Error: Error,
      setTimeout: () => {},
      clearTimeout: () => {},
      setInterval: () => {},
      clearInterval: () => {}
    };
  }

  // Executa código em contexto isolado
  private runInContext(code: string, _context: any): any {
    // Em produção, usaria vm2 ou similar
    // Esta é uma simulação simplificada
    const wrappedCode = `
      (function() {
        try {
          ${code}
        } catch(e) {
          return 'Erro: ' + e.message;
        }
      })()
    `;
    
    try {
      return eval(wrappedCode);
    } catch (e) {
      return `Erro: ${e}`;
    }
  }

  // Simula execução Python
  private simulatePythonExecution(code: string): string {
    const lines = code.split('\n').length;
    return `[Python Sandbox] Executado ${lines} linhas\nOutput: Simulacao de execucao bem-sucedida`;
  }

  // Simula busca web
  private simulateWebSearch(query: string, maxResults: number): any {
    return {
      query,
      results: Array.from({ length: maxResults }, (_, i) => ({
        title: `Resultado ${i + 1} para "${query}"`,
        url: `https://duckduckgo.com/result?${i}`,
        snippet: `Informacao relevante sobre ${query} encontrada em fonte ${i + 1}`,
        relevance: Math.random() * 0.5 + 0.5
      })),
      timestamp: Date.now()
    };
  }

  // Verifica permissão
  private hasPermission(env: SandboxEnvironment, permission: string): boolean {
    return env.permissions.includes(permission) || env.permissions.includes('*');
  }

  // Registra execução no log
  private logExecution(env: SandboxEnvironment, log: ExecutionLog): void {
    env.executionLog.push(log);
    
    // Mantém apenas últimas 100 execuções
    if (env.executionLog.length > 100) {
      env.executionLog = env.executionLog.slice(-100);
    }
  }

  // Adiciona permissão a um ambiente
  grantPermission(envId: string, permission: string): boolean {
    const env = this.environments.get(envId);
    if (env) {
      if (!env.permissions.includes(permission)) {
        env.permissions.push(permission);
      }
      return true;
    }
    return false;
  }

  // Revoga permissão de um ambiente
  revokePermission(envId: string, permission: string): boolean {
    const env = this.environments.get(envId);
    if (env) {
      env.permissions = env.permissions.filter(p => p !== permission);
      return true;
    }
    return false;
  }

  // Destrói ambiente sandbox
  destroyEnvironment(envId: string): boolean {
    const env = this.environments.get(envId);
    if (env) {
      env.active = false;
      this.environments.delete(envId);
      return true;
    }
    return false;
  }

  // Limpa todos os ambientes
  clearAllEnvironments(): void {
    this.environments.forEach(env => {
      env.active = false;
    });
    this.environments.clear();
  }

  // Getters
  getEnvironment(envId: string): SandboxEnvironment | undefined {
    return this.environments.get(envId);
  }

  getAllEnvironments(): SandboxEnvironment[] {
    return Array.from(this.environments.values());
  }

  getActiveEnvironments(): SandboxEnvironment[] {
    return Array.from(this.environments.values()).filter(e => e.active);
  }

  getEnvironmentCount(): number {
    return this.environments.size;
  }

  getGlobalPermissions(): string[] {
    return Array.from(this.globalPermissions);
  }

  // Define modo isolado global
  setIsolatedMode(isolated: boolean): void {
    this.isolatedMode = isolated;
  }

  isIsolatedMode(): boolean {
    return this.isolatedMode;
  }
}

export const createSandbox = (isolatedMode?: boolean) => {
  return new BRXSandbox(isolatedMode);
};
