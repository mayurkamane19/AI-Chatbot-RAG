import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pdfFile, setPdfFile] = useState(null);

  const askQuestion = async () => {
    if (!query.trim()) return;

    const userMessage = {
      type: "user",
      text: query,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch(
        `https://ai-chatbot-rag-0goe.onrender.com/chat?query=${encodeURIComponent(
          query
        )}`
      );

      const data = await res.json();

      const botMessage = {
        type: "bot",
        text: data.response,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: "Error connecting to backend",
        },
      ]);
    }

    setLoading(false);
    setQuery("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      askQuestion();
    }
  };

  return (
    <div
      style={{
        background: "#0f172a",
        minHeight: "100vh",
        color: "white",
        padding: "20px",
      }}
    >
      <h1 style={{ textAlign: "center" }}>
        🤖 AI PDF Chatbot
      </h1>

      {/* PDF Upload UI */}
      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        <input
  type="file"
  accept=".pdf"
  onChange={async (e) => {
    const file = e.target.files[0];
    setPdfFile(file);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(
        "https://ai-chatbot-rag-0goe.onrender.com/upload-pdf",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: data.message,
        },
      ]);
    } catch (err) {
      console.error(err);
    }
  }}
/>

        {pdfFile && (
          <p>
            Uploaded: {pdfFile.name}
          </p>
        )}
      </div>

      {/* Chat Area */}
      <div
        style={{
          maxWidth: "900px",
          margin: "auto",
          background: "#1e293b",
          padding: "20px",
          borderRadius: "12px",
          minHeight: "400px",
          overflowY: "auto",
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              display: "flex",
              justifyContent:
                msg.type === "user"
                  ? "flex-end"
                  : "flex-start",
              marginBottom: "12px",
            }}
          >
            <div
              style={{
                background:
                  msg.type === "user"
                    ? "#2563eb"
                    : "#334155",
                padding: "12px",
                borderRadius: "12px",
                maxWidth: "70%",
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div
            style={{
              textAlign: "left",
              color: "#94a3b8",
            }}
          >
            🤖 Thinking...
          </div>
        )}
      </div>

      {/* Input Area */}
      <div
        style={{
          maxWidth: "900px",
          margin: "20px auto",
          display: "flex",
          gap: "10px",
        }}
      >
        <input
          type="text"
          value={query}
          onChange={(e) =>
            setQuery(e.target.value)
          }
          onKeyDown={handleKeyPress}
          placeholder="Ask a question..."
          style={{
            flex: 1,
            padding: "14px",
            borderRadius: "10px",
            border: "none",
            fontSize: "16px",
          }}
        />

        <button
          onClick={askQuestion}
          style={{
            padding: "14px 25px",
            background: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "10px",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;