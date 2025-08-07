def generate_follow_up(answer):
    answer = answer.lower()

    if any(word in answer for word in ["student", "college", "school"]):
        return "What are you studying right now?"
    elif any(word in answer for word in ["unemployed", "looking", "jobless"]):
        return "What challenges are you facing in getting a job?"
    elif any(word in answer for word in ["doctor", "engineer", "teacher"]):
        return f"How long have you been working as a {answer}?"
    elif "yes" in answer:
        return "Can you explain why?"
    elif "no" in answer:
        return "Can you share the reason for that?"
    else:
        return "Thanks! Would you like to elaborate more?"
