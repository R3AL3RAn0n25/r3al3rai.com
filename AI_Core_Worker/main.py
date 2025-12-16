# main.py - R3AL3R AI with integrated voice assistant and Jarvis Mode
import time
import os
import AI_Core_Worker as ai_module

if __name__ == "__main__":
    print("🚀 Starting R3AL3R AI System...")
    
    # Initialize AI Core with voice capabilities
    enable_voice = os.environ.get("ENABLE_VOICE", "true").lower() == "true"
    ai = ai_module.RealerAI(enable_voice=enable_voice)
    
    print("\n📋 Available Commands:")
    print("  - Say 'realer enable jarvis mode' to activate voice assistant")
    print("  - Say 'realer system status' for status report")
    print("  - Say 'realer list files' to list current directory")
    print("  - Press Ctrl+C to exit")
    
    if enable_voice:
        print("\n🎤 Voice interface ready. Say 'realer' followed by your command.")
        # Auto-enable Jarvis Mode for standalone operation
        ai.enable_jarvis_mode()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down R3AL3R AI...")
        if ai.voice_assistant:
            ai.disable_jarvis_mode()
        print("Goodbye!")

