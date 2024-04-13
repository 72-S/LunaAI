def parse_commands(prompt):
    if prompt == "/start":
        return False, "Hello, I am a chatbot. How can I help you today?"
    elif prompt == "/help":
        return False, "I am a chatbot. You can ask me anything you want."
    else:
        return True, prompt
