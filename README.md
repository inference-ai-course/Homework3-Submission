# Start the FastAPI server that will be running on http://localhost:8000/chat
# If server is deployed on a difference machine than the client, remember to modify the config.ini file
ollama run llama3
cd server
uvicorn main:app --reload

# Connect to the server and send request through uploading audio files or live recording
# 1. Test with python client:
cd client
python testApp.py <round> (where round is an integer of value 1, 2, 3, 4, or 5)

python testApp.py 1 --> upload input/input1.m4a and a result1.mp3 with audio answers is returned
python testApp.py 2 --> upload input/input2.m4a and a result2.mp3 with audio answers is returned
python testApp.py 3 --> upload input/input3.m4a and a result3.mp3 with audio answers is returned
python testApp.py 4 --> upload input/input4.m4a and a result4.mp3 with audio answers is returned
python testApp.py 5 --> upload input/input5.m4a and a result5.mp3 with audio answers is returned

# 2. Test with UI:
cd UI
python voiceChatBot.py
Go to http://localhost:7860/ to chat by either uploading audio file or live recording