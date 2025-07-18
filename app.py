from flask import Flask
from db_config import get_connection

from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash

from flask import session
from werkzeug.security import check_password_hash

from flask import jsonify

app = Flask(__name__)

from functools import wraps
from flask import flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in first.")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        try:
            db = get_connection()
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
            db.commit()
            return render_template('registered.html')
        except Exception as e:
            return f"Error: {e}"

    return render_template('register.html')
app.secret_key = 'myfavsingerisarijitsingh'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            return render_template('logged_in.html', email=user['email'])
        else:
            return "Invalid email or password."

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quizzes")
    quizzes = cursor.fetchall()

    return render_template('index.html', quizzes=quizzes, email=session['email'])

@app.route('/confirm/<int:quiz_id>')
@login_required
def confirm_quiz(quiz_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quizzes WHERE id = %s", (quiz_id,))
    quiz = cursor.fetchone()

    if not quiz:
        return "Quiz not found."

    return render_template('confirm.html', quiz=quiz)    

@app.route('/quiz/<int:quiz_id>')
@login_required
def quiz(quiz_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM questions WHERE quiz_id = %s", (quiz_id,))
    questions = cursor.fetchall()

    if not questions:
        return "No questions found for this quiz."

    return render_template('quiz.html', questions=questions, quiz_id=quiz_id)

@app.route('/save-answer', methods=['POST'])
@login_required
def save_answer():
    data = request.get_json()
    user_id = session.get('user_id')
    quiz_id = data.get('quiz_id')
    question_id = data.get('question_id')
    selected_option = data.get('selected_option')

    if not user_id:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    # Get correct answer from DB
    cursor.execute("SELECT correct_ans FROM questions WHERE id = %s", (question_id,))
    result = cursor.fetchone()
    correct_answer = result['correct_ans']
    is_correct = (selected_option == correct_answer)

    # Check if already answered — update if yes, insert if no
    cursor.execute("""
        SELECT id FROM user_answers
        WHERE user_id = %s AND quiz_id = %s AND question_id = %s
    """, (user_id, quiz_id, question_id))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE user_answers SET selected_option = %s, is_correct = %s, timestamp = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (selected_option, is_correct, existing['id']))
    else:
        cursor.execute("""
            INSERT INTO user_answers (user_id, quiz_id, question_id, selected_option, is_correct)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, quiz_id, question_id, selected_option, is_correct))

    db.commit()
    return jsonify({'success': True})

@app.route('/submit/<int:quiz_id>', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    # Fetch total questions
    cursor.execute("SELECT COUNT(*) as total FROM questions WHERE quiz_id = %s", (quiz_id,))
    total_qs = cursor.fetchone()['total']

    # Fetch correct answers by user
    cursor.execute("""
        SELECT COUNT(*) as correct FROM user_answers 
        WHERE user_id = %s AND quiz_id = %s AND is_correct = TRUE
    """, (user_id, quiz_id))
    correct = cursor.fetchone()['correct']

    score = int((correct / total_qs) * 100) if total_qs > 0 else 0

    return render_template('result.html', total=total_qs, correct=correct, score=score)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)


