import json
import nltk
from nltk.metrics import edit_distance
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# Load the knowledge base from a JSON file
with open("knowledge_base.json", "r") as kb_file:
    knowledge_base = json.load(kb_file)

# Initialize NLTK's WordNet
nltk.download("wordnet")
nltk.download("punkt")
wnl = nltk.WordNetLemmatizer()

# Initialize the chatbot
def initialize_chat():
    add_message("Chatbot: Hi! I'm CECbot. Ask me anything or press Enter to quit.", is_bot=True)

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
            matches.append(answer)

    return matches

# Function to add chat bubble messages to the chat history
def add_message(message, is_bot=False):
    timestamp = datetime.now().strftime("%H:%M")
    chat_frame = tk.Frame(chat_history_frame, bg="white")
    chat_frame.pack(anchor="w" if is_bot else "e", padx=10, pady=5)
    chat_bubble = create_chat_bubble(chat_frame, message, is_bot)
    chat_bubble.pack(fill="both", expand=True)
    timestamp_label = tk.Label(chat_frame, text=timestamp, font=("Helvetica", 8), fg="gray")
    timestamp_label.pack(side="left" if is_bot else "right")
    chat_history_canvas.configure(scrollregion=chat_history_canvas.bbox("all"))

# Function to create chat bubble with rounded corners
def create_chat_bubble(parent, message, is_bot=False):
    bg_color = "lightblue" if is_bot else "lightgreen"
    fg_color = "black" if is_bot else "black"
    corner_radius = 20  # Adjust the corner radius as needed

    bubble = tk.Label(parent, text=message, bg=bg_color, fg=fg_color, wraplength=250, justify="left",
                     padx=10, pady=5, relief=tk.SOLID, borderwidth=1, anchor="w" if not is_bot else "e")
    bubble.config(font=("Helvetica", 10))
    bubble.bind("<Configure>", lambda e: bubble.config(wraplength=e.width - 10))

    return bubble

# Function to handle user input
def handle_user_input(event=None):
    user_input = user_input_text.get("1.0", tk.END).strip()

    if user_input.lower() == "exit":
        add_message("Goodbye!", is_bot=True)
        window.quit()
    else:
        add_message(user_input, is_bot=False)
        matching_answers = find_nearest_matches(user_input)
        if not matching_answers:
            add_message("I'm sorry, I don't have a close match for that.", is_bot=True)
        else:
            for answer in matching_answers:
                add_message(answer, is_bot=True)
        chat_history_canvas.yview_moveto(1.0)  # Auto-scroll to the bottom of the chat history
    user_input_text.delete("0.0", tk.END)

# Create the GUI window
window = tk.Tk()
window.title("CECbot")
window.geometry("400x600")  # Adjusted window size

# Create a chat history display with chat bubbles
chat_history = tk.Frame(window, bg="white")
chat_history.pack(fill="both", expand=True)
chat_history_canvas = tk.Canvas(chat_history, bg="white")
chat_history_canvas.pack(side="left", fill="both", expand=True)
chat_history_scrollbar = tk.Scrollbar(chat_history, command=chat_history_canvas.yview)
chat_history_scrollbar.pack(side="right", fill="y")
chat_history_canvas.configure(yscrollcommand=chat_history_scrollbar.set)
chat_history_frame = tk.Frame(chat_history_canvas, bg="white")
chat_history_canvas.create_window((0, 0), window=chat_history_frame, anchor="nw")

# Create a text input field with proper styling
user_input_text = tk.Text(window, height=3, width=40)
user_input_text.pack()

# Bind the Enter key to the handle_user_input function
user_input_text.bind("<Return>", handle_user_input)

# Create a "Send" button with proper styling
send_button = tk.Button(window, text="Send", command=handle_user_input)
send_button.pack()

# Initialize the chat
initialize_chat()

# Start the GUI event loop
window.mainloop()
