import ChatbotWidget from '../components/chatbot/ChatbotWidget';

interface StatItem {
  label: string;
  value: string;
  color: string;
}

export default function Home() {
  const stats: StatItem[] = [
    { label: 'Turnos Activos', value: '42', color: 'indigo' },
    { label: 'Cobertura Hoy', value: '98%', color: 'emerald' },
    { label: 'Incidentes', value: '0', color: 'slate' }
  ];

  return (
    <main className="min-h-screen bg-[#020617] text-slate-200 font-sans selection:bg-indigo-500/30">
      {/* Sidebar Simulation */}
      <div className="fixed left-0 top-0 bottom-0 w-64 bg-[#0f172a] border-r border-white/5 p-6 hidden lg:block">
        <div className="flex items-center gap-3 mb-12">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white">S</div>
          <span className="text-xl font-bold tracking-tight text-white">SmartHR</span>
        </div>

        <nav className="space-y-2">
          {['Dashboard', 'Personal', 'Tiempos Fuera', 'Turnos', 'Asistencia', 'Nómina'].map((item) => (
            <div key={item}
              className={`px-4 py-2 rounded-xl cursor-pointer transition-all ${item === 'Turnos' ? 'bg-indigo-600/10 text-indigo-400 font-medium' : 'hover:bg-white/5 text-slate-400'}`}>
              {item}
            </div>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <div className="lg:pl-64 p-8">
        <header className="flex justify-between items-center mb-12">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Planificación de Turnos</h1>
            <p className="text-slate-400">Control de horarios y coberturas del personal.</p>
          </div>
          <div className="flex gap-4">
            <button className="px-6 py-2.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-all">Reportes</button>
            <button className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-medium transition-all shadow-lg shadow-indigo-600/20">Nuevo Turno</button>
          </div>
        </header>

        {/* Dashboard Grid Mockup */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {stats.map((stat) => (
            <div key={stat.label} className="p-6 rounded-3xl bg-[#0f172a] border border-white/5 hover:border-indigo-500/30 transition-all">
              <p className="text-slate-400 text-sm mb-1">{stat.label}</p>
              <h2 className="text-4xl font-bold text-white">{stat.value}</h2>
            </div>
          ))}
        </div>

        <div className="rounded-3xl bg-[#0f172a] border border-white/5 p-8 min-h-[400px]">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-xl font-semibold text-white">Calendario Semanal</h3>
            <div className="flex gap-2">
              <span className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center cursor-pointer">←</span>
              <span className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center cursor-pointer">→</span>
            </div>
          </div>

          <div className="grid grid-cols-7 gap-4">
            {['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'].map(day => (
              <div key={day} className="h-32 rounded-2xl bg-white/[0.02] border border-white/5 p-4">
                <span className="text-xs text-slate-500 uppercase font-bold">{day}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* The Premium Chatbot Widget (Typed) */}
      <ChatbotWidget currentScreen="Turnos" />
    </main>
  );
}
