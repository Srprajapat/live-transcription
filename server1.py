from whisper_live.server import TranscriptionServer

server = TranscriptionServer()
# Runs on localhost port 9090
server.run("0.0.0.0", 9090, backend="faster_whisper")