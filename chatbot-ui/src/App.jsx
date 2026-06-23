import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const askQuestion = async () => {
    try {
      const res = await fetch(
        `https://ai-chatbot-rag-0goe.onrender.com/chat?query=${encodeURIComponent(query)}`
      );

      const data = await res.json();

      console.log("API Response:", data);

      setResponse(data.response || "No response received");
    } catch (error) {
      console.error(error);
      setResponse("Error connecting to backend");
    }
  };

  return (
    <div
      style={{
        maxWidth: "700px",
        margin: "50px auto",
        textAlign: "center",
        color: "white",
      }}
    >
      <h1>🤖 AI PDF Chatbot</h1>

      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
        style={{
          width: "100%",
          padding: "12px",
          marginBottom: "10px",
        }}
      />

      <button
        onClick={askQuestion}
        style={{
          padding: "10px 20px",
          cursor: "pointer",
        }}
      >
        Ask
      </button>

      <div
        style={{
          marginTop: "20px",
          padding: "15px",
          border: "1px solid white",
          borderRadius: "10px",
        }}
      >
        <h3>Response:</h3>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;