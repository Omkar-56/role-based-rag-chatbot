import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import QueryForm from "../components/QueryForm";
import UploadForm from "../components/UploadForm";
import AddUserForm from "../components/AddUserForm";

export default function Dashboard() {
  const role = localStorage.getItem("role");
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("chat");

  const logout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <div style={{ display: "flex" }}>
      <Sidebar
        role={role}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      <div style={{ flex: 1, padding: 20 }}>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <h2>Dashboard ({role})</h2>
          <button onClick={logout}>Logout</button>
        </div>

        <hr />

        {activeTab === "chat" && <QueryForm />}

        {activeTab === "upload" && <UploadForm />}

        {activeTab === "users" && <AddUserForm />}
      </div>
    </div>
  );
}
