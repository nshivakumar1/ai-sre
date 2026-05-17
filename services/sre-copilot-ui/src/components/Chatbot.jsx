import React, { useState } from 'react';

export default function Chatbot() {
  const [messages, setMessages] = useState([{ role: 'system', text: 'How can I help you today?' }]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    if (e.key !== 'Enter' || !input.trim()) return;
    const userMessage = input.trim();
    setMessages(prev => [...prev, { role: 'user', text: userMessage }]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8006/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage })
      });
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'system', text: data.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'system', text: 'Error connecting to chatbot API.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            {msg.text}
          </div>
        ))}
        {loading && <div className="message system loading">...</div>}
      </div>
      <input 
        type="text" 
        placeholder="Ask about infrastructure or incidents..." 
        className="chat-input"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={sendMessage}
        disabled={loading}
      />
    </div>
  );
}
