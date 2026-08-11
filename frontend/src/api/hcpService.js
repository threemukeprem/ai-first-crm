import api from "./api";

export const getHcps = async () => {
  const response = await api.get("/hcps");
  return response.data;
};

export const getHcp = async (id) => {
  const response = await api.get(`/hcps/${id}`);
  return response.data;
};

export const createHcp = async (data) => {
  const response = await api.post("/hcps", data);
  return response.data;
};

export const updateHcp = async (id, data) => {
  const response = await api.patch(`/hcps/${id}`, data);
  return response.data;
};

export const deleteHcp = async (id) => {
  await api.delete(`/hcps/${id}`);
};