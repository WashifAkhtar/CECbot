import json
import nltk
from nltk.corpus import wordnet
from nltk.metrics import edit_distance

# Load the knowledge base from a JSON file
with open("knowledge_base.json", "r") as kb_file:
    knowledge_base = json.load(kb_file)

# Initialize NLTK's WordNet
nltk.download("wordnet")
nltk.download("punkt")
wnl = nltk.WordNetLemmatizer()

# Define a function to find the nearest matches in the knowledge base
def find_nearest_matches(query):
    matches = []
    query = wnl.lemmatize(query.lower())  # Lemmatize and lowercase the query

    for entry in knowledge_base:
        question = entry["question"]
        answer = entry["answer"]
        keywords = entry.get("keywords", [])
        question = wnl.lemmatize(question.lower())  # Lemmatize and lowercase the question

        # Calculate similarity using NLTK's edit_distance
        similarity_nltk = 1 / (1 + edit_distance(query, question))

        # Match based on keywords
        keyword_match = any(keyword in query for keyword in keywords)

        # You can adjust the thresholds as needed
        if similarity_nltk > 0.8 or keyword_match:
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
