def process_input(user_text: str) -> str:
    # THIS IS WHERE YOUR REAL SELF-EVOLVING ENGINE LIVES
    # For now just echo + a little personality
    responses = [
        "On it, boss.",
        "Consider it done.",
        "Working my magic...",
        "Right away."
    ]
    import random
    return random.choice(responses) + f" You said: {user_text}"