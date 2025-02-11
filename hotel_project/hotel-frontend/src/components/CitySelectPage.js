import React from 'react';


export function CitySelectPage({ cities, error, onSelectCity }) {
    const handleChange = (e) => {
      onSelectCity(e.target.value);
    };
  
    return (
      <div className="container">
        <h1 className="header">Select a City</h1>
        {error && <p className="error">{error}</p>}
        <div>
          <label htmlFor="city-select" className="label">
            Select a city:
          </label>
          <select
            id="city-select"
            defaultValue=""
            onChange={handleChange}
            className="select"
          >
            <option value="">-- Choose a city --</option>
            {cities.map((city) => (
              <option key={city.code} value={city.code}>
                {city.name}
              </option>
            ))}
          </select>
        </div>
      </div>
    );
  }
  
  export default CitySelectPage;
  