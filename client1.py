from whisper_live.client import TranscriptionClient

# Connect to your local server
client = TranscriptionClient("localhost", 9090, model="small", lang="en")

# This opens the mic and starts printing text to your console
client()