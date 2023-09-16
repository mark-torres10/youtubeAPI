import './App.css';

import React, { useState } from 'react';
import './App.css';

function App() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearchSubmit = () => {
    // Handle the search here (we'll add this functionality later)
    console.log('Searching for:', searchTerm);
  };

  return (
    <div className="App">
      <h1>Search App</h1>
      <input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={handleSearchChange}
      />
      <button onClick={handleSearchSubmit}>Search</button>
    </div>
  );
}

export default App;
