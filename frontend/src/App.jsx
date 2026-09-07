import { useEffect, useState } from "react"

function App() {
  const API_URL = "https://ev-energy-monitor.onrender.com"
  const [power, setPower] = useState(null)
  const [chargers, setChargers] = useState([])
const [health, setHealth] = useState([])
const [recommendation, setRecommendation] = useState(null)   
useEffect(() => {
    const fetchData = () => {
  fetch(`${API_URL}/site/power`)
    .then((response) => response.json())
    .then((data) => setPower(data))

  fetch(`${API_URL}/sensors`)
    .then((response) => response.json())
    .then((data) => setChargers(data))

  fetch(`${API_URL}/site/health`)
    .then((response) => response.json())
    .then((data) => setHealth(data.chargers))
  fetch(`${API_URL}/site/power/recommendation`)
    .then((response) => response.json())
    .then((data) => setRecommendation(data))

  }
    fetchData()

    const interval = setInterval(() => {
  console.log("Refreshing dashboard...")
  fetchData()
}, 5000)

    return () => clearInterval(interval)
  }, [])
  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>EV Energy Monitor</h1>
      <p>Site status: Online</p>

      {power && (
        <div>
          <h2>Site Power</h2>
            {recommendation && recommendation.status === "over_limit" && (
  <div
    style={{
      border: "2px solid red",
      padding: "15px",
      marginBottom: "20px",
      borderRadius: "8px"
    }}
  >
    <h3>⚠️ Power Limit Exceeded</h3>
    <p>
      Reduce charging by {recommendation.power_to_reduce_kw} kW
    </p>
    <p>
      Recommended charger: {recommendation.target_charger}
    </p>
  </div>
)}
          <div style={{ display: "flex", gap: "20px", justifyContent: "center" }}>
            <div style={{ border: "1px solid #ccc", padding: "20px" }}>
              <h3>Current Power</h3>
              <p>{power.current_power_kw} kW</p>
            </div>

            <div style={{ border: "1px solid #ccc", padding: "20px" }}>
              <h3>Power Limit</h3>
              <p>{power.site_power_limit_kw} kW</p>
            </div>

            <div style={{ border: "1px solid #ccc", padding: "20px" }}>
              <h3>Available Power</h3>
              <p>{power.available_power_kw} kW</p>
            </div>
          </div>

              <h2>Charger Status</h2>

        {chargers.map((charger) => {
          const chargerHealth = health.find(
            (item) => item.charger === charger.name
          )

          return (
            <div
              key={charger.id}
              style={{
                border: "1px solid #ccc",
                padding: "20px",
                marginTop: "15px",
                borderRadius: "8px",
                maxWidth: "400px"
              }}
            >
              <h3>{charger.name}</h3>
              <p>Power: {charger.power_kw} kW</p>
              <p>Temperature: {charger.temperature} °F</p>
              <p>Status: {charger.status}</p>

              {chargerHealth && (
                <p style={{
    color: chargerHealth.status === "fresh" ? "green" : "red",
    fontWeight: "bold"
  }}
                
                
                
                
                
                >
                  
                  
                  
                  
                  Health: {chargerHealth.status}
                
                
                
                </p>
              )}
            </div>
          )
        })}
        </div>
      )}
    </div>
  )
}

export default App