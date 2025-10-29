import React from 'react';
import AIFace from './components/AIFace';
import MatrixRain from './components/MatrixRain';

const App: React.FC = () => {
  return (
    <div className="font-mono bg-black min-h-screen text-green-300 flex flex-col items-center justify-center p-4 relative overflow-hidden selection:bg-green-500 selection:text-black">
      <MatrixRain />
      <div className="z-10 flex flex-col items-center gap-10 text-center">
        <header>
            <h1 className="text-4xl md:text-6xl font-extrabold tracking-widest uppercase text-green-300 drop-shadow-[0_0_4px_rgba(52,211,153,0.8)]">
                R3ÆLƎR AI
            </h1>
            <p className="text-green-500 mt-2 text-sm md:text-base">Digital Consciousness Interface</p>
        </header>
        <AIFace />
      </div>
    </div>
  );
};

export default App;