import React, { useState } from "react";

export function CitySelectPage({ cities, error, onSelectCity }) {
  const [searchTerm, setSearchTerm] = useState("");

  const handleInputChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredCities = cities.filter((city) =>
    city.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleCityClick = (city) => {
    onSelectCity(city.code);
    setSearchTerm(city.name);
  };

  return (
    <div className="container">
      <h1 className="header">Select a City</h1>
      {error && <p className="error">{error}</p>}
      <div style={{ position: "relative" }}>
        <label htmlFor="city-search" className="label">
          Type a city name:
        </label>
        <input
          id="city-search"
          type="text"
          value={searchTerm}
          onChange={handleInputChange}
          className="input"
          placeholder="Search for a city..."
        />
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