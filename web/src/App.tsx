import React, { useEffect, useState } from 'react';
import HomePage from "./pages/HomePage";
import { requestMicrophonePermission } from "./helpers/audio";

function App() {
  const [hasPermission, setHasPermission] = useState<boolean>(false);

  useEffect(() => {
    requestMicrophonePermission().then((success) => {
      setHasPermission(success);
    });
  }, []);

  return hasPermission ? <HomePage /> :
    <div className="permission-warning">
      Microphone permission required
      <button onClick={requestMicrophonePermission} className="btn btn-primary">
        Grant Permission
      </button>
    </div>
}

export default App;
