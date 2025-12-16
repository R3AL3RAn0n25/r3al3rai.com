#!/usr/bin/env python3
"""
Test script for NeMo Canary ASR integration
"""
import nemo.collections.asr as nemo_asr
import tempfile
import soundfile as sf
import numpy as np

def test_nemo_asr():
    """Test NeMo Canary ASR model"""
    try:
        print("Loading NeMo Canary ASR model...")
        asr_model = nemo_asr.models.ASRModel.from_pretrained("nvidia/canary-1b-v2")
        print("✓ NeMo model loaded successfully!")
        
        # Create a simple test audio (silence)
        test_audio = np.zeros(16000, dtype=np.float32)  # 1 second of silence
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            sf.write(tmp_file.name, test_audio, 16000)
            transcriptions = asr_model.transcribe([tmp_file.name])
            print(f"✓ Test transcription completed: '{transcriptions[0]}'")
            
        return True
        
    except Exception as e:
        print(f"✗ NeMo ASR test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing NeMo Canary ASR integration...")
    success = test_nemo_asr()
    if success:
        print("\n🎉 NeMo integration is ready!")
    else:
        print("\n❌ NeMo integration needs attention")