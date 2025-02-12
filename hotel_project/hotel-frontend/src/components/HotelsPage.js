import React, { useState, useEffect } from "react"; // Import React and hooks

export function HotelsPage({ selectedCity, onBack }) {
  // State to store the list of hotels for the selected city
  const [hotels, setHotels] = useState([]);
  // State to track the loading status during the API request
  const [loading, setLoading] = useState(false);
  // State to track any errors that occur during the fetch for hotels
  const [errorHotels, setErrorHotels] = useState(null);

  // This effect runs each time the selectedCity changes
  useEffect(() => {
    const fetchHotels = async () => {
      if (selectedCity) {
        setLoading(true);
        setErrorHotels(null);
        try {
          // Fetch hotels for the specific selected city using its code
          const response = await fetch(
            `http://127.0.0.1:8000/hotels/api/hotels/${selectedCity.code}`
          );
          if (!response.ok) {
            throw new Error("Error fetching hotels");
          }
          // Parse the JSON data from the response
          const data = await response.json();
          // Set the hotels state with the fetched data
          setHotels(data);
        } catch (err) {
          // Log any errors and update error state for display
          console.error("Error fetching hotels:", err);
          setErrorHotels("Failed to load hotels. Please try again later.");
        } finally {
          // Change loading state to false regardless of outcome
          setLoading(false);
        }
      }
    };

    fetchHotels();
  }, [selectedCity]);

  return (
    <div className="container">
      {/* Button to navigate back to the city select screen */}
      <button onClick={onBack} className="button">
        &larr; Back
      </button>
      <h1 className="header">Hotels in {selectedCity.name}</h1>
      {/* Show error message if an error occurred during hotel fetch */}
      {errorHotels && <p className="error">{errorHotels}</p>}
      {loading ? (
        // Display loading text while the request is in progress
        <p>Loading hotels...</p>
      ) : hotels.length > 0 ? (
        // If hotels exist, render them as an unordered list with styled cards
        <ul>
          {hotels.map((hotel) => (
            <li key={hotel.code} className="hotel-card">
              <h3>{hotel.name}</h3>
              <p>Hotel Code: {hotel.code}</p>
            </li>
          ))}
        </ul>
      ) : (
        // If no hotels exist, inform the user
        <p>No hotels found in this city.</p>
      )}
    </div>
  );
}

export default HotelsPage;