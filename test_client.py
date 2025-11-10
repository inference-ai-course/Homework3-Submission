#!/usr/bin/env python3
"""
Test client for Voice Assistant API

This script allows you to test the voice assistant by:
1. Recording audio from your microphone (optional)
2. Sending audio files to the API
3. Playing back the responses
"""

import requests
import argparse
import time
from pathlib import Path

API_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Checking API health...")
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        health_data = response.json()

        print(f"Status: {health_data['status']}")
        print(f"ASR Model Loaded: {health_data['asr_loaded']}")
        print(f"LLM Model Loaded: {health_data['llm_loaded']}")
        print(f"CUDA Available: {health_data['cuda_available']}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def get_conversation():
    """Get current conversation history"""
    try:
        response = requests.get(f"{API_URL}/conversation")
        response.raise_for_status()
        data = response.json()

        print(f"\nConversation History (Turn {data['turn_count']}/{5}):")
        print("-" * 60)
        for msg in data['history']:
            role = msg['role'].upper()
            content = msg['content']
            print(f"{role}: {content}\n")
        return data
    except Exception as e:
        print(f"Failed to get conversation: {e}")
        return None

def reset_conversation():
    """Reset conversation history"""
    try:
        response = requests.post(f"{API_URL}/reset")
        response.raise_for_status()
        print("Conversation reset successfully")
        return True
    except Exception as e:
        print(f"Failed to reset conversation: {e}")
        return False

def send_audio(audio_path: str, output_path: str = None):
    """
    Send audio file to the chat endpoint

    Args:
        audio_path: Path to input audio file
        output_path: Path to save response audio (optional)
    """
    audio_file = Path(audio_path)

    if not audio_file.exists():
        print(f"Error: Audio file not found: {audio_path}")
        return False

    print(f"\nSending audio: {audio_path}")

    try:
        with open(audio_file, "rb") as f:
            files = {"file": (audio_file.name, f, "audio/wav")}

            print("Waiting for response...")
            start_time = time.time()

            response = requests.post(
                f"{API_URL}/chat/",
                files=files,
                timeout=120  # 2 minute timeout
            )

            elapsed = time.time() - start_time

            response.raise_for_status()

            # Save response audio
            if output_path is None:
                output_path = f"response_{int(time.time())}.wav"

            with open(output_path, "wb") as out_f:
                out_f.write(response.content)

            print(f"Response received in {elapsed:.2f}s")
            print(f"Response saved to: {output_path}")

            return True

    except requests.exceptions.Timeout:
        print("Request timed out. The server might be processing a large request.")
        return False
    except Exception as e:
        print(f"Failed to send audio: {e}")
        return False

def interactive_mode():
    """Interactive testing mode"""
    print("\n" + "=" * 60)
    print("Voice Assistant - Interactive Test Mode")
    print("=" * 60)

    if not test_health():
        print("\nError: API is not healthy. Make sure the server is running.")
        return

    print("\nCommands:")
    print("  send <audio_file>  - Send audio file to assistant")
    print("  history            - View conversation history")
    print("  reset              - Reset conversation")
    print("  health             - Check API health")
    print("  quit               - Exit")
    print()

    while True:
        try:
            command = input("\n> ").strip().split()

            if not command:
                continue

            cmd = command[0].lower()

            if cmd == "quit" or cmd == "exit":
                print("Goodbye!")
                break

            elif cmd == "send":
                if len(command) < 2:
                    print("Usage: send <audio_file>")
                    continue
                audio_path = command[1]
                send_audio(audio_path)

            elif cmd == "history":
                get_conversation()

            elif cmd == "reset":
                reset_conversation()

            elif cmd == "health":
                test_health()

            else:
                print(f"Unknown command: {cmd}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Test client for Voice Assistant API")
    parser.add_argument("--audio", "-a", help="Path to audio file to send")
    parser.add_argument("--output", "-o", help="Path to save response audio")
    parser.add_argument("--health", action="store_true", help="Check API health")
    parser.add_argument("--history", action="store_true", help="View conversation history")
    parser.add_argument("--reset", action="store_true", help="Reset conversation")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    # Interactive mode
    if args.interactive or (not args.audio and not args.health and not args.history and not args.reset):
        interactive_mode()
        return

    # Single command mode
    if args.health:
        test_health()

    if args.history:
        get_conversation()

    if args.reset:
        reset_conversation()

    if args.audio:
        send_audio(args.audio, args.output)

if __name__ == "__main__":
    main()
