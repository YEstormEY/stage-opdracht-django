import React, { useState } from "react"; // Import React and useState hook

export function CitySelectPage({ cities, error, onSelectCity }) {
  // State to store the current search term input by the user
  const [searchTerm, setSearchTerm] = useState("");

  // Update state when the user types in the search input
  const handleInputChange = (e) => {
    setSearchTerm(e.target.value);
  };

  // Filter the cities based on search term (case insensitive match)
  const filteredCities = cities.filter((city) =>
    city.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // When a city is clicked in the autocomplete list, select it via the passed callback
  const handleCityClick = (city) => {
    onSelectCity(city.code);
    // Optionally update the search term to display the selected city's name
    setSearchTerm(city.name);
  };

  return (
    <div className="container">
      <h1 className="header">Select a City</h1>
      {/* Display error message if there's an error */}
      {error && <p className="error">{error}</p>}
      <div style={{ position: "relative" }}>
        <label htmlFor="city-search" className="label">
          Type a city name:
        </label>
        {/* Input for the search term */}
        <input
          id="city-search"
          type="text"
          value={searchTerm}
          onChange={handleInputChange}
          className="input"
          placeholder="Search for a city..."
        />
        {/* Display autocomplete suggestions if there is a search term and at least one matching city */}
        {searchTerm && filteredCities.length > 0 && (
          <ul className="autocomplete-list">
            {filteredCities.map((city) => (
              <li
                key={city.code}
                className="autocomplete-item"
                onClick={() => handleCityClick(city)}
              >
                {city.name}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default CitySelectPage;