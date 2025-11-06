import React from 'react';
import AudioRecorderContainer from "../components/AudioRecorderContainer";

function HomePage() {

  return (
    <div className="App">
      <header className="App-header">
        <h1>Audio Chatbot</h1>
      </header>

      <main className="App-main">
        <AudioRecorderContainer />
      </main>
    </div>
  );
}

export default HomePage;
