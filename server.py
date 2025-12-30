import asyncio
import websockets
import numpy as np
from faster_whisper import WhisperModel

# Configuration
HOST = "localhost"
PORT = 8765
MODEL_SIZE = "tiny"  # Options: tiny, base, small, medium, large
SAMPLE_RATE = 16000

print(f"Loading Whisper model ({MODEL_SIZE})...")
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
print("Model loaded.")

async def transcribe_audio(websocket):
    print(f"Client connected from {websocket.remote_address}")
    
    # Buffer to hold audio data
    audio_buffer = np.array([], dtype=np.float32)
    
    # Parameters for processing
    # Process every 2 seconds of audio
    PROCESS_INTERVAL_SAMPLES = 2 * SAMPLE_RATE 
    # Keep 0.5 seconds of overlap to avoid cutting words at boundaries
    OVERLAP_SAMPLES = int(0.5 * SAMPLE_RATE)
    
    try:
        async for message in websocket:
            # Receive audio chunk (assuming float32 bytes)
            chunk = np.frombuffer(message, dtype=np.float32)
            audio_buffer = np.concatenate((audio_buffer, chunk))
            
            # If buffer is large enough, transcribe
            if len(audio_buffer) >= PROCESS_INTERVAL_SAMPLES:
                # Transcribe the current buffer
                segments, info = model.transcribe(audio_buffer, beam_size=5, language="en")
                
                transcription_text = " ".join([segment.text for segment in segments]).strip()
                
                if transcription_text:
                    print(f"Transcribed: {transcription_text}")
                    await websocket.send(transcription_text)
                
                # Keep the overlap for the next chunk
                audio_buffer = audio_buffer[-OVERLAP_SAMPLES:]
                
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    print(f"Starting WebSocket server on ws://{HOST}:{PORT}")
    async with websockets.serve(transcribe_audio, HOST, PORT):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
