'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { Sidebar } from '@/components/layouts/sidebar';
import { ProtectedLayout } from '@/components/layouts/protected-layout';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    setMessages([
      {
        id: '1',
        role: 'assistant',
        content: "Hello! I'm your AI assistant. I can help you manage your tasks using natural language.",
        timestamp: new Date(),
      }
    ]);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      const token = localStorage.getItem('access_token');
      // Updated token extraction logic for safety
      if (!token) throw new Error("No token found");
      const tokenPayload = JSON.parse(atob(token.split('.')[1]));
      const userId = tokenPayload.sub;

      const response = await fetch(`http://127.0.0.1:8000/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: currentInput }),
      });

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        // Updated response mapping to match backend
        content: data.response || "I processed your request.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ProtectedLayout>
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <main className="flex-1 md:ml-64 p-6 flex flex-col">
          <div className="bg-white rounded-xl shadow-sm border h-full flex flex-col">
            <div className="border-b p-4">
              <h1 className="text-xl font-bold text-slate-800">AI Task Assistant</h1>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] flex items-start gap-3 rounded-2xl px-4 py-3 ${message.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-slate-800'}`}>
                    {message.role === 'assistant' ? <Bot size={18} className="mt-1" /> : <User size={18} className="mt-1" />}
                    <p className="text-sm">{message.content}</p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
            <form onSubmit={handleSubmit} className="border-t p-4 flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                className="flex-1 border rounded-xl px-4 py-3 text-black outline-none"
                placeholder="Type your message..."
              />
              <button type="submit" className="bg-indigo-600 text-white rounded-xl px-4 py-3">
                <Send size={18} />
              </button>
            </form>
          </div>
        </main>
      </div>
    </ProtectedLayout>
  );
}