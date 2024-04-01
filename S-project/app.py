# Importing  necessary modules
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import requests
import os

# Creating Flask application instance
app = Flask(__name__)
#Secret key
app.secret_key = os.urandom(24)

# Function to initialize the database and populate it with initial data

def initialize_database():
    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()

    # Creating  tables if not exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    email TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY,
                    category_id INTEGER,
                    question TEXT,
                    answer TEXT,
                    FOREIGN KEY(category_id) REFERENCES categories(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    score INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')

    # Inserting initial data into categories table
    c.execute("INSERT INTO categories (name) VALUES ('General Knowledge')")
    c.execute("INSERT INTO categories (name) VALUES ('Science')")
    c.execute("INSERT INTO categories (name) VALUES ('History')")
    c.execute("INSERT INTO categories (name) VALUES ('Sports')")
    # Add more categories as needed

    conn.commit()
    conn.close()

# creating a function to fetch questions from the Open Trivia Database API
    
def fetch_questions(amount=10, category=9, difficulty='easy', type='multiple'):
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type={type}"
    response = requests.get(url)
    data = response.json()
    return data.get('results', [])

# creating a function to insert fetched questions into the database

def insert_questions(questions):
    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()

    # Inserting each question into the database
    for q in questions:
        category = q['category']
        question = q['question']
        answer = q['correct_answer']

        c.execute('INSERT INTO questions (category_id, question, answer) VALUES (?, ?, ?)', (category, question, answer))

    conn.commit()
    conn.close()

# Initializing the database and populate it with initial data
initialize_database()

# Fetching questions from the API and insert them into the database
questions = fetch_questions(amount=10)
insert_questions(questions)

# creating a function to display quiz questions
@app.route('/quiz')
def display_quiz():

    # Checking if user is logged in

    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetching questions from the database

    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()

    c.execute("SELECT * FROM questions")
    questions = c.fetchall()

    conn.close()

    return render_template('quiz.html', questions=questions)

# creating a function to handle answer submission

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    # Checking if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieving submitted answer and question id

    user_answer = request.form['answer']
    question_id = request.form['question_id']

    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()

    # Retrieving correct answer from the database

    c.execute("SELECT answer FROM questions WHERE id=?", (question_id,))
    correct_answer = c.fetchone()[0]

    # Comparing user answer with correct answer

    if user_answer.lower() == correct_answer.lower():
        flash('Correct!', 'success')
    else:
        flash('Incorrect!', 'danger')

    conn.close()

    return redirect(url_for('display_quiz'))

# creating a function to display leaderboard

@app.route('/leaderboard')
def display_leaderboard():

    # Checking  if user is logged in

    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetching  leaderboard data from the database

    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()

    c.execute("SELECT username, score FROM users JOIN scores ON users.id = scores.user_id ORDER BY score DESC")
    leaderboard = c.fetchall()

    conn.close()

    return render_template('leaderboard.html', leaderboard=leaderboard)

# Creating a function to handle user login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('trivia.db')
        c = conn.cursor()

        # Checking if user credentials are valid

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        conn.close()

        # If user exists, log them in
        if user:
            session['username'] = username
            flash('You have been logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

# creating a function to handle user registration

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        conn = sqlite3.connect('trivia.db')
        c = conn.cursor()

        #Inserting new user into the database

        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()

        conn.close()

        flash('You have been registered successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Creating a function to display user dashboard

@app.route('/dashboard')
def dashboard():
    # Checking if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetching categories and user score from the database

    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()

    c.execute("SELECT * FROM categories")
    categories = c.fetchall()

    c.execute("SELECT score FROM scores WHERE user_id=(SELECT id FROM users WHERE username=?)", (session['username'],))
    user_score = c.fetchone()

    conn.close()

    return render_template('dashboard.html', categories=categories, user_score=user_score)

# creating a function to handle user logout

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))

# Creating a function to display quiz categories and allow users to choose a category

@app.route('/categories')
def display_categories():
    # Checking if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetching categories from the database

    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()
    c.execute("SELECT * FROM categories")
    categories = c.fetchall()
    conn.close()

    return render_template('categories.html', categories=categories)

# creating a function to handle quiz submission
@app.route('/submit', methods=['GET', 'POST'])
def submit_quiz():

    # Checking  if user is logged in

    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        # quiz submission

        pass  # Placeholder for  submission logic

    # Rendering the submit page

    return render_template('submit.html')
 
# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)  
