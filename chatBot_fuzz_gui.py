import tkinter as tk
from tkinter import Scrollbar, simpledialog
from fuzzywuzzy import fuzz
import json

# Load the knowledge base from a JSON file
with open("knowledge_base.json", "r") as kb_file:
    knowledge_base = json.load(kb_file)

# Define a global variable to store matching questions
matching_questions = []

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

# Function to handle user input
def handle_user_input(event=None):
    user_input = user_input_entry.get()
    
    if user_input.lower() == "exit":
        add_message("You", user_input)
        add_message("Chatbot", "Goodbye!")
        root.after(50, root.destroy)  # Close the window after a 2-second delay
    else:
        add_message("You", user_input)
        
        global matching_questions  # Use the global variable
        matching_questions = find_nearest_matches(user_input)
        
        if not matching_questions:
            add_message("Chatbot", "I'm sorry, I don't have a close match for that.")
        elif len(matching_questions) == 1:
            question, answer = matching_questions[0]
            add_message("Chatbot", answer)
        else:
            add_message("Chatbot", "I found multiple potential matches. Please select one:")
            options = [f"{i}. {question}" for i, (question, _) in enumerate(matching_questions, start=1)]
            for option in options:
                add_message("Chatbot", option)
            root.after(000, show_dialog)  # Add delay before showing the dialog

        user_input_entry.delete(0, tk.END)

# Function to add a message to the chat history
def add_message(sender, message):
    chat_history_text.config(state=tk.NORMAL)
    if sender == "You":
        chat_history_text.insert(tk.END, f"You: {message}\n", "user_message")
    elif sender == "Chatbot":
        chat_history_text.insert(tk.END, f"Chatbot: {message}\n", "chatbot_message")
    chat_history_text.see(tk.END)  # Scroll to the end of the chat history
    chat_history_text.config(state=tk.DISABLED)

# Function to show the dialog
def show_dialog():
    selected_index = simpledialog.askinteger("Select Option", "Choose an option:", initialvalue=1, minvalue=1, maxvalue=len(matching_questions))
    if selected_index is not None:
        question, answer = matching_questions[selected_index - 1]
        add_message("Chatbot", answer)
    else:
        add_message("Chatbot", "Invalid choice. Please enter a valid number.")

# Create the main GUI window
root = tk.Tk()
root.title("CECbot Chatbot")

# Create a text area for chat history with chat bubble styling and a scrollbar
chat_history_frame = tk.Frame(root)
chat_history_frame.pack(fill=tk.BOTH, expand=True)
chat_history_text = tk.Text(chat_history_frame, wrap=tk.WORD, width=80, height=30, font=("Helvetica", 12))
chat_history_text.tag_configure("user_message", justify='left', foreground='green')
chat_history_text.tag_configure("chatbot_message", justify='left', foreground='blue')
chat_history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = Scrollbar(chat_history_frame, command=chat_history_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history_text.config(yscrollcommand=scrollbar.set)
chat_history_text.config(state=tk.DISABLED)

# Create an entry for user input
user_input_entry = tk.Entry(root, width=40, font=("Helvetica", 12))
user_input_entry.bind('<Return>', handle_user_input)
user_input_entry.pack()

# Create a "Send" button for user input
send_button = tk.Button(root, text="Send", command=handle_user_input)
send_button.pack()

# Display the initial welcome message
add_message("Chatbot", "Hi! I'm CECbot. Ask me anything or type 'exit' to quit.")

root.mainloop()
