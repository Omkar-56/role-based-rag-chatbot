import { useState } from "react";
import { api } from "../services/api";

function formatAnswerToPoints(answer) {
  if (!answer) return [];

  let text = answer
    .replace(/\n+/g, " ")
    .replace(/•|–|—/g, "-");

  let parts = text
    .split(/-|\.\s+/)
    .map((p) => p.trim())
    .filter((p) => p.length > 5);

  // Remove generic intro lines
  parts = parts.filter(
    (p) =>
      !p.toLowerCase().includes("according to") &&
      !p.toLowerCase().includes("based on")
  );

  return parts;
}

export default function QueryForm() {
  const [query, setQuery] = useState("");
  const [answerPoints, setAnswerPoints] = useState([]);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await api.post("/chat", {
        query,
      });

      setAnswerPoints(formatAnswerToPoints(res.data.answer));
      setSources(res.data.sources || []);
    } catch (err) {
      alert("Failed to fetch answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 900 }}>
      <h3>Ask a Question</h3>

      <div style={{ display: "flex", gap: 10 }}>
        <input
          style={{ flex: 1 }}
          placeholder="Type your question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={ask} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {/* Answer */}
      {answerPoints.length > 0 && (
        <div className="card" style={{ marginTop: 20 }}>
          <h4>Answer</h4>
          <ul>
            {answerPoints.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Sources */}
      {sources.length > 0 && (
        <div className="card">
          <h4>Sources</h4>
          <ul>
            {sources.map((s, i) => (
              <li key={i}>
                {s.source} ({s.role})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
