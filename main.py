import json
from difflib import get_close_matches

# Function to load the knowledge base from a JSON file.
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Function to save the updated knowledge base to the JSON file.
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Function to find the best matching question in the knowledge base for the user's question.
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Function to retrieve the answer for a given question from the knowledge base.
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        
# Main chatbot function that handles user interaction and updates the knowledge base.
def chatbot():
    # Load the existing knowledge base from the file.
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    # Start an interaction loop.
    while True:
        user_input: str = input('You: ')

        # Check for the 'quit' command to exit the loop.
        if user_input.lower() == 'quit':
            break

        # Attempt to find the best match for the user's question in the knowledge base.
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            # If a matching question is found, provide the corresponding answer.
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            # If no match is found, ask the user to teach the chatbot the answer.
            print('Bot: I do not know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                # If the user provides an answer, add the new question-answer pair to the knowledge base.
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                # Save the updated knowledge base to the file.
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

# Ensure the chatbot function runs when the script is executed directly.
if __name__ == '__main__':
    chatbot()
