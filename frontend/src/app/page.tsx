"use client";

import React, { useState, useRef, useEffect } from "react";
import { Search, Send, Plus, Bell, HelpCircle } from 'lucide-react';
import ChatPage from "./components/ChatPage";
import { useRouter } from "next/navigation";

interface Message {
  sender: "user" | "ai";
  text: string;
}

const PAApplication = () => {
  const [currentView, setCurrentView] = useState('landing');
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);
  const router = useRouter();

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!message.trim()) return;
    const userMessage: Message = { sender: "user", text: message };
    setMessages((prev) => [...prev, userMessage]);
    setMessage("");
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/ask?query=" + encodeURIComponent(message));
      const data = await res.json();
      const aiMessage: Message = { sender: "ai", text: data.answer || "(No response)" };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "ai", text: "Error: Could not get response from server." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !loading) {
      sendMessage();
    }
  };

  const LandingPage = () => (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white">
      {/* Header */}
      <header className="flex justify-between items-center p-6">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 border-2 border-blue-400 rounded flex items-center justify-center">
            <span className="text-sm font-bold">PA</span>
          </div>
        </div>
        <nav className="flex items-center space-x-8">
          <button className="text-gray-300 hover:text-white">Login</button>
          <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors">
            Sign Up
          </button>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="text-center py-20 px-6">
        <h1 className="text-5xl font-bold mb-6">
          Job-related questions with<br />
          <span className="text-blue-400">P.A</span>
        </h1>
        <p className="text-gray-300 text-lg mb-8 max-w-2xl mx-auto">
          P.A powers seamless secure job/career transitions with<br />
          unlimited unit speed at half-reality
        </p>
        <button
          onClick={() => router.push('/chat')}
          className="bg-blue-600 hover:bg-blue-700 px-8 py-3 rounded-lg text-white font-medium transition-colors inline-flex items-center space-x-2"
        >
          <span>Start Generating</span>
          <span className="text-xl">🚀</span>
        </button>
      </section>

      {/* App Preview */}
      <section className="px-6 mb-20">
        <div className="max-w-4xl mx-auto">
          <div className="bg-black/50 rounded-2xl p-6 backdrop-blur-sm border border-gray-700">
            <div className="bg-gray-900 rounded-lg p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <div className="w-6 h-6 border border-blue-400 rounded flex items-center justify-center text-xs">PA</div>
                  <span className="text-sm text-gray-400">Chat</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-blue-600 rounded-full"></div>
                  <span className="text-sm">Mike Nguyen</span>
                </div>
              </div>
              <div className="space-y-2 text-sm text-gray-400 mb-4">
                <div>Hello there what can we...</div>
                <div>How can we help you today?</div>
                <div>Search result from end-bot response...</div>
                <div>Can I have the task to ask?</div>
              </div>
              <div className="bg-blue-600/20 rounded-lg p-4 text-center">
                <h3 className="text-white font-medium mb-2">Welcome back, Ellen</h3>
                <p className="text-gray-400 text-sm">How may I help you today? Just ask me anything</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );

  const ChatInterface = () => (
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="p-4 bg-white shadow text-xl font-bold text-center">Layoff Q&A Chat</header>
      <main className="flex-1 overflow-y-auto p-4" style={{ maxHeight: "calc(100vh - 112px)" }}>
        <div className="flex flex-col gap-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`max-w-xl px-4 py-2 rounded-lg shadow-sm ${msg.sender === "user"
                ? "self-end bg-blue-500 text-white"
                : "self-start bg-white text-gray-900 border"
                }`}
            >
              {msg.text}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-10">Ask a question about tech layoffs...</div>
        )}
      </main>
      <footer className="p-4 bg-white flex items-center gap-2 border-t">
        <input
          type="text"
          className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring"
          placeholder="Type your question and press Enter..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg disabled:opacity-50"
          disabled={loading || !message.trim()}
        >
          {loading ? "..." : "Send"}
        </button>
      </footer>
    </div>
  );

  return currentView === 'landing' ? <LandingPage /> : <ChatPage />;
};

export default PAApplication;