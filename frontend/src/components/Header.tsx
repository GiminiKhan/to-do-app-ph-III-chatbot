'use client';

import Link from 'next/link';
import { authService } from '../services/auth-client';
import { useEffect, useState } from 'react';

export default function Header() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    setIsAuthenticated(authService.isAuthenticated());
  }, []);

  return (
    <header className="bg-white shadow-sm p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">Todo App</h1>
        <nav>
          {isAuthenticated ? (
            <Link href="/chat" className="flex items-center gap-2 text-blue-600 hover:text-blue-800">
              {/* Chat Icon (SVG) */}
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 8.511c.584.288 1 .882 1 1.589v5.25c0 1.105-.895 2-2 2h-1.5v-3.75l-4.5 4.5 4.5 4.5V20.5a2 2 0 002-2V10.1c0-.707.416-1.301 1-1.589zM3 10.1v5.25c0 1.105.895 2 2h3l4.5 4.5 4.5-4.5h3c1.105 0 2-.895 2-2V10.1c0-.707-.416-1.301-1-1.589z" />
              </svg>
              Chatbot
            </Link>
          ) : (
            <span className="text-gray-500">Chatbot (Login Required)</span>
          )}
        </nav>
      </div>
    </header>
  );
}
