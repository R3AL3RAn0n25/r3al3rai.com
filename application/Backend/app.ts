import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import MatrixRain from './components/MatrixRain';
import AIFace from './components/AIFace';
import Background from './components/Background';
import axios from 'axios';

type AIState = 'idle' | 'thinking' | 'speaking';

interface ChatMessage {
  sender: string;
  text: string;
}

const API_BASE_URL = '/api';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showRegister, setShowRegister] = useState(false);
  const [aiState, setAIState] = useState<AIState>('idle');
  const [chatLog, setChatLog] = useState<ChatMessage[]>([]);
  const [isDebriefOpen, setIsDebriefOpen] = useState(false);
  const [debriefContent, setDebriefContent] = useState('');
  const [token, setToken] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleLogin = async (username: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, { username, password });
      if (response.data.success) {
        setToken(response.data.token);
        setIsAuthenticated(true);
        setError(null);
        setChatLog([...chatLog, { sender: 'ai', text: 'Access granted. Welcome to R3AL3R AI.' }]);
        navigate('/dashboard');
      } else {
        setError(response.data.error || 'Invalid credentials');
      }
    } catch (err: any) {
      setError(err.message || 'Invalid credentials');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (username: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, { username, password });
      if (response.data.success) {
        setError(null);
        setShowRegister(false);
        handleLogin(username, password);
      } else {
        setError(response.data.error || 'Registration failed');
      }
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setToken(null);
    setChatLog([]);
    setError(null);
    setShowRegister(false);
    navigate('/');
  };

  const handleFaceClick = () => {
    setAIState(aiState === 'idle' ? 'thinking' : 'idle');
  };

  const callGemini = async (systemPrompt: string, userQuery: string, retries = 3, delay = 1000): Promise<string> => {
    for (let i = 0; i < retries; i++) {
      try {
        const response = await axios.post(
          `${API_BASE_URL}/thebrain`,
          { userInput: userQuery, user_id: 'testuser', conversation_history: chatLog },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        return response.data.response;
      } catch (error) {
        console.error(`R3AL3R AI call attempt ${i + 1} failed:`, error);
        if (i < retries - 1) {
          await new Promise(res => setTimeout(res, delay * Math.pow(2, i)));
        }
      }
    }
    throw new Error('Max retries reached');
  };

  const handleGenerateDebrief = async () => {
    setIsDebriefOpen(true);
    try {
      const formattedLog = chatLog
        .filter(msg => msg.sender === 'user' || msg.sender === 'ai')
        .map(msg => `${msg.sender.toUpperCase()}: ${msg.text}`)
        .join('\n');
      if (formattedLog.length < 10) {
        setDebriefContent('Not enough conversation data to generate a debrief.');
        return;
      }
      const debrief = await callGemini('Generate a debrief based on this conversation log:', formattedLog);
      setDebriefContent(debrief);
    } catch (error: any) {
      setDebriefContent('Failed to generate debrief.');
    }
  };

  return (
    <div className="w-screen h-screen bg-black text-green-400 font-mono overflow-hidden">
      <MatrixRain />
      <Background />
      <AIFace state={aiState} onClick={handleFaceClick} />
      <main className="relative z-10 w-full h-full flex items-center justify-center p-4">
        {isAuthenticated ? (
          <div className="w-full max-w-4xl flex flex-col gap-4">
            <div className="messages bg-gray-900 p-4 rounded-md max-h-[60vh] overflow-auto">
              {chatLog.map((msg, index) => (
                <div key={index} className={`msg ${msg.sender} flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} mb-2`}>
                  <div className={`bubble p-3 rounded-md ${msg.sender === 'user' ? 'bg-green-800 text-white' : 'bg-gray-800 text-green-400'}`}>
                    {msg.text}
                  </div>
                </div>
              ))}
            </div>
            <div className="composer flex gap-2">
              <input className="flex-1 p-3 bg-gray-800 border border-green-600 rounded-md text-green-400 focus:outline-none focus:ring-2 focus:ring-green-500" placeholder="Type a message..." />
              <button className="p-3 bg-green-800 text-white rounded-md hover:bg-green-700">Send</button>
            </div>
            <div className="absolute top-4 right-4 flex gap-2">
              <button onClick={handleGenerateDebrief} className="bg-green-800 text-white p-2 rounded-md hover:bg-green-700 z-20">
                ✨ Generate Mission Debrief
              </button>
              <button onClick={handleLogout} className="bg-red-800 text-white p-2 rounded-md hover:bg-red-700 z-20">
                Logout
              </button>
            </div>
          </div>
        ) : showRegister ? (
          <div className="w-full max-w-md p-8 bg-black bg-opacity-75 border-2 border-green-500 rounded-lg shadow-[0_0_25px_rgba(0,255,0,0.3)] z-20">
            <h1 className="text-4xl text-center mb-4 text-green-400 font-bold" style={{ textShadow: '0 0 10px #0f0' }}>Register</h1>
            <form onSubmit={(e) => {
              e.preventDefault();
              const username = (e.currentTarget.elements.namedItem('username') as HTMLInputElement).value;
              const password = (e.currentTarget.elements.namedItem('password') as HTMLInputElement).value;
              handleRegister(username, password);
            }} className="space-y-6">
              <input type="text" name="username" placeholder="Username" className="w-full p-3 bg-gray-800 border border-green-600 rounded-md text-green-400" disabled={isLoading} />
              <input type="password" name="password" placeholder="Password" className="w-full p-3 bg-gray-800 border border-green-600 rounded-md text-green-400" disabled={isLoading} />
              <button type="submit" disabled={isLoading} className="w-full p-3 bg-green-800 text-white rounded-md hover:bg-green-700">
                {isLoading ? 'Registering...' : 'Register'}
              </button>
            </form>
            {error && <div className="mt-4 p-3 bg-red-900 text-red-300 text-center">{error}</div>}
          </div>
        ) : (
          <div className="w-full max-w-md p-8 bg-black bg-opacity-75 border-2 border-green-500 rounded-lg shadow-[0_0_25px_rgba(0,255,0,0.3)] z-20">
            <h1 className="text-4xl text-center mb-4 text-green-400 font-bold" style={{ textShadow: '0 0 10px #0f0' }}>R3ÆLƎR AI</h1>
            <h2 className="text-xl text-center mb-8 text-green-400">System Access Required</h2>
            <form onSubmit={(e) => {
              e.preventDefault();
              const username = (e.currentTarget.elements.namedItem('username') as HTMLInputElement).value;
              const password = (e.currentTarget.elements.namedItem('password') as HTMLInputElement).value;
              handleLogin(username, password);
            }} className="space-y-6">
              <div>
                <input
                  type="text"
                  name="username"
                  placeholder="Username"
                  className="w-full p-3 bg-gray-800 border border-green-600 rounded-md text-green-400 focus:outline-none focus:ring-2 focus:ring-green-500"
                  disabled={isLoading}
                />
              </div>
              <div>
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  className="w-full p-3 bg-gray-800 border border-green-600 rounded-md text-green-400 focus:outline-none focus:ring-2 focus:ring-green-500"
                  disabled={isLoading}
                />
              </div>
              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex items-center justify-center gap-2 p-3 bg-green-800 font-bold rounded-md hover:bg-green-700 text-white disabled:bg-gray-700 disabled:cursor-not-allowed transition-all"
              >
                {isLoading ? 'Authenticating...' : 'Engage'} <span>🔒</span>
              </button>
            </form>
            {error && (
              <div className="mt-4 p-3 bg-red-900 border border-red-500 rounded-md text-red-300 text-center">
                <p>// ACCESS DENIED: {error}</p>
              </div>
            )}
            <div className="mt-6 text-center">
              <p className="text-gray-400">
                New user?{' '}
                <button onClick={() => setShowRegister(true)} className="text-green-400 hover:underline font-bold">
                  Register
                </button>
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

