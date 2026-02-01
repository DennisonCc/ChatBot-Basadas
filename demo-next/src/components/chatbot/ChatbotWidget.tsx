'use client';
import React, { useState, useEffect, useRef } from 'react';
import './ChatbotWidget.css';

interface Message {
    text: string;
    isBot: boolean;
}

interface ChatbotWidgetProps {
    currentScreen?: string;
    apiUrl?: string;
}

const ChatbotWidget: React.FC<ChatbotWidgetProps> = ({
    currentScreen = "Principal",
    apiUrl = "http://localhost:7842"
}) => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [messages, setMessages] = useState<Message[]>([
        {
            text: `Hola, soy tu Consultor de RRHH. Analizando el contexto, veo que estás en la sección de **${currentScreen}**. ¿Cómo puedo optimizar tu gestión hoy?`,
            isBot: true
        }
    ]);
    const [inputValue, setInputValue] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = (): void => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSend = async (): Promise<void> => {
        if (!inputValue.trim()) return;

        const userMessage: Message = { text: inputValue, isBot: false };
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const response = await fetch(`${apiUrl}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: inputValue,
                    session_id: "premium-session-ts",
                    current_screen: currentScreen
                }),
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            setMessages(prev => [...prev, { text: data.response, isBot: true }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                text: "Parece que hay una interrupción con el servidor inteligente. Por favor, verifica la conexión.",
                isBot: true
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={`premium-chatbot ${isOpen ? 'is-open' : ''}`}>
            <button className="launcher-btn" onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? (
                    <span className="close-icon">&times;</span>
                ) : (
                    <div className="launcher-content">
                        <span className="pulse-ring"></span>
                        <img src="/logo.png" alt="AI HR" className="launcher-logo" />
                    </div>
                )}
            </button>

            {isOpen && (
                <div className="chat-window">
                    <div className="chat-header">
                        <div className="header-brand">
                            <div className="logo-container">
                                <img src="/logo.png" alt="AI HR" />
                                <span className="status-dot"></span>
                            </div>
                            <div className="header-text">
                                <h3>Nexus AI</h3>
                                <p>Consultor Senior de RRHH</p>
                            </div>
                        </div>
                        <div className="current-context">
                            <span className="context-label">Contexto</span>
                            <span className="context-value">{currentScreen}</span>
                        </div>
                    </div>

                    <div className="chat-body">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message-row ${msg.isBot ? 'bot' : 'user'}`}>
                                {msg.isBot && <img src="/logo.png" className="mini-logo" alt="bot" />}
                                <div className="bubble">
                                    {msg.text.split('\n').map((line, i) => (
                                        <p key={i}>{line}</p>
                                    ))}
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="message-row bot thinking-row">
                                <img src="/logo.png" className="mini-logo animate-pulse" alt="bot" />
                                <div className="bubble typing">
                                    <span></span><span></span><span></span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="chat-footer">
                        <div className="input-wrapper">
                            <input
                                type="text"
                                placeholder="Escribe tu consulta o pide una inferencia..."
                                value={inputValue}
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInputValue(e.target.value)}
                                onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === 'Enter' && handleSend()}
                            />
                            <button className="send-btn" onClick={handleSend} disabled={isLoading}>
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChatbotWidget;
