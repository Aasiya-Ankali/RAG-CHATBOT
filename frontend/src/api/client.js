const API = "http://localhost:8000/api";
const DASHBOARD_API = "http://localhost:8000/dashboard";
const DASHBOARD_POWERPLANT_API ="http://localhost:8000/dashboard_powerplant"

export async function queryRAG(question) {
  try {
    const RES = await fetch(`${API}/query`, {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    if (!RES.ok) {
      throw new Error(`API Error : ${RES.status}`);
    }
    return await RES.json();
  } catch (err) {
    console.error("RAG Query Failed ", err);
    return { answer: "something went wrong ,please try again", sources: [] };
  }
}

export async function chatRAG(question, lastAnswer = null) {
  try {
    const RES = await fetch(`${API}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        question : question, 
        last_answer : lastAnswer 
      }),
    });
    
    if (!RES.ok) {
      throw new Error(`API Error: ${RES.status}`);
    }
    
    const data = await RES.json();
    return data.answer;  // Returns just the answer string
    
  } catch (err) {
    console.error("Chat Failed:", err);
    return "Sorry, something went wrong. Please try again.";
  }
}

export async function getEnergyCapacity() {
    const RES = await fetch(`${DASHBOARD_POWERPLANT_API}/energy_capacity`)
    return RES.json()
}

export async function getEnergyTrends() {
    const RES = await fetch(`${DASHBOARD_POWERPLANT_API}/energy_trends`)
    return RES.json()
}

export async function getCountryData() {
    const RES = await fetch(`${DASHBOARD_POWERPLANT_API}/country_insights`)
    return RES.json()
}

export async function getEnergySourceDistribution() {
    const RES = await fetch(`${DASHBOARD_POWERPLANT_API}/energy_sources`)
    return RES.json()
}
// Exported feature-specific backend fetch functions
export const chatApi = {
  submitQuery: (question) => apiClient('/api/query', { body: { question } }),
};
