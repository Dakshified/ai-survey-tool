def generate_follow_up(answer):
    answer = answer.lower()
    if "unemployed" in answer:
        return "What challenges are you facing in finding a job?"
    elif "student" in answer:
        return "What course are you currently pursuing?"
    elif "yes" in answer:
        return "Can you elaborate a bit more?"
    else:
        return "Thank you. Would you like to provide more details?"
