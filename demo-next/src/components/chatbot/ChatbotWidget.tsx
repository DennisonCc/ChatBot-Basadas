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

// User Avatar SVG Component
const UserAvatar = () => (
    <svg className="user-avatar" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="userGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{ stopColor: '#6366f1', stopOpacity: 1 }} />
                <stop offset="100%" style={{ stopColor: '#a855f7', stopOpacity: 1 }} />
            </linearGradient>
        </defs>
        <circle cx="16" cy="16" r="16" fill="url(#userGrad)" opacity="0.15" />
        <circle cx="16" cy="12" r="5" fill="url(#userGrad)" />
        <path d="M6 26c0-5.5 4.5-8 10-8s10 2.5 10 8" fill="url(#userGrad)" />
    </svg>
);

// Rich Message Formatter
const formatMessage = (text: string) => {
    const parts = [];
    let currentText = text;
    let key = 0;

    // Split by code blocks first (```code```)
    const codeBlockRegex = /```([\s\S]*?)```/g;
    const segments = currentText.split(codeBlockRegex);

    segments.forEach((segment, index) => {
        if (index % 2 === 1) {
            // This is a code block
            parts.push(
                <pre key={key++} className="code-block">
                    <code>{segment.trim()}</code>
                </pre>
            );
        } else {
            // Regular text - process inline formatting
            const lines = segment.split('\n');
            lines.forEach((line, lineIdx) => {
                if (!line.trim()) {
                    parts.push(<br key={key++} />);
                    return;
                }

                // Check for lists
                if (line.trim().match(/^[-*•]\s/)) {
                    const content = line.replace(/^[-*•]\s/, '');
                    parts.push(
                        <div key={key++} className="list-item">
                            <span className="bullet">•</span>
                            <span>{processInlineFormatting(content)}</span>
                        </div>
                    );
                } else if (line.trim().match(/^\d+\.\s/)) {
                    const match = line.match(/^(\d+)\.\s(.+)/);
                    if (match) {
                        parts.push(
                            <div key={key++} className="list-item numbered">
                                <span className="number">{match[1]}.</span>
                                <span>{processInlineFormatting(match[2])}</span>
                            </div>
                        );
                    }
                } else {
                    // Regular paragraph
                    parts.push(
                        <p key={key++}>{processInlineFormatting(line)}</p>
                    );
                }
            });
        }
    });

    return parts;
};

// Process inline formatting (**bold**, `code`, etc.)
const processInlineFormatting = (text: string) => {
    const parts = [];
    let currentText = text;
    let key = 0;

    // Process **bold**
    const boldRegex = /\*\*([^*]+)\*\*/g;
    const segments = currentText.split(boldRegex);

    segments.forEach((segment, index) => {
        if (index % 2 === 1) {
            parts.push(<strong key={key++} className="highlight">{segment}</strong>);
        } else {
            // Process `inline code`
            const codeSegments = segment.split(/`([^`]+)`/g);
            codeSegments.forEach((codeSeg, codeIdx) => {
                if (codeIdx % 2 === 1) {
                    parts.push(<code key={key++} className="inline-code">{codeSeg}</code>);
                } else if (codeSeg) {
                    parts.push(<span key={key++}>{codeSeg}</span>);
                }
            });
        }
    });

    return parts;
};

const ChatbotWidget: React.FC<ChatbotWidgetProps> = ({
    currentScreen = "Principal",
    apiUrl = "http://localhost:7842"
}) => {
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [messages, setMessages] = useState<Message[]>([
        {
            text: `Hola, soy tu **Consultor de RRHH** especializado en el Sistema de Gestión de Personal. Estás en la sección de **${currentScreen}**. ¿En qué puedo ayudarte?`,
            isBot: true
        }
    ]);
    const [inputValue, setInputValue] = useState<string>('');
    const [showToast, setShowToast] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = (): void => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    // Sugerir corrección de forma conversacional
    const suggestCorrection = (msgIndex: number) => {
        const correctionPrompt = "Parece que la información anterior no es correcta. Por favor, indícame cuál es la información correcta y la guardaré para futuras consultas.";
        setInputValue(correctionPrompt);
    };

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

            // Detect memory update confirmation
            const memoryKeywords = ["guardada", "actualizado", "anotado"];
            if (memoryKeywords.some(keyword => data.response.toLowerCase().includes(keyword))) {
                setShowToast(true);
                setTimeout(() => setShowToast(false), 3000);
            }

        } catch (error) {
            setMessages(prev => [...prev, {
                text: "⚠️ Parece que hay una interrupción con el servidor inteligente. Por favor, verifica la conexión.",
                isBot: true
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={`premium-chatbot ${isOpen ? 'is-open' : ''}`}>
            {/* ... launcher button ... */}
            <button className="launcher-btn" onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? (
                    <span className="close-icon">&times;</span>
                ) : (
                    <div className="launcher-content">
                        <span className="pulse-ring"></span>
                        <img src="/ai-logo.png" alt="Nexus AI" className="launcher-logo" />
                    </div>
                )}
            </button>

            {isOpen && (
                <div className="chat-window">
                    {/* MEMORY TOAST */}
                    {showToast && (
                        <div className="memory-toast">
                            <span className="toast-icon">🧠</span>
                            <span>Memoria Actualizada</span>
                        </div>
                    )}

                    <div className="chat-header">
                        {/* ... header content ... */}
                        <div className="header-brand">
                            <div className="logo-container">
                                <img src="/ai-logo.png" alt="Nexus AI" />
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
                        {/* ... messages ... */}
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message-row ${msg.isBot ? 'bot' : 'user'}`}>
                                {msg.isBot ? (
                                    <img src="/ai-logo.png" className="mini-logo ai-logo" alt="Nexus AI" />
                                ) : (
                                    <UserAvatar />
                                )}
                                <div className="bubble">
                                    {msg.isBot ? formatMessage(msg.text) : <p>{msg.text}</p>}
                                    {msg.isBot && idx > 0 && (
                                        <button
                                            className="feedback-btn"
                                            onClick={() => suggestCorrection(idx)}
                                            title="¿Información incorrecta? Haz clic para corregir"
                                        >
                                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="14" height="14">
                                                <path d="M12 20h9" />
                                                <path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z" />
                                            </svg>
                                        </button>
                                    )}
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="message-row bot thinking-row">
                                <img src="/ai-logo.png" className="mini-logo ai-logo animate-pulse" alt="Nexus AI" />
                                <div className="bubble typing">
                                    <span></span><span></span><span></span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="chat-footer">
                        {/* ... footer content ... */}
                        <div className="input-wrapper">
                            <input
                                type="text"
                                placeholder="Escribe tu consulta sobre el sistema..."
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
