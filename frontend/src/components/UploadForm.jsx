import { useState } from "react";
import { api } from "../services/api";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [department, setDepartment] = useState("general");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) {
      setStatus("Please select a file");
      return;
    }

    setLoading(true);
    setStatus("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post(
        `/documents/upload?department=${department}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setStatus(`✅ Uploaded: ${res.data.filename}`);
      setFile(null);
    } catch (err) {
      setStatus("❌ Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600 }}>
      <h3>Upload Document</h3>

      <div style={{ marginBottom: 12 }}>
        <input
          type="file"
          accept=".md,.csv"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>

      <div style={{ marginBottom: 12 }}>
        <label>Department:</label>
        <br />
        <select
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
        >
          <option value="general">General</option>
          <option value="finance">Finance</option>
          <option value="hr">HR</option>
          <option value="engineering">Engineering</option>
          <option value="marketing">Marketing</option>
        </select>
      </div>

      <button onClick={upload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>

      {status && <p style={{ marginTop: 12 }}>{status}</p>}
    </div>
  );
}
