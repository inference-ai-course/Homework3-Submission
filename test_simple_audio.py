"""
Simple Test Script for Voice Agent

Creates test audio, sends to API, and plays response.
"""
import requests
from gtts import gTTS
import os
import sys


def create_test_audio(text: str, filename: str = "test_input.wav"):
    """Create test audio file"""
    print(f"Creating test audio: '{text}'")
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    print(f"✓ Saved to {filename}")
    return filename


def test_voice_agent(audio_file: str, session_id: str = None):
    """Test the voice agent API"""
    url = "http://localhost:8000/chat/"
    
    print(f"\nSending request to {url}")
    
    # Check if server is running
    try:
        import requests
        health_check = requests.get("http://localhost:8000/health/", timeout=2)
        if health_check.status_code != 200:
            raise requests.exceptions.ConnectionError("Server health check failed")
    except requests.exceptions.RequestException:
        raise requests.exceptions.ConnectionError("Cannot connect to server")
    
    # Prepare request
    headers = {}
    if session_id:
        headers["X-Session-ID"] = session_id
        print(f"Using session: {session_id}")
    
    # Send audio
    with open(audio_file, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files, headers=headers)
    
    # Check response
    if response.status_code == 200:
        print("✓ Request successful!")
        
        # Extract metadata from headers
        session_id = response.headers.get("X-Session-ID")
        transcript = response.headers.get("X-Transcript")
        bot_response = response.headers.get("X-Bot-Response")
        turn_number = response.headers.get("X-Turn-Number")
        processing_time = response.headers.get("X-Processing-Time")
        
        print(f"\n{'=' * 60}")
        print(f"Session ID: {session_id}")
        print(f"Turn: {turn_number}/5")
        print(f"Processing Time: {processing_time}s")
        print(f"{'=' * 60}")
        print(f"\nYou said: {transcript}")
        print(f"Bot said: {bot_response}")
        print(f"{'=' * 60}\n")
        
        # Save response audio
        output_file = f"response_turn{turn_number}.mp3"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"✓ Response saved to {output_file}")
        
        return session_id, output_file
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.json())
        return None, None


def run_5_turn_conversation():
    """Run a complete 5-turn conversation"""
    print("\n" + "=" * 60)
    print("VOICE AGENT - 5 TURN CONVERSATION TEST")
    print("=" * 60)
    
    # Test conversation
    test_inputs = [
        "Hello! How are you today?",
        "What's the weather like?",
        "Can you tell me a joke?",
        "What did I just ask you about?",
        "Thanks for chatting with me!"
    ]
    
    session_id = None
    
    for i, text in enumerate(test_inputs, 1):
        print(f"\n{'*' * 60}")
        print(f"TURN {i}/5")
        print(f"{'*' * 60}")
        
        # Create test audio
        audio_file = f"turn{i}_input.wav"
        create_test_audio(text, audio_file)
        
        # Send to API
        session_id, output_file = test_voice_agent(audio_file, session_id)
        
        if not session_id:
            print("✗ Test failed!")
            sys.exit(1)
        
        # Clean up input file
        os.remove(audio_file)
        
        input("\nPress Enter to continue to next turn...")
    
    print(f"\n{'=' * 60}")
    print("✓ ALL 5 TURNS COMPLETED SUCCESSFULLY!")
    print(f"{'=' * 60}")
    print(f"\nSession ID: {session_id}")
    print("\nGenerated files:")
    for i in range(1, 6):
        print(f"  - response_turn{i}.mp3")


def main():
    """Main test function"""
    import sys
    
    if len(sys.argv) > 1:
        # Single test with custom text
        text = " ".join(sys.argv[1:])
        audio_file = create_test_audio(text)
        test_voice_agent(audio_file)
        os.remove(audio_file)
    else:
        # Run full 5-turn test
        try:
            run_5_turn_conversation()
        except KeyboardInterrupt:
            print("\n\nTest interrupted by user")
        except requests.exceptions.ConnectionError:
            print("\n" + "=" * 60)
            print("✗ Cannot connect to API. Is the server running?")
            print("=" * 60)
            print("\nTo start the server:")
            print("  1. Open a new terminal window")
            print("  2. Navigate to the project directory")
            print("  3. Activate the virtual environment:")
            print("     source venv/bin/activate")
            print("  4. Start the server:")
            print("     python main.py")
            print("\nThen run this test script again in another terminal.")
            print("=" * 60)
            sys.exit(1)
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
