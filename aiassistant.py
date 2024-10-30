import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Step 2: Prepare Data
data = {
    'text': ['hello', 'hi', 'how are you', 'tell me a joke', 'what is your name', 
             'goodbye', 'bye', 'see you', 'who created you', 'define artificial intelligence'],
    'intent': ['greeting', 'greeting', 'greeting', 'joke', 'personal_question', 
               'goodbye', 'goodbye', 'goodbye', 'creator_info', 'definition']
}
df = pd.DataFrame(data)

# Step 3: Train Model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['intent']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
classifier = LogisticRegression()
classifier.fit(X_train, y_train)

# Step 4: Set Up Database
conn = sqlite3.connect('assistant_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (id INTEGER PRIMARY KEY, key TEXT, value TEXT)''')
conn.commit()\
# Functions
def classify_intent(user_input):
    X_input = vectorizer.transform([user_input])
    return classifier.predict(X_input)[0]

def respond_based_on_intent(intent):
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
    cursor.execute("INSERT INTO user_data (key, value) VALUES (?, ?)", (user_input, response))
    conn.commit()
    global df, X, y
    df = df.append({'text': user_input, 'intent': response}, ignore_index=True)
    X = vectorizer.fit_transform(df['text'])
    classifier.fit(X, df['intent'])

# Main Loop
def main():
    print("Hello! I'm your AI assistant. Type 'exit' to end our chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        intent = classify_intent(user_input)
        response = respond_based_on_intent(intent)
        print(f"Assistant: {response}")
        
        if response == "I'm not sure how to respond to that.":
            learn = input("Would you like to teach me how to respond to that? (yes/no) ")
            if learn.lower() == 'yes':
                value = input("What should I respond? ")
                learn_from_user(user_input, value)

if __name__ == "__main__":
    main()
