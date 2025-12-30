# Live Audio Transcription with WhisperLive

This project provides real-time audio transcription using OpenAI's Whisper model via WhisperLive, a WebSocket-based server for streaming transcription.

## Features

- Real-time audio transcription from microphone input.
- WebSocket streaming for low-latency transcription.
- Support for multiple Whisper models (tiny, base, small, etc.).
- Client-server architecture for distributed setups.
- Optional web interface and subtitle output.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Srprajapat/live-transcription.git
   cd live-transcription
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

Start the WhisperLive server:

```
python server.py
```

- The server listens on `ws://localhost:8765` by default.
- Loads the Whisper model for transcription.

**Customization**:
- Edit `server.py` to change model (e.g., `model="tiny"` for speed) or language.

### Running the Client

In another terminal, start the client to stream audio:

```
python client.py
```

- Connects to the server and sends microphone audio.
- Receives and prints transcriptions in real-time.
- Press Ctrl+C to stop.

**Variants**:
- `client1.py`: Alternative client implementation.
- `server1.py`: Alternative server implementation.

### Web Interface (Optional)

Open `index.html` in a browser for a simple web-based interface (if implemented).

### Subtitle Output

Transcriptions can be saved to `output.srt` for subtitle files.

## Requirements

- Python 3.8+
- Microphone access
- Internet for initial model download (WhisperLive caches models locally)

## Dependencies

- `faster-whisper`: Optimized Whisper implementation.
- `websockets`: For WebSocket communication.
- `pyaudio`: Audio recording.
- `numpy`: Audio processing.

## Troubleshooting

- **Microphone Issues**: Ensure microphone is enabled and set as default in system settings.
- **Connection Errors**: Check if the server is running on the correct port.
- **Model Download**: First run may take time to download the Whisper model.
- **Port Conflicts**: Change port in `server.py` if 8765 is in use.

## Project Structure

- `server.py`: Main WhisperLive server.
- `client.py`: Main client for audio streaming.
- `client1.py` / `server1.py`: Alternative implementations.
- `index.html`: Web interface (if available).
- `output.srt`: Subtitle output file.
- `requirements.txt`: Python dependencies.

## Contributing

Feel free to open issues or submit pull requests.