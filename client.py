import asyncio
import websockets
import pyaudio
import sys

# Audio Configuration
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000
SERVER_URI = "ws://localhost:8765"

async def send_audio(websocket, stream):
    """Continuously read audio from mic and send to server."""
    print("🎤 Microphone capture started. Sending audio...")
    try:
        while True:
            # Read audio chunk. exception_on_overflow=False prevents crashing if system is slow
            data = await asyncio.to_thread(stream.read, CHUNK, exception_on_overflow=False)
            await websocket.send(data)
            # Small sleep to yield control if needed, though await send does that
            await asyncio.sleep(0) 
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ Connection closed by server.")
    except Exception as e:
        print(f"❌ Error sending audio: {e}")

async def receive_transcription(websocket):
    """Continuously receive transcription text from server."""
    try:
        async for message in websocket:
            # Clear line and print new text (simple visualization)
            # \r returns to start of line, end="" prevents newline
            print(f"\r📝 Transcription: {message}", end="", flush=True)
            # Print a newline occasionally or just let it stream? 
            # Let's just print it out.
            print("") 
    except websockets.exceptions.ConnectionClosed:
        print("\n⚠️ Connection closed.")
    except Exception as e:
        print(f"\n❌ Error receiving: {e}")

async def run_client():
    p = pyaudio.PyAudio()
    
    try:
        # Open audio stream
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        print(f"Connecting to {SERVER_URI}...")
        async with websockets.connect(SERVER_URI) as websocket:
            print("✅ Connected! Speak into your microphone.")
            print("Press Ctrl+C to stop.")
            
            # Create tasks for sending and receiving
            send_task = asyncio.create_task(send_audio(websocket, stream))
            receive_task = asyncio.create_task(receive_transcription(websocket))
            
            # Wait for both (or until one fails/stops)
            await asyncio.gather(send_task, receive_task)
            
    except OSError as e:
        print(f"❌ Audio Device Error: {e}")
        print("Check your microphone settings.")
    except ConnectionRefusedError:
        print(f"❌ Could not connect to server at {SERVER_URI}")
        print("Make sure server.py is running first.")
    except KeyboardInterrupt:
        print("\n🛑 Stopping client...")
    finally:
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        p.terminate()

if __name__ == "__main__":
    try:
        asyncio.run(run_client())
    except KeyboardInterrupt:
        pass
