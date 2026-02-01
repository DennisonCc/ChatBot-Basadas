import React, { useState, useEffect, useRef } from 'react';
import './ChatbotWidget.css';

/**
 * ChatbotWidget - Componente de soporte inteligente
 * 
 * @param {string} currentScreen - El nombre de la pantalla actual donde se encuentra el usuario.
 * @param {string} apiUrl - (Opcional) URL base de la API del chatbot.
 */
const ChatbotWidget = ({ currentScreen = "Principal", apiUrl = "http://localhost:7842" }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { text: `¡Hola! Soy tu asistente de soporte. Veo que estás en la sección de ${currentScreen}. ¿En qué puedo ayudarte hoy?`, isBot: true }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSend = async () => {
        if (!inputValue.trim()) return;

        const userMessage = { text: inputValue, isBot: false };
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const response = await fetch(`${apiUrl}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: inputValue,
                    session_id: "user-session-react",
                    current_screen: currentScreen
                }),
            });

            const data = await response.json();
            setMessages(prev => [...prev, { text: data.response, isBot: true }]);
        } catch (error) {
            setMessages(prev => [...prev, { text: "Lo siento, tengo problemas para conectarme al servidor de soporte.", isBot: true }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={`chatbot-container ${isOpen ? 'open' : ''}`}>
            {!isOpen && (
                <button className="chatbot-launcher" onClick={() => setIsOpen(true)}>
                    <span className="pulse"></span>
                    💬
                </button>
            )}

            {isOpen && (
                <div className="chatbot-window">
                    <div className="chatbot-header">
                        <div className="header-info">
                            <h3>Soporte Inteligente</h3>
                            <span className="screen-badge">Pantalla: {currentScreen}</span>
                        </div>
                        <button className="close-btn" onClick={() => setIsOpen(false)}>×</button>
                    </div>

                    <div className="chatbot-messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message-bubble ${msg.isBot ? 'bot' : 'user'}`}>
                                {msg.text}
                            </div>
                        ))}
                        {isLoading && <div className="message-bubble bot thinking">Escribiendo...</div>}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="chatbot-input">
                        <input
                            type="text"
                            placeholder="Escribe tu consulta..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        />
                        <button onClick={handleSend} disabled={isLoading}>➤</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChatbotWidget;
