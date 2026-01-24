import { useState } from "react";
import { api } from "../services/api";

export default function AddUserForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("hr");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const createUser = async () => {
    if (!username || !password) {
      setStatus("❌ Username and password required");
      return;
    }

    setLoading(true);
    setStatus("");

    try {
      const res = await api.post("/users", {
        username,
        password,
        role,
      });

      setStatus(`✅ User created: ${res.data.username}`);
      setUsername("");
      setPassword("");
      setRole("hr");
    } catch (err) {
      if (err.response?.status === 403) {
        setStatus("❌ Only admin can create users");
      } else {
        setStatus("❌ Failed to create user (maybe already exists)");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500 }}>
      <h3>Add New User</h3>

      <div style={{ marginBottom: 10 }}>
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>

      <div style={{ marginBottom: 10 }}>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <div style={{ marginBottom: 10 }}>
        <label>Role</label>
        <br />
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="hr">HR</option>
          <option value="finance">Finance</option>
          <option value="engineering">Engineering</option>
          <option value="marketing">Marketing</option>
          <option value="general">General</option>
          <option value="c_level">C-Level</option>
        </select>
      </div>

      <button onClick={createUser} disabled={loading}>
        {loading ? "Creating..." : "Create User"}
      </button>

      {status && <p style={{ marginTop: 12 }}>{status}</p>}
    </div>
  );
}
