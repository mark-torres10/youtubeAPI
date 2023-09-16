import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [showChannels, setShowChannels] = useState(false);
  const [showEpisodes, setShowEpisodes] = useState(false);
  const [channels, setChannels] = useState([]);
  const [episodes, setEpisodes] = useState([]);

  const fetchChannels = () => {
    axios.get('/api/channels/')
      .then((response) => {
        setChannels(response.data);
        setShowChannels(true);
      })
      .catch((error) => {
        console.error('Error fetching channels:', error);
      });
  };

  const fetchEpisodes = () => {
    axios.get('/api/episodes/')
      .then((response) => {
        setEpisodes(response.data);
        setShowEpisodes(true);
      })
      .catch((error) => {
        console.error('Error fetching episodes:', error);
      });
  };

  return (
    <div className="App">
      <div>
        <button onClick={fetchChannels}>Fetch Channels</button>
        <button onClick={fetchEpisodes}>Fetch Episodes</button>
      </div>
      {showChannels && (
        <div>
          <h2>Channels</h2>
          <table>
            {/* Render table rows for channels */}
          </table>
        </div>
      )}
      {showEpisodes && (
        <div>
          <h2>Episodes</h2>
          <table>
            {/* Render table rows for episodes */}
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
