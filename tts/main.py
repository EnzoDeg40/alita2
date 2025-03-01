import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Initialize TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# List speakers
print(tts.speakers)

# TTS to a file, use a preset speaker
tts.tts_to_file(
  text="Hello world!",
  speaker="Craig Gutsy",
  language="en",
  file_path="output.wav"
)