import asyncio
import websockets
import numpy as np
from faster_whisper import WhisperModel

HOST = "localhost"
PORT = 8765
MODEL_SIZE = "small"     # better than tiny, still fast
SAMPLE_RATE = 16000

print(f"Loading Whisper model ({MODEL_SIZE})...")
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
print("Model loaded.")

PROCESS_INTERVAL_SEC = 1.0
OVERLAP_SEC = 0.25

PROCESS_INTERVAL_SAMPLES = int(PROCESS_INTERVAL_SEC * SAMPLE_RATE)
OVERLAP_SAMPLES = int(OVERLAP_SEC * SAMPLE_RATE)

async def transcribe_audio(websocket):
    print(f"Client connected from {websocket.remote_address}")
    audio_buffer = np.array([], dtype=np.float32)

    try:
        async for message in websocket:
            chunk = np.frombuffer(message, dtype=np.float32)
            audio_buffer = np.concatenate((audio_buffer, chunk))

            if len(audio_buffer) >= PROCESS_INTERVAL_SAMPLES:
                segments, info = model.transcribe(
                    audio_buffer,
                    beam_size=5,
                    vad_filter=True,
                    temperature=0.0,
                )

                text = " ".join(seg.text for seg in segments).strip()
                if text:
                    await websocket.send(text)

                audio_buffer = audio_buffer[-OVERLAP_SAMPLES:]

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    print(f"Server running on ws://{HOST}:{PORT}")
    async with websockets.serve(transcribe_audio, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
