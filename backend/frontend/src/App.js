import { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const res = await fetch(`http://127.0.0.1:8000/chat?query=${input}`);
      const data = await res.json();

      const botMessage = { role: "bot", text: data };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error connecting to server" },
      ]);
    }

    setInput("");
    setLoading(false);
  };

  return (
    <div className="app">
      <div className="chat-container">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role === "user" ? "user" : "bot"}>
            {msg.text}
          </div>
        ))}

        {loading && <div className="bot">Typing...</div>}
      </div>

      <div className="input-box">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;