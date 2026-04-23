def is_safe_prompt(prompt):
    blocked = ["ignore previous instructions", "hack", "delete", "shutdown"]
    return not any(word in prompt.lower() for word in blocked)