import api from "./api";

export const getInteractions = async () => {
  const response = await api.get("/interactions");
  return response.data;
};

export const createInteraction = async (data) => {
  const response = await api.post("/interactions", data);
  return response.data;
};

export const analyzeInteraction = async (interactionId) => {
  const response = await api.post(
    `/ai/analyze-interaction/${interactionId}`,
    {
      create_follow_up: true,
    }
  );

  return response.data;
};