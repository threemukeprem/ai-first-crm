import { useEffect, useState } from "react";
import "./App.css";

import {
  getHcps,
  createHcp,
  deleteHcp,
} from "./api/hcpService";

import {
  createInteraction,
  analyzeInteraction,
} from "./api/interactionService";

import HcpForm from "./components/HcpForm";
import HcpTable from "./components/HcpTable";
import InteractionForm from "./components/InteractionForm";

function App() {
  const [health, setHealth] = useState("Healthy");
  const [hcps, setHcps] = useState([]);
  const [aiResult, setAiResult] = useState(null);

  useEffect(() => {
    loadHcps();
  }, []);

  async function loadHcps() {
    try {
      const data = await getHcps();
      setHcps(data);
      setHealth("Healthy");
    } catch (err) {
      console.error(err);
      setHealth("Backend Error");
    }
  }

  async function handleCreateHcp(data) {
    try {
      await createHcp(data);
      await loadHcps();
    } catch (err) {
      console.error(err);
      alert("Failed to create HCP");
    }
  }

  async function handleDeleteHcp(id) {
    if (!window.confirm("Delete this HCP?")) return;

    try {
      await deleteHcp(id);
      await loadHcps();
    } catch (err) {
      console.error(err);
      alert("Delete failed");
    }
  }

  async function handleInteraction(data) {
    try {
      const interaction = await createInteraction(data);

      const ai = await analyzeInteraction(interaction.id);

      setAiResult(ai);

      alert("Interaction saved and AI analysis completed.");
    } catch (err) {
      console.error(err);
      alert("Interaction creation failed.");
    }
  }

  return (
    <div className="app">

      <header className="header">
        <h1>AI-First CRM</h1>
        <h3>Backend Status: {health}</h3>
      </header>

      <div className="card">

        <HcpForm onSubmit={handleCreateHcp} />

        <hr />

        <h2>Healthcare Professionals</h2>

        <p>
          <strong>Total HCPs:</strong> {hcps.length}
        </p>

        <HcpTable
          hcps={hcps}
          onDelete={handleDeleteHcp}
        />

        <hr />

        <InteractionForm
          hcps={hcps}
          onSubmit={handleInteraction}
        />

        {aiResult && (
          <>
            <hr />

            <h2>AI Analysis</h2>

            <p>
              <strong>Summary:</strong>
              <br />
              {aiResult.ai_summary}
            </p>

            <p>
              <strong>Sentiment:</strong>
              <br />
              {aiResult.sentiment}
            </p>

            <p>
              <strong>Suggested Follow-up:</strong>
              <br />
              {aiResult.suggested_follow_up}
            </p>

            <p>
              <strong>Provider:</strong>
              <br />
              {aiResult.provider}
            </p>

            <p>
              <strong>Follow-up Created:</strong>{" "}
              {aiResult.follow_up_created ? "Yes" : "No"}
            </p>
          </>
        )}

      </div>

    </div>
  );
}

export default App;