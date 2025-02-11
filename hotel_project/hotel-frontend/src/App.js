import React, { useState, useEffect } from "react";
import CitySelectPage from "./components/CitySelectPage";
import HotelsPage from "./components/HotelsPage";
import "./styles/styles.css";

function App() {
  const [cities, setCities] = useState([]);
  const [error, setError] = useState(null);
  const [selectedCity, setSelectedCity] = useState(null);
  const [page, setPage] = useState("select");

  useEffect(() => {
    const fetchCities = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/hotels/api/cities/");
        if (!response.ok) {
          throw new Error("Error fetching cities");
        }
        const data = await response.json();
        setCities(data);
      } catch (err) {
        console.error("Error fetching cities:", err);
        setError("Failed to load cities. Please try again later.");
      }
    };
    fetchCities();
  }, []);

  const handleSelectCity = (code) => {
    const city = cities.find((c) => c.code === code);
    if (city) {
      setSelectedCity(city);
      setPage("hotels");
    }
  };

  const handleBack = () => {
    setSelectedCity(null);
    setPage("select");
  };

  return (
    <div className="min-h-screen" style={{ backgroundColor: "#f7fafc", padding: "1rem" }}>
      {page === "select" && (
        <CitySelectPage cities={cities} error={error} onSelectCity={handleSelectCity} />
      )}
      {page === "hotels" && selectedCity && (
        <HotelsPage selectedCity={selectedCity} onBack={handleBack} />
      )}
    </div>
  );
}

export default App;
