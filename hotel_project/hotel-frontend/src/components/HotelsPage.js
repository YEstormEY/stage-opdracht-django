import React, { useState, useEffect } from "react";

export function HotelsPage({ selectedCity, onBack }) {
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorHotels, setErrorHotels] = useState(null);

  useEffect(() => {
    const fetchHotels = async () => {
      if (selectedCity) {
        setLoading(true);
        setErrorHotels(null);
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/hotels/api/hotels/${selectedCity.code}`
          );
          if (!response.ok) {
            throw new Error("Error fetching hotels");
          }
          const data = await response.json();
          setHotels(data);
        } catch (err) {
          console.error("Error fetching hotels:", err);
          setErrorHotels("Failed to load hotels. Please try again later.");
        } finally {
          setLoading(false);
        }
      }
    };
    fetchHotels();
  }, [selectedCity]);

  return (
    <div className="container">
      <button onClick={onBack} className="button">
        &larr; Back
      </button>
      <h1 className="header">Hotels in {selectedCity.name}</h1>
      {errorHotels && <p className="error">{errorHotels}</p>}
      {loading ? (
        <p>Loading hotels...</p>
      ) : hotels.length > 0 ? (
        <ul>
          {hotels.map((hotel) => (
            <li key={hotel.code} className="hotel-card">
              <h3>{hotel.name}</h3>
              <p>Hotel Code: {hotel.code}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No hotels found in this city.</p>
      )}
    </div>
  );
}

export default HotelsPage;