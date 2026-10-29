import React, { useState, useRef, useEffect } from "react";
import { chatRAG } from "../api/client";
import "./ChatInterface.css";

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [lastAnswer, setLastAnswer] = useState(null);

  const messagesEndRef = useRef(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim()) return;
    
    const userMessage = {
      role: 'user',
      content: inputText.trim()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      // Call API with question and last_answer (not history!)
      console.log('Sending:', {
        question: userMessage.content,
        last_answer: lastAnswer
      });
      
      const answer = await chatRAG(userMessage.content, lastAnswer);
      
      console.log('Received:', answer);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: answer
      }]);
      setLastAnswer(answer);
      console.log('Saved last answer:', answer.substring(0, 50) + '...');
      
    } catch (err) {
      console.error("Chat error:", err);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
  setMessages([]);
  setLastAnswer(null); 
  console.log('Chat cleared');
};
  
  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <h2>💬 Power Plant Assistant</h2>
        <button onClick={handleClearChat} className="clear-btn">
          🆕 New Chat
        </button>
      </div>
      
      {/* Messages */}
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h3>👋 Hello!</h3>
            <p>Ask me anything about power plants</p>
            <div className="examples">
              <p><strong>Try:</strong></p>
              <button onClick={() => setInputText("What types of power plants are there?")}>
                What types of power plants are there?
              </button>
              <button onClick={() => setInputText("How many powerplants are there in Afghanistan ?")}>
                How many powerplants are there in Afghanistan ?
              </button>
            </div>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="avatar">
              {msg.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="bubble">
              {msg.content}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message assistant">
            <div className="avatar">🤖</div>
            <div className="bubble typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input */}
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
          className="message-input"
        />
        <button 
          type="submit" 
          disabled={loading || !inputText.trim()}
          className="send-button"
        >
          {loading ? '⏳' : '⬆️'}
        </button>
      </form>
    </div>
  );
}