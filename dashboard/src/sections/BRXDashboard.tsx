import { useState, useEffect, useCallback } from 'react';
import { 
  Activity, Brain, Cpu, Database, 
  Shield, Zap, Settings, Play, Square,
  TrendingUp, AlertCircle, CheckCircle, 
  Clock, Layers, Network, Terminal
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';

import type { 
  BRXEngine, 
  BRXEngineState,
  AgentParameter,
  MindConfig 
} from '@/brx-engine';

interface DashboardProps {
  engine: BRXEngine;
}

export function BRXDashboard({ engine }: DashboardProps) {
  const [state, setState] = useState<BRXEngineState>(engine.getState());
  const [stats, setStats] = useState(engine.getStats());
  const [isRunning, setIsRunning] = useState(engine.isRunning());
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const interval = setInterval(() => {
      setState(engine.getState());
      setStats(engine.getStats());
      setIsRunning(engine.isRunning());
    }, 1000);

    return () => clearInterval(interval);
  }, [engine]);

  const handleStart = useCallback(() => {
    engine.start();
    setIsRunning(true);
  }, [engine]);

  const handleStop = useCallback(() => {
    engine.stop();
    setIsRunning(false);
  }, [engine]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4">
      <header className="mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="relative">
              <Brain className="w-12 h-12 text-cyan-400" />
              <div className={`absolute -top-1 -right-1 w-3 h-3 rounded-full ${isRunning ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                BRX-ENGINE
              </h1>
              <p className="text-slate-400 text-sm">
                v{stats.version} | Auto-Evolution AI System | {isRunning ? 'RUNNING' : 'STOPPED'}
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <Badge variant="outline" className="border-cyan-500/50 text-cyan-400">
              <Cpu className="w-3 h-3 mr-1" />
              {stats.minds} Minds
            </Badge>
            <Badge variant="outline" className="border-purple-500/50 text-purple-400">
              <Layers className="w-3 h-3 mr-1" />
              {stats.tools} Tools
            </Badge>
            <Badge variant="outline" className="border-green-500/50 text-green-400">
              <Database className="w-3 h-3 mr-1" />
              {stats.memories.total} Memories
            </Badge>
            
            {isRunning ? (
              <Button variant="destructive" size="sm" onClick={handleStop}>
                <Square className="w-4 h-4 mr-1" />
                Stop
              </Button>
            ) : (
              <Button variant="default" size="sm" onClick={handleStart} className="bg-green-600 hover:bg-green-700">
                <Play className="w-4 h-4 mr-1" />
                Start
              </Button>
            )}
          </div>
        </div>
      </header>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="bg-slate-900 border border-slate-800">
          <TabsTrigger value="overview" className="data-[state=active]:bg-cyan-500/20">
            <Activity className="w-4 h-4 mr-1" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="minds" className="data-[state=active]:bg-purple-500/20">
            <Network className="w-4 h-4 mr-1" />
            8 Minds
          </TabsTrigger>
          <TabsTrigger value="parameters" className="data-[state=active]:bg-green-500/20">
            <Settings className="w-4 h-4 mr-1" />
            Parameters
          </TabsTrigger>
          <TabsTrigger value="memory" className="data-[state=active]:bg-yellow-500/20">
            <Database className="w-4 h-4 mr-1" />
            Memory
          </TabsTrigger>
          <TabsTrigger value="tools" className="data-[state=active]:bg-orange-500/20">
            <Terminal className="w-4 h-4 mr-1" />
            Tools
          </TabsTrigger>
          <TabsTrigger value="sandbox" className="data-[state=active]:bg-red-500/20">
            <Shield className="w-4 h-4 mr-1" />
            Sandbox
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <OverviewPanel stats={stats} state={state} />
        </TabsContent>

        <TabsContent value="minds" className="space-y-4">
          <MindsPanel engine={engine} />
        </TabsContent>

        <TabsContent value="parameters" className="space-y-4">
          <ParametersPanel engine={engine} />
        </TabsContent>

        <TabsContent value="memory" className="space-y-4">
          <MemoryPanel engine={engine} />
        </TabsContent>

        <TabsContent value="tools" className="space-y-4">
          <ToolsPanel engine={engine} />
        </TabsContent>

        <TabsContent value="sandbox" className="space-y-4">
          <SandboxPanel engine={engine} />
        </TabsContent>
      </Tabs>
    </div>
  );
}

function OverviewPanel({ stats, state }: { stats: any; state: BRXEngineState }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card className="bg-slate-900 border-slate-800">
        <CardHeader className="pb-2">
          <CardDescription className="text-slate-400">Evolution Cycle</CardDescription>
          <CardTitle className="text-3xl text-cyan-400">{stats.cycle}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center text-sm text-slate-500">
            <Clock className="w-4 h-4 mr-1" />
            Last update: {new Date(state.lastUpdate).toLocaleTimeString()}
          </div>
        </CardContent>
      </Card>

      <Card className="bg-slate-900 border-slate-800">
        <CardHeader className="pb-2">
          <CardDescription className="text-slate-400">Parameters</CardDescription>
          <CardTitle className="text-3xl text-green-400">{stats.parameters}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2 text-sm">
            <span className="text-green-500">+{stats.positiveParams}</span>
            <span className="text-slate-600">|</span>
            <span className="text-red-500">-{stats.negativeParams}</span>
          </div>
        </CardContent>
      </Card>

      <Card className="bg-slate-900 border-slate-800">
        <CardHeader className="pb-2">
          <CardDescription className="text-slate-400">Efficiency</CardDescription>
          <CardTitle className="text-3xl text-purple-400">
            {(stats.performance.efficiency * 100).toFixed(1)}%
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Progress value={stats.performance.efficiency * 100} className="h-2" />
        </CardContent>
      </Card>

      <Card className="bg-slate-900 border-slate-800">
        <CardHeader className="pb-2">
          <CardDescription className="text-slate-400">Success Rate</CardDescription>
          <CardTitle className="text-3xl text-yellow-400">
            {(stats.performance.successRate * 100).toFixed(1)}%
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Progress value={stats.performance.successRate * 100} className="h-2" />
        </CardContent>
      </Card>

      <Card className="col-span-full bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-cyan-400" />
            Performance Metrics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricItem label="Avg Response Time" value={`${stats.performance.avgResponseTime.toFixed(0)}ms`} icon={Clock} />
            <MetricItem label="Parameter Count" value={stats.performance.parameterCount} icon={Settings} />
            <MetricItem label="Memory Usage" value={stats.performance.memoryUsage} icon={Database} />
            <MetricItem label="Cycle Speed" value={`${(stats.performance.cycleSpeed / 1000).toFixed(0)}s`} icon={Zap} />
          </div>
        </CardContent>
      </Card>

      <Card className="col-span-full bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Activity className="w-5 h-5 text-green-400" />
            System Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <StatusItem label="8 Minds System" status="active" />
            <StatusItem label="Evolution Engine" status="active" />
            <StatusItem label="Toolkit (45+)" status="active" />
            <StatusItem label="Sandbox" status="active" />
            <StatusItem label="Memory System" status="active" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function MindsPanel({ engine }: { engine: BRXEngine }) {
  const minds = engine.getMinds().getActiveMinds();
  const history = engine.getMinds().getDebateHistory();

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Network className="w-5 h-5 text-purple-400" />
            8 Minds Configuration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 gap-3">
            {minds.map((mind, index) => (
              <MindCard key={mind.name} mind={mind} index={index} />
            ))}
          </div>
        </CardContent>
      </Card>

      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            Circular Debate History
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[500px]">
            <div className="space-y-2">
              {history.length === 0 ? (
                <p className="text-slate-500 text-center py-8">No debates yet</p>
              ) : (
                history.map((round, i) => (
                  <div key={i} className="p-3 bg-slate-800/50 rounded-lg border border-slate-700">
                    <div className="flex items-center justify-between mb-2">
                      <Badge variant="outline" className="text-xs">Round {round.round + 1}</Badge>
                      <span className="text-xs text-slate-500">{round.mindName}</span>
                    </div>
                    <p className="text-sm text-slate-300">{round.output}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <Badge variant="secondary" className="text-xs">{(round.confidence * 100).toFixed(0)}% confidence</Badge>
                      <span className="text-xs text-slate-500">{round.parameters.length} params</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}

function MindCard({ mind, index }: { mind: MindConfig; index: number }) {
  const colors = [
    'border-blue-500/50 text-blue-400',
    'border-green-500/50 text-green-400',
    'border-purple-500/50 text-purple-400',
    'border-red-500/50 text-red-400',
    'border-yellow-500/50 text-yellow-400',
    'border-cyan-500/50 text-cyan-400',
    'border-orange-500/50 text-orange-400',
    'border-pink-500/50 text-pink-400'
  ];

  return (
    <div className={`p-4 rounded-lg border ${colors[index]} bg-slate-800/30`}>
      <div className="flex items-center justify-between">
        <div>
          <h4 className="font-semibold">{mind.name}</h4>
          <p className="text-xs text-slate-400">{mind.specialty}</p>
        </div>
        <Badge variant="outline" className="text-xs">Weight: {mind.weight}</Badge>
      </div>
      <p className="text-sm text-slate-500 mt-2">{mind.objective}</p>
    </div>
  );
}

function ParametersPanel({ engine }: { engine: BRXEngine }) {
  const params = engine.getEvolution().getParameters();
  const positive = engine.getEvolution().getPositiveParameters();
  const negative = engine.getEvolution().getNegativeParameters();

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <Card className="lg:col-span-2 bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Settings className="w-5 h-5 text-green-400" />
            All Parameters ({params.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[500px]">
            <div className="space-y-2">
              {params.map(param => (
                <ParameterRow key={param.id} param={param} />
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      <div className="space-y-4">
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-lg">Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-green-400">Positive</span>
                  <span>{positive.length}</span>
                </div>
                <Progress value={(positive.length / params.length) * 100} className="h-2 bg-green-500/20" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-red-400">Negative</span>
                  <span>{negative.length}</span>
                </div>
                <Progress value={(negative.length / params.length) * 100} className="h-2 bg-red-500/20" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-lg">Evolution History</CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-[300px]">
              <div className="space-y-2">
                {engine.getEvolution().getEvolutionHistory().slice(-10).map(cycle => (
                  <div key={cycle.cycle} className="p-2 bg-slate-800 rounded text-sm">
                    <div className="flex justify-between">
                      <span className="text-cyan-400">Cycle {cycle.cycle}</span>
                      <span className="text-slate-500">{new Date(cycle.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <div className="flex gap-2 mt-1 text-xs">
                      <span className="text-green-500">+{cycle.improvements.length}</span>
                      <span className="text-red-500">-{cycle.regressions.length}</span>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function ParameterRow({ param }: { param: AgentParameter }) {
  const typeColors = {
    positive: 'border-green-500/30 bg-green-500/10',
    negative: 'border-red-500/30 bg-red-500/10',
    neutral: 'border-slate-500/30 bg-slate-500/10'
  };

  return (
    <div className={`p-3 rounded-lg border ${typeColors[param.type]} flex items-center justify-between`}>
      <div>
        <div className="flex items-center gap-2">
          <span className="font-medium">{param.name}</span>
          <Badge variant="outline" className="text-xs">{param.type}</Badge>
        </div>
        <p className="text-xs text-slate-500">{param.context}</p>
      </div>
      <div className="text-right">
        <div className="font-mono text-sm">{typeof param.value === 'number' ? param.value.toFixed(4) : param.value}</div>
        <div className="text-xs text-slate-500">{(param.confidence * 100).toFixed(0)}% conf</div>
      </div>
    </div>
  );
}

function MemoryPanel({ engine }: { engine: BRXEngine }) {
  const stats = engine.getMemory().getStats();
  const memories = engine.getMemory().getAllMemories();

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Database className="w-5 h-5 text-yellow-400" />
            Memory Tiers
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-cyan-400">Short Term</span>
                <span>{stats.short}</span>
              </div>
              <Progress value={(stats.short / 100) * 100} className="h-2" />
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-purple-400">Medium Term</span>
                <span>{stats.medium}</span>
              </div>
              <Progress value={(stats.medium / 500) * 100} className="h-2" />
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-green-400">Long Term</span>
                <span>{stats.long}</span>
              </div>
              <Progress value={(stats.long / 10000) * 100} className="h-2" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="lg:col-span-2 bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-lg">Recent Memories</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[500px]">
            <div className="space-y-2">
              {memories.slice(-50).reverse().map(memory => (
                <MemoryRow key={memory.id} memory={memory} />
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}

function MemoryRow({ memory }: { memory: any }) {
  const typeColors = {
    short: 'border-cyan-500/30',
    medium: 'border-purple-500/30',
    long: 'border-green-500/30'
  };

  return (
    <div className={`p-3 rounded-lg border ${typeColors[memory.type as keyof typeof typeColors]} bg-slate-800/30`}>
      <div className="flex items-center justify-between mb-1">
        <Badge variant="outline" className="text-xs">{memory.type}</Badge>
        <span className="text-xs text-slate-500">{new Date(memory.timestamp).toLocaleTimeString()}</span>
      </div>
      <p className="text-sm text-slate-300">{memory.content}</p>
      <div className="flex items-center gap-3 mt-2 text-xs text-slate-500">
        <span>Context: {memory.context}</span>
        <span>Access: {memory.accessCount}</span>
        <span>Importance: {(memory.importance * 100).toFixed(0)}%</span>
      </div>
    </div>
  );
}

function ToolsPanel({ engine }: { engine: BRXEngine }) {
  const tools = engine.getToolkit().getTools();
  const categories = ['execution', 'search', 'analysis', 'creation', 'system'];

  return (
    <Card className="bg-slate-900 border-slate-800">
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <Terminal className="w-5 h-5 text-orange-400" />
          Available Tools ({tools.length})
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {categories.map(category => {
            const categoryTools = tools.filter(t => t.category === category);
            return (
              <div key={category}>
                <h4 className="text-sm font-semibold text-slate-400 uppercase mb-2">{category}</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                  {categoryTools.map(tool => (
                    <div key={tool.name} className="p-3 rounded-lg border border-slate-700 bg-slate-800/30">
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-sm">{tool.name}</span>
                        <Badge 
                          variant="outline" 
                          className={`text-xs ${
                            tool.riskLevel === 'high' ? 'border-red-500/50 text-red-400' :
                            tool.riskLevel === 'medium' ? 'border-yellow-500/50 text-yellow-400' :
                            'border-green-500/50 text-green-400'
                          }`}
                        >
                          {tool.riskLevel}
                        </Badge>
                      </div>
                      <p className="text-xs text-slate-500 mt-1">{tool.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

function SandboxPanel({ engine }: { engine: BRXEngine }) {
  const sandboxes = engine.getSandbox().getAllEnvironments();

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Shield className="w-5 h-5 text-red-400" />
            Sandbox Environments
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {sandboxes.map(env => (
              <div key={env.id} className="p-4 rounded-lg border border-slate-700 bg-slate-800/30">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${env.active ? 'bg-green-400' : 'bg-red-400'}`} />
                    <span className="font-medium">{env.id}</span>
                  </div>
                  <Badge variant="outline" className="text-xs">{env.permissions.length} permissions</Badge>
                </div>
                <div className="flex items-center gap-2 mt-2 text-xs text-slate-500">
                  <span>Isolated: {env.isolated ? 'Yes' : 'No'}</span>
                  <span>|</span>
                  <span>Executions: {env.executionLog.length}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle className="text-lg">Global Permissions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {engine.getSandbox().getGlobalPermissions().map(perm => (
              <Badge key={perm} variant="secondary" className="text-xs">{perm}</Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function MetricItem({ label, value, icon: Icon }: { label: string; value: string | number; icon: any }) {
  return (
    <div className="flex items-center gap-3 p-3 rounded-lg bg-slate-800/50">
      <Icon className="w-5 h-5 text-slate-400" />
      <div>
        <p className="text-xs text-slate-500">{label}</p>
        <p className="font-semibold">{value}</p>
      </div>
    </div>
  );
}

function StatusItem({ label, status }: { label: string; status: 'active' | 'inactive' }) {
  return (
    <div className="flex items-center gap-2">
      {status === 'active' ? (
        <CheckCircle className="w-4 h-4 text-green-400" />
      ) : (
        <AlertCircle className="w-4 h-4 text-red-400" />
      )}
      <span className="text-sm text-slate-300">{label}</span>
    </div>
  );
}
