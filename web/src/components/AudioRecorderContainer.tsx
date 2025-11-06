import React, { useRef, useState } from "react";
import AudioRecorder from "./AudioRecorder";
import { getMediaRecorder, playAudioBlob } from "../helpers/audio";
import { postChat } from "../api/chat";

const AudioRecorderContainer: React.FC = () => {
  const [isRecording, setIsRecording] = useState<boolean>(false);

  const mediaRecorderRef = useRef<MediaRecorder>(null);
  const chunksRef = useRef<Blob[]>([]);

  const handleRecordingComplete = async (audioBlob: Blob) => {
    const response = await postChat(audioBlob);
    await playAudioBlob(response);
    console.log(response)
    console.log(audioBlob)
  };

  const handleStart = async (): Promise<void> => {
    chunksRef.current = [];
    mediaRecorderRef.current = await getMediaRecorder(chunksRef);
    setIsRecording(true);

  };

  const handleStop = async (): Promise<void> => {
    if (mediaRecorderRef.current && isRecording) {
      const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
      mediaRecorderRef.current.stop();
      await handleRecordingComplete(audioBlob);
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
