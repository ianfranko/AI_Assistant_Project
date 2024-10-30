import pandas as pd

# Sample dataset for training the assistant
data = {
    'text': [
        'hello', 'hi', 'how are you', 'tell me a joke', 'what is your name', 
        'goodbye', 'bye', 'see you', 'who created you', 'define artificial intelligence'
    ],
    'intent': [
        'greeting', 'greeting', 'greeting', 'joke', 'personal_question', 
        'goodbye', 'goodbye', 'goodbye', 'creator_info', 'definition'
    ]
}

df = pd.DataFrame(data)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Vectorize the dataset
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])  # Transform text data to numerical format

# Define labels (intents)
y = df['intent']

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the classifier
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
import sqlite3

# Initialize SQLite Database
conn = sqlite3.connect('assistant_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (id INTEGER PRIMARY KEY, key TEXT, value TEXT)''')
conn.commit()
def classify_intent(user_input):
    """Predict the intent of user input using the trained model."""
    X_input = vectorizer.transform([user_input])
    prediction = classifier.predict(X_input)
    return prediction[0]

def respond_based_on_intent(intent):
    """Respond to the user based on the identified intent."""
    responses = {
        "greeting": "Hello! How can I assist you today?",
        "joke": "Why don’t scientists trust atoms? Because they make up everything!",
        "personal_question": "I am your assistant, here to help with whatever you need!",
        "goodbye": "Goodbye! Looking forward to our next chat.",
        "creator_info": "I was created by an amazing developer!",
        "definition": "Artificial Intelligence is the simulation of human intelligence in machines."
    }
    return responses.get(intent, "I'm not sure how to respond to that.")

def learn_from_user(user_input, response):
    """Store new user input and response in the database."""
    cursor.execute("INSERT INTO user_data (key, value) VALUES (?, ?)", (user_input, response))
    conn.commit()
    # Append new data to DataFrame and re-train model
    global df, X, y
    df = df.append({'text': user_input, 'intent': response}, ignore_index=True)
    X = vectorizer.fit_transform(df['text'])
    classifier.fit(X, df['intent'])
def main():
    print("Hello! I'm your AI assistant. Type 'exit' to end our chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Predict intent
        intent = classify_intent(user_input)
        response = respond_based_on_intent(intent)
        print(f"Assistant: {response}")
        
        # If no suitable response is found, learn from the user
        if response == "I'm not sure how to respond to that.":
            learn = input("Would you like to teach me how to respond to that? (yes/no) ")
            if learn.lower() == 'yes':
                value = input("What should I respond? ")
                learn_from_user(user_input, value)

if __name__ == "__main__":
    main()
import speech_recognition as sr

def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Could not request results from Google Speech Recognition service."

