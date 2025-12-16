import subprocess
import sys

packages = [
    "openai-whisper",
    "edge_tts",
    "pyaudio",
    "numpy",
    "torch",
    "torchvision",
    "torchaudio"
]

for pkg in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

print("\nAll dependencies installed! Run: python r3al3erai.py")