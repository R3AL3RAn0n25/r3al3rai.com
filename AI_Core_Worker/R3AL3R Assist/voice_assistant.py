# Unified Voice Assistant for R3AL3R AI
import os
import time
import threading
import numpy as np
import whisper
import pyaudio
import asyncio
import edge_tts
import webrtcvad
import subprocess
from pydub import AudioSegment
from pydub.playback import play
import nemo.collections.asr as nemo_asr
import tempfile
import soundfile as sf

# Configure pydub to use the correct ffmpeg path
AudioSegment.converter = r"C:\Users\work8\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"

class VoiceAssistant:
    def __init__(self, ai_core, use_nemo=True):
        self.ai = ai_core
        self.wake_word = "realer"
        self.premium = True
        self.listening = False
        self.use_nemo = use_nemo

        if self.use_nemo:
            print("Loading NeMo Canary ASR model...")
            self.asr_model = nemo_asr.models.ASRModel.from_pretrained("nvidia/canary-1b-v2")
        else:
            print("Loading Whisper model (this takes a sec)...")
            self.model = whisper.load_model("small.en")

        self.vad = webrtcvad.Vad(2)
        self.p = pyaudio.PyAudio()
        self.stream_in = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=320  # 20ms for VAD
        )

    async def _speak_async(self, text: str):
        print(f"\nR3AL3RAI: {text}")
        communicate = edge_tts.Communicate(text, voice="en-GB-RyanNeural")
        await communicate.save("tmp_voice.mp3")
        try:
            audio = AudioSegment.from_mp3("tmp_voice.mp3")
            play(audio)
        except Exception as e:
            print(f"Error playing audio: {e}")
        finally:
            if os.path.exists("tmp_voice.mp3"):
                os.remove("tmp_voice.mp3")

    def speak(self, text: str):
        asyncio.run(self._speak_async(text))

    def process_query(self, query: str) -> str:
        query = query.lower().strip()

        # Jarvis Mode commands
        if "enable jarvis mode" in query or "activate jarvis" in query:
            if hasattr(self.ai, 'enable_jarvis_mode'):
                success = self.ai.enable_jarvis_mode()
                return "Jarvis Mode activated. I am now monitoring and ready to assist." if success else "Jarvis Mode already active."
        
        if "disable jarvis mode" in query or "deactivate jarvis" in query:
            if hasattr(self.ai, 'disable_jarvis_mode'):
                self.ai.disable_jarvis_mode()
                return "Jarvis Mode deactivated. Returning to standard operation."
        
        if "system status" in query or "status report" in query:
            return "All systems operational. Voice interface active. Standing by for commands."
        
        if "list files" in query:
            path = query.replace("list files", "").strip() or "."
            try:
                files = os.listdir(path)
                return f"{len(files)} items: {', '.join(files[:10])}"
            except Exception as e:
                return f"Access error: {e}"
        
        if "git status" in query:
            try:
                result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True, check=True)
                return result.stdout or "Clean repo."
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                return f"Error executing git status: {e}"

        # Use AI core if available
        if hasattr(self.ai, 'generate_response'):
            return self.ai.generate_response(query)
        
        return "Processing your request..."

    def is_silent(self, data):
        frame = np.frombuffer(data, np.int16).tobytes()
        return not self.vad.is_speech(frame, 16000)

    def listener_loop(self):
        speech_buffer = []
        print(f"Voice layer active — say '{self.wake_word}' + command")

        while self.listening:
            try:
                data = self.stream_in.read(320, exception_on_overflow=False)
            except OSError:
                continue

            if not self.is_silent(data):
                speech_buffer.append(data)
            elif len(speech_buffer) > 0:
                # Process speech when silence is detected
                audio_data = b''.join(speech_buffer)
                speech_buffer = []

                if len(audio_data) > 320 * 10:  # 200ms min speech
                    if self.use_nemo:
                        # Use NeMo Canary for transcription
                        audio_np = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
                        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                            sf.write(tmp_file.name, audio_np, 16000)
                            transcriptions = self.asr_model.transcribe([tmp_file.name])
                            text = transcriptions[0].strip().lower()
                            os.unlink(tmp_file.name)
                    else:
                        # Fallback to Whisper
                        audio_np = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
                        result = self.model.transcribe(audio_np, language="en", fp16=False)
                        text = result["text"].strip().lower()

                    if len(text) > 2 and text not in ['you', '.', 'you.', '']:  # Filter noise
                        print(f"\nYou: {text}")

                        if self.premium and text.startswith("set wake word"):
                            new_word = text.split("set wake word", 1)[-1].strip()
                            if new_word:
                                self.wake_word = new_word
                                self.speak(f"Wake word changed to {new_word}")

                        elif self.wake_word in text:
                            query = text.split(self.wake_word, 1)[-1].strip() or text
                            response = self.process_query(query)
                            if isinstance(response, dict):
                                response = response.get("response", "No response")
                            self.speak(str(response))
    
    def idle_chatter(self):
        """Jarvis Mode idle chatter - more interactive"""
        count = 0
        messages = [
            "Systems nominal. Standing by.",
            "All systems operational. Ready for commands.",
            "Monitoring active. How may I assist?",
            "Voice interface online. Awaiting instructions."
        ]
        msg_index = 0
        
        while self.listening:
            time.sleep(1)
            count += 1
            if count >= 120:  # Every 2 minutes
                if hasattr(self.ai, 'jarvis_mode') and self.ai.jarvis_mode:
                    self.speak(messages[msg_index % len(messages)])
                    msg_index += 1
                else:
                    self.speak("Systems nominal. Standing by.")
                count = 0

    def start(self):
        self.listening = True
        threading.Thread(target=self.listener_loop, daemon=True).start()
        threading.Thread(target=self.idle_chatter, daemon=True).start()
        jarvis_status = " - JARVIS MODE" if hasattr(self.ai, 'jarvis_mode') and self.ai.jarvis_mode else ""
        print(f"R3AL3RAI voice interface fully armed{jarvis_status}.")

    def stop(self):
        self.listening = False
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.p.terminate()
        print("Voice assistant stopped.")

if __name__ == "__main__":
    # Simple mock AI for standalone testing
    class MockAI:
        def __init__(self):
            self.jarvis_mode = False
        
        def generate_response(self, query):
            return f"Received: {query}"
        
        def enable_jarvis_mode(self):
            self.jarvis_mode = True
            return True
        
        def disable_jarvis_mode(self):
            self.jarvis_mode = False
    
    ai = MockAI()
    voice = VoiceAssistant(ai, use_nemo=True)
    voice.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        voice.stop()
