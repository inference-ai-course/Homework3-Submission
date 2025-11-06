import React from 'react';

type AudioRecorderDisplayProps = {
  isRecording: boolean;
  onStart: () => void;
  onStop: () => void;
};

const AudioRecorder: React.FC<AudioRecorderDisplayProps> = ({
  isRecording,
  onStart,
  onStop
}) => {
  return (
    <div className="audio-recorder">
      <div className="recorder-container">
        <div className="recorder-controls">
          {isRecording ? (
            <button onClick={onStop} className="btn btn-stop">
              Send to Chatbot
            </button>
          ) : (
            <button
              onClick={onStart}
              className="btn btn-record"
            >
              Start Recording
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AudioRecorder;
