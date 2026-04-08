conversation_history = []

def add_to_memory(question, answer):
    conversation_history.append({
        "question": question,
        "answer": answer
    })

def get_memory():
    return conversation_history[-3:]