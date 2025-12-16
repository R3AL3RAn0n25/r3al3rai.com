#!/usr/bin/env python3
"""
R3AL3R AI - Jarvis Mode Launcher
Quick start script for voice-enabled AI assistant
"""
import os
import sys
import time

# Set environment variables for voice mode
os.environ["ENABLE_VOICE"] = "true"

# Add project paths
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI_Core_Worker'))

from AI_Core_Worker.AI_Core_Worker import RealerAI

def main():
    print("🤖 R3AL3R AI - JARVIS MODE")
    print("=" * 40)
    print("Initializing voice-enabled AI assistant...")
    
    try:
        # Initialize AI with voice capabilities
        ai = RealerAI(enable_voice=True)
        
        print("\n✅ AI Core loaded")
        print("🎤 Voice interface ready")
        
        # Enable Jarvis Mode
        success = ai.enable_jarvis_mode()
        
        if success:
            print("🚀 JARVIS MODE ACTIVATED")
            print("\nVoice Commands:")
            print("  • 'realer system status' - Get system status")
            print("  • 'realer list files' - List current directory")
            print("  • 'realer git status' - Check git repository")
            print("  • 'realer disable jarvis mode' - Deactivate voice")
            print("\n🎯 Say 'realer' followed by your command...")
            print("Press Ctrl+C to exit\n")
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down Jarvis Mode...")
                ai.disable_jarvis_mode()
                print("Goodbye!")
        else:
            print("❌ Failed to activate Jarvis Mode")
            
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Run: pip install -r AI_Core_Worker/R3AL3RAI/requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()