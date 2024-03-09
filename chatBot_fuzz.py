from fuzzywuzzy import fuzz
import json

# Load the knowledge base from a JSON file
with open("knowledge_base.json", "r") as kb_file:
    knowledge_base = json.load(kb_file)

# Define a function to find the nearest matches in the knowledge base
def find_nearest_matches(query):
    matches = []
    for entry in knowledge_base:
        question = entry["question"]
        answer = entry["answer"]
        keywords = entry["keywords"]
        
        # Check if the user query is an exact match to any keyword
        if query.lower() in [kw.lower() for kw in keywords]:
            matches.append((question, answer))
        else:
            # Calculate token set ratio similarity
            similarity = fuzz.token_set_ratio(query, question)
            if similarity >= 60:  # Adjust the similarity threshold as needed
                matches.append((question, answer))
    
    return matches

# Main chatbot loop
print("Chatbot: Hi! I'm CECbot. Ask me anything or type 'exit' to quit.")
while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    
    matching_questions = find_nearest_matches(user_input)
    
    if not matching_questions:
        print("Chatbot: I'm sorry, I don't have a close match for that.")
    elif len(matching_questions) == 1:
        question, answer = matching_questions[0]
        print("Chatbot:", answer)
    else:
        print("Chatbot: I found multiple potential matches. Please select one by entering the corresponding number:")
        for i, (question, _) in enumerate(matching_questions, start=1):
            print(f"{i}. {question}")
        
        choice = input("Your choice: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(matching_questions):
                question, answer = matching_questions[choice - 1]
                print("Chatbot:", answer)
            else:
                print("Chatbot: Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Chatbot: Invalid choice. Please enter a valid number.")