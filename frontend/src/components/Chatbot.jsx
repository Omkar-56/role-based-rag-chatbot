import { useState } from "react";
import { Input, Button, MessageList } from "react-chat-elements";
import { api } from "../services/api";

function formatAnswerToPoints(answer) {
  if (!answer) return "";

  // Normalize separators
  let text = answer
    .replace(/\n+/g, " ")
    .replace(/•/g, "-")
    .replace(/–/g, "-")
    .replace(/—/g, "-");

  // Split on hyphens OR sentence endings
  let parts = text
    .split(/-|\.\s+/)
    .map((p) => p.trim())
    .filter((p) => p.length > 5);

  // Remove intro sentence if present
  if (parts.length > 1) {
    parts = parts.filter(
      (p) =>
        !p.toLowerCase().includes("according to") &&
        !p.toLowerCase().includes("based on")
    );
  }

  return parts.map((p) => `• ${p}`).join("\n");
}



function formatSources(sources = []) {
  if (!sources.length) return "";

  const unique = new Map();

  sources.forEach((s) => {
    const key = `${s.source}-${s.role}`;
    if (!unique.has(key)) {
      unique.set(key, s);
    }
  });

  return (
    "\n\nSources:\n" +
    [...unique.values()]
      .map((s) => `• ${s.source} (${s.role})`)
      .join("\n")
  );
}

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!text.trim()) return;

    const userMsg = {
      position: "right",
      type: "text",
      text,
      title: "You",
    };

    setMessages((prev) => [...prev, userMsg]);
    setText("");
    setLoading(true);

    try {
      const res = await api.post("/chat", {
        query: text,
      });

      const formattedAnswer = formatAnswerToPoints(res.data.answer);
      const sourcesText = formatSources(res.data.sources);

      const botMsg = {
        position: "left",
        type: "text",
        title: "AI",
        text: formattedAnswer + "\n\n" + sourcesText,
      };


      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      alert("Chat failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <MessageList
        className="message-list"
        lockable
        toBottomHeight={"100%"}
        dataSource={messages}
        style={{
          height: "60vh",
          background: "#020617",
        }}
      />

      <div style={{ display: "flex", gap: 10, marginTop: 10 }}>
        <Input
          placeholder="Ask something..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
        />
        <Button
          text={loading ? "..." : "Send"}
          onClick={sendMessage}
        />
      </div>
    </div>
  );
}
