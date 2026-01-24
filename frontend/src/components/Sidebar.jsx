export default function Sidebar({ role, activeTab, setActiveTab }) {
  return (
    <div className="sidebar" style={{ width: 220 }}>
      <h3>🤖 RAG Bot</h3>

      <div
        className="tab"
        onClick={() => setActiveTab("chat")}
      >
        💬 Chat
      </div>

      {role === "c_level" && (
        <>
          <div
            className="tab"
            onClick={() => setActiveTab("upload")}
          >
            📄 Upload Docs
          </div>
        </>
      )}

      {role === "c_level" && (
        <div
          className="tab"
          onClick={() => setActiveTab("users")}
        >
          👤 Add User
        </div>
      )}

    </div>
  );
}
