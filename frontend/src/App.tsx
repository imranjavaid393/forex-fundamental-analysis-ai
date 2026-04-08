import React, { useState } from 'react';
import Home from './pages/Home';
import History from './pages/History';
import './styles.css';

const App: React.FC = () => {
  const [page, setPage] = useState<'home' | 'history'>('home');

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">📈</span>
            <span className="logo-text">Forex AI</span>
            <span className="logo-sub">Fundamental Analysis</span>
          </div>
          <nav className="nav">
            <button
              className={`nav-btn ${page === 'home' ? 'active' : ''}`}
              onClick={() => setPage('home')}
            >
              Dashboard
            </button>
            <button
              className={`nav-btn ${page === 'history' ? 'active' : ''}`}
              onClick={() => setPage('history')}
            >
              History
            </button>
          </nav>
        </div>
      </header>
      <main className="app-main">
        {page === 'home' ? <Home /> : <History />}
      </main>
      <footer className="app-footer">
        <p>Forex Fundamental Analysis AI • Powered by economic indicators & AI</p>
      </footer>
    </div>
  );
};

export default App;
