import { useEffect, useState } from "react";
import API from "./api/api";
import "./App.css";

function App() {
  const [health, setHealth] = useState("Checking...");
  const [hcps, setHcps] = useState([]);

  const [fullName, setFullName] = useState("");
  const [specialty, setSpecialty] = useState("");
  const [city, setCity] = useState("");

  useEffect(() => {
    checkBackend();
    loadHcps();
  }, []);

  async function checkBackend() {
    try {
      const res = await API.get("/health");
      setHealth(res.data.status);
    } catch (err) {
      console.error("Health check failed:", err);
      setHealth("Backend Error");
    }
  }

  async function loadHcps() {
    try {
      const res = await API.get("/hcps");
      setHcps(res.data);
    } catch (err) {
      console.error("Failed to load HCPs:", err);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      await API.post("/hcps", {
        full_name: fullName,
        specialty,
        city,
      });

      setFullName("");
      setSpecialty("");
      setCity("");

      await loadHcps();
    } catch (err) {
      console.error("Failed to create HCP:", err);
      alert("Failed to add HCP");
    }
  }

  async function handleDelete(id) {
    try {
      await API.delete(`/hcps/${id}`);
      await loadHcps();
    } catch (err) {
      console.error("Failed to delete HCP:", err);
      alert("Failed to delete HCP");
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>AI-First CRM</h1>
        <h3>
          Backend Status: <span>{health}</span>
        </h3>
      </header>

      <div className="card">
        <h2>Add Healthcare Professional</h2>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />

          <input
            type="text"
            placeholder="Specialty"
            value={specialty}
            onChange={(e) => setSpecialty(e.target.value)}
            required
          />

          <input
            type="text"
            placeholder="City"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            required
          />

          <button type="submit">Add HCP</button>
        </form>
      </div>

      <div className="card">
        <h2>Healthcare Professionals</h2>
        <p>Total HCPs: {hcps.length}</p>

        <table width="100%">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Specialty</th>
              <th>City</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {hcps.map((hcp) => (
              <tr key={hcp.id}>
                <td>{hcp.id}</td>
                <td>{hcp.full_name}</td>
                <td>{hcp.specialty}</td>
                <td>{hcp.city}</td>
                <td>
                  <button
                    type="button"
                    onClick={() => handleDelete(hcp.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;