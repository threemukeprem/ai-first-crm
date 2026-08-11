import { useState } from "react";

function HcpForm({ onSubmit }) {
  const [form, setForm] = useState({
    full_name: "",
    specialty: "",
    organization: "",
    city: "",
    email: "",
    phone: "",
    preferred_channel: "",
    notes: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);

    setForm({
      full_name: "",
      specialty: "",
      organization: "",
      city: "",
      email: "",
      phone: "",
      preferred_channel: "",
      notes: "",
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add Healthcare Professional</h2>

      <input
        name="full_name"
        placeholder="Full Name"
        value={form.full_name}
        onChange={handleChange}
        required
      />

      <input
        name="specialty"
        placeholder="Specialty"
        value={form.specialty}
        onChange={handleChange}
      />

      <input
        name="organization"
        placeholder="Organization"
        value={form.organization}
        onChange={handleChange}
      />

      <input
        name="city"
        placeholder="City"
        value={form.city}
        onChange={handleChange}
      />

      <input
        name="email"
        placeholder="Email"
        value={form.email}
        onChange={handleChange}
      />

      <input
        name="phone"
        placeholder="Phone"
        value={form.phone}
        onChange={handleChange}
      />

      <input
        name="preferred_channel"
        placeholder="Preferred Channel"
        value={form.preferred_channel}
        onChange={handleChange}
      />

      <textarea
        name="notes"
        placeholder="Notes"
        value={form.notes}
        onChange={handleChange}
      />

      <br />
      <br />

      <button type="submit">
        Add HCP
      </button>
    </form>
  );
}

export default HcpForm;