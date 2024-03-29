#trivia quiz game
#practise on inserting questions to the database

import sqlite3
import requests

# Creating a function to initialize the database and populate it with sample data
def initialize_database():
    # Connecting to the database
    conn = sqlite3.connect('data.sqlite')
    #createing a cursor object (c) 
    c = conn.cursor()

    # Creating tables if they don't exist

    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY,
                    category_id INTEGER,
                    question TEXT,
                    answer TEXT,
                    FOREIGN KEY(category_id) REFERENCES categories(id))''')

    # Committing changes and close connection
    conn.commit()
    conn.close()

# creating a function to fetch questions from the Open Trivia Database API
def fetch_questions(amount=10, category=9, difficulty='easy', type='multiple'):
    # Constructing the URL for the API request
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type={type}"

    # Sending a  GET request to the API and parse the JSON response
    response = requests.get(url)
    #Extracting JSON data
    data = response.json()

    # Extracting and returning the results from the response, or an empty list if there are no results
    return data.get('results', [])

# creating a function to insert fetched questions into the database
def insert_questions(questions):
    # Connect to the database
    conn = sqlite3.connect('data.sqlite')
    c = conn.cursor()

    # Iterating over each fetched question and inserting it into the database
    for q in questions:
        category = q['category']
        question = q['question']
        answer = q['correct_answer']

        c.execute('INSERT INTO questions (category_id, question, answer) VALUES (?, ?, ?)', (category, question, answer))

    # Committing changes and close connection
    conn.commit()
    conn.close()

# Initializing the database schema
initialize_database()
#Fetching 10 questions from the API
new_questions = fetch_questions(amount=10)
# Inserting fetched questions into the database 
insert_questions(new_questions)  
print("Questions are added to 'trivia.db' can check by connecting it to SQlite studio APP.")
