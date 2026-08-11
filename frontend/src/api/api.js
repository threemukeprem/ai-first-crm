import axios from "axios";

const API = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ||
    "https://ai-first-crm-backend-dwf2.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

export default API;