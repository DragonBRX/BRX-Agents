import { useEffect, useState } from 'react';
import { BRXDashboard } from './sections/BRXDashboard';
import { createBRXEngine, BRXEngine } from './brx-engine';
import { Loader2 } from 'lucide-react';

function App() {
  const [engine, setEngine] = useState<BRXEngine | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Inicializa o BRX-ENGINE
    try {
      const brxEngine = createBRXEngine();
      
      // Inicia automaticamente
      brxEngine.start();
      
      setEngine(brxEngine);
      setLoading(false);
      
      console.log('[App] BRX-ENGINE inicializado com sucesso');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao inicializar BRX-ENGINE');
      setLoading(false);
    }

    // Cleanup ao desmontar
    return () => {
      if (engine) {
        engine.stop();
      }
    };
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-cyan-400 animate-spin mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-slate-200">Inicializando BRX-ENGINE...</h2>
          <p className="text-slate-500 mt-2">Carregando sistema de 8 mentes e 45+ ferramentas</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-red-400 text-2xl">!</span>
          </div>
          <h2 className="text-xl font-semibold text-red-400">Erro de Inicialização</h2>
          <p className="text-slate-500 mt-2">{error}</p>
        </div>
      </div>
    );
  }

  if (!engine) {
    return null;
  }

  return <BRXDashboard engine={engine} />;
}

export default App;
