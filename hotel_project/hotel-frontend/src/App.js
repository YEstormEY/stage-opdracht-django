import React, { useState, useEffect } from "react"; // Import React and hooks for state and side effects
import CitySelectPage from "./components/CitySelectPage"; // Import the city selection component
import HotelsPage from "./components/HotelsPage"; // Import the hotels display component
import "./styles/styles.css"; // Import the global CSS styles

function App() {
  // State to store an array of city objects fetched from the API
  const [cities, setCities] = useState([]);
  // State to track any errors that occur during data fetching
  const [error, setError] = useState(null);
  // State to store the currently selected city object
  const [selectedCity, setSelectedCity] = useState(null);
  // State to determine which page to show: either the city selection ("select") or the hotels ("hotels") page
  const [page, setPage] = useState("select");

  // Fetch cities from the API when the component mounts
  useEffect(() => {
    const fetchCities = async () => {
      try {
        // Make a GET request to fetch the list of cities
        const response = await fetch("http://127.0.0.1:8000/hotels/api/cities/");
        if (!response.ok) {
          // If HTTP response is not ok, throw an error to be caught in the catch block
          throw new Error("Error fetching cities");
        }
        // Parse the JSON data from the response
        const data = await response.json();
        // Update the cities state with the fetched data
        setCities(data);
      } catch (err) {
        // Log any errors and update the error state to notify the user
        console.error("Error fetching cities:", err);
        setError("Failed to load cities. Please try again later.");
      }
    };

    fetchCities();
  }, []); // Empty dependency array means this runs only once when the component mounts

  // Handler to select a city by its code
  const handleSelectCity = (code) => {
    // Find the city in the current cities list that matches the selected code
    const city = cities.find((c) => c.code === code);
    if (city) {
      // Update state with the selected city and move to the hotels page
      setSelectedCity(city);
      setPage("hotels");
    }
  };

  // Handler to go back from the hotels page to the city selection page
  const handleBack = () => {
    // Reset selected city and switch back to the "select" page
    setSelectedCity(null);
    setPage("select");
  };

  return (
    <div className="min-h-screen" style={{ padding: "1rem" }}>
      {/* Conditionally render the CitySelectPage if the page state is "select" */}
      {page === "select" && (
        <CitySelectPage cities={cities} error={error} onSelectCity={handleSelectCity} />
      )}
      {/* Conditionally render the HotelsPage if a city is selected and the page state is "hotels" */}
      {page === "hotels" && selectedCity && (
        <HotelsPage selectedCity={selectedCity} onBack={handleBack} />
      )}
    </div>
  );
}

export default App;