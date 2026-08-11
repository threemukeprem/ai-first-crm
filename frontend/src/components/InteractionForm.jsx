import { useState } from "react";

function InteractionForm({ hcps, onSubmit }) {
  const [form, setForm] = useState({
    hcp_id: "",
    interaction_type: "Product Discussion",
    channel: "In-Person",
    interaction_date: new Date().toISOString().slice(0, 16),
    notes: "",
    products_discussed: "",
    topics_discussed: "",
    objections: "",
    outcome: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    onSubmit({
      ...form,
      hcp_id: Number(form.hcp_id),
    });

    setForm({
      hcp_id: "",
      interaction_type: "Product Discussion",
      channel: "In-Person",
      interaction_date: new Date().toISOString().slice(0, 16),
      notes: "",
      products_discussed: "",
      topics_discussed: "",
      objections: "",
      outcome: "",
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Log Interaction</h2>

      <select
        name="hcp_id"
        value={form.hcp_id}
        onChange={handleChange}
        required
      >
        <option value="">Select HCP</option>

        {hcps.map((hcp) => (
          <option key={hcp.id} value={hcp.id}>
            {hcp.full_name}
          </option>
        ))}
      </select>

      <br /><br />

      <textarea
        name="notes"
        placeholder="Interaction Notes"
        value={form.notes}
        onChange={handleChange}
        rows={6}
        required
      />

      <br /><br />

      <input
        name="products_discussed"
        placeholder="Products Discussed"
        value={form.products_discussed}
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="topics_discussed"
        placeholder="Topics Discussed"
        value={form.topics_discussed}
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="objections"
        placeholder="Objections"
        value={form.objections}
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="outcome"
        placeholder="Outcome"
        value={form.outcome}
        onChange={handleChange}
      />

      <br /><br />

      <button type="submit">
        Save Interaction
      </button>
    </form>
  );
}

export default InteractionForm;