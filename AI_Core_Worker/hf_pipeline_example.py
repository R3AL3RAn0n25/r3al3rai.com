"""
Minimal Hugging Face pipeline example for text-generation using OpenThinker-7B.

Warning: `open-thoughts/OpenThinker-7B` is a large 7B parameter model and
downloading it can take many GB of disk/RAM. This script demonstrates the
API usage and will fallback to a tiny model if the primary model isn't available
or if `USE_SMALL_MODEL=1` is set in the environment.
"""
import os
from typing import Any

def run_demo() -> Any:
    try:
        from transformers import pipeline
    except Exception as e:
        print("Transformers not installed. Install with: pip install transformers accelerate safetensors")
        return None

    prefer_small = os.getenv("USE_SMALL_MODEL", "0") == "1"
    model_id = "open-thoughts/OpenThinker-7B"
    if prefer_small:
        model_id = "sshleifer/tiny-gpt2"  # fast demo

    print(f"Loading pipeline with model: {model_id}")
    try:
        pipe = pipeline("text-generation", model=model_id)
    except Exception as e:
        print(f"Failed to load {model_id}: {e}")
        print("Falling back to tiny-gpt2 for demonstration.")
        pipe = pipeline("text-generation", model="sshleifer/tiny-gpt2")

    # Chat-style input using messages array
    messages = [
        {"role": "user", "content": "Who are you?"},
    ]

    print("Running generation...")
    try:
        out = pipe(messages)
        print(out)
        return out
    except TypeError:
        # Some pipelines expect raw strings rather than chat messages
        print("Pipeline didn't accept messages; trying with prompt text...")
        prompt = "User: Who are you?\nAssistant:"
        out = pipe(prompt, max_new_tokens=64)
        print(out)
        return out


if __name__ == "__main__":
    run_demo()
