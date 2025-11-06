import React, { useRef, useState } from "react";
import AudioRecorder from "./AudioRecorder";
import { getMediaRecorder } from "../helpers/audio";

const AudioRecorderContainer: React.FC = () => {
  const [isRecording, setIsRecording] = useState<boolean>(false);

  const mediaRecorderRef = useRef<MediaRecorder>(null);
  const chunksRef = useRef<Blob[]>([]);

  const handleRecordingComplete = (audioBlob: Blob) => {
    // TODO: send audioBlob to backend
    console.log(audioBlob)
  };

  const handleStart = async (): Promise<void> => {
    chunksRef.current = [];
    mediaRecorderRef.current = await getMediaRecorder(
      chunksRef,
      handleRecordingComplete
    );
    setIsRecording(true);

  };

  const handleStop = (): void => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <AudioRecorder
      isRecording={isRecording}
      onStart={handleStart}
      onStop={handleStop}
    />
  );
};

export default AudioRecorderContainer;
