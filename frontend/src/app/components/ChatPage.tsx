"use client";
import React, { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";

interface Message {
    sender: "user" | "ai";
    text: string;
}

export function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [message, setMessage] = useState("");
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

    return (
        <div className="flex flex-col h-screen bg-gray-100">
            <header className="p-4 bg-white shadow text-xl font-bold text-center flex items-center">
                <button
                    className="mr-4 px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 text-gray-700 text-base"
                    onClick={() => router.push("/")}
                >
                    ← Back
                </button>
                <span className="flex-1 text-center">Layoff Q&A Chat</span>
            </header>
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
                    className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring text-black"
                    placeholder="Type your question and press Enter..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={loading}
                />
                <span className="ml-1 text-xl">✈️</span>
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
} 