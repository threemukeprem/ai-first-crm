import API from "./api";

// Get all HCPs
export async function getHcps() {
  const response = await API.get("/hcps");
  return response.data;
}

// Create new HCP
export async function createHcp(hcpData) {
  const response = await API.post("/hcps", hcpData);
  return response.data;
}

// Delete HCP
export async function deleteHcp(id) {
  const response = await API.delete(`/hcps/${id}`);
  return response.data;
}