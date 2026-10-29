// import React from "react";
// import EnergyCapacity from "./dashboard/EnergyCapacity";
// import EnergySourceDistribution from "./dashboard/EnergySource";
// import CountryInsights from "./dashboard/CountryInsights";
// import EnergyTrends from "./dashboard/EnergyTrends";
// import ChatInterface from "./components/ChatInterface";



// function App() {
//   return (
//     <div >
//       <h1>Siemens RAG+ Assistant</h1>
//       <ChatInterface/>
//       <hr />
//       <h2>Energy Analytics</h2>
//       <h3>Energy Installed Capacity for Country</h3><EnergyCapacity />
//       <h3>Energy Trends in Years</h3><EnergyTrends />
//       <h3>Country Insights </h3><CountryInsights />
//       <h3>Energy Source Distribution</h3><EnergySourceDistribution />

//     </div>
//   );
// }


// export default App;
import React, { useState } from "react";
import EnergyCapacity from "./dashboard/EnergyCapacity";
import EnergySourceDistribution from "./dashboard/EnergySource";
import CountryInsights from "./dashboard/CountryInsights";
import EnergyTrends from "./dashboard/EnergyTrends";
import ChatInterface from "./components/ChatInterface";
import "./App.css";

function App() {
  // State: 'chat' or 'analytics'
  const [activeView, setActiveView] = useState("chat");

  return (
    <div className="app-layout">
      {/* Left Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>⚡ Siemens</h2>
          <p>RAG Assistant</p>
        </div>

        <nav className="sidebar-nav">
          <button
            className={`nav-btn ${activeView === "chat" ? "active" : ""}`}
            onClick={() => setActiveView("chat")}
          >
            <span className="nav-icon">💬</span>
            <span className="nav-text">Chat Assistant</span>
          </button>

          <button
            className={`nav-btn ${activeView === "analytics" ? "active" : ""}`}
            onClick={() => setActiveView("analytics")}
          >
            <span className="nav-icon">📊</span>
            <span className="nav-text">Analytics</span>
          </button>
        </nav>

        {/* <div className="sidebar-footer">
          <p>v1.0.0</p>
        </div> */}
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {activeView === "chat" && <ChatInterface />}

        {activeView === "analytics" && (
          <div className="analytics-container">
            <div className="analytics-header">
              <h1>📊 Energy Analytics Dashboard</h1>
              <p>Insights into global power plant data</p>
            </div>

            <div className="analytics-grid">
              <section className="analytics-section">
                <h3>🔋 Energy Generation Capacity by Country</h3>
                <EnergyCapacity />
              </section>

              <section className="analytics-section">
                <h3>📈 Energy Trends Over Years</h3>
                <EnergyTrends />
              </section>

              {/* <section className="analytics-section">
                <h3>🌍 Country Insights</h3>
                <CountryInsights />
              </section> */}

              <section className="analytics-section">
                <h3>⚡ Primary Fuel Distribution</h3>
                <EnergySourceDistribution />
              </section>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;