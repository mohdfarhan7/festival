from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load festival data
def load_festival_data():
    try:
        with open('data/festivals.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: festivals.json file not found")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in festivals.json")
        return {}

# Timer management
def init_timer():
    session['start_time'] = datetime.now().timestamp()
    session['time_left'] = 600  # 10 minutes in seconds

def update_timer():
    if 'start_time' in session:
        elapsed = datetime.now().timestamp() - session['start_time']
        session['time_left'] = max(0, 600 - elapsed)

@app.route('/')
def index():
    # Clear any existing session data
    session.clear()
    return render_template('index.html')

@app.route('/home')
def home():
    festivals = load_festival_data()
    if not festivals:
        return render_template('error.html', message="Unable to load festival data")
    return render_template('home.html', festivals=festivals)

@app.route('/learn/<festival_id>')
def learn(festival_id):
    festivals = load_festival_data()
    festival = festivals.get(festival_id)
    if not festival:
        return redirect(url_for('home'))
    return render_template('learn.html', festival=festival, festival_id=festival_id)

@app.route('/save_answer', methods=['POST'])
def save_answer():
    data = request.get_json()
    question_index = data.get('question_index')
    answer = data.get('answer')
    
    if 'selected_answers' not in session:
        session['selected_answers'] = {}
    
    session['selected_answers'][question_index] = answer
    session.modified = True
    return jsonify({'status': 'success'})

@app.route('/quiz/<festival_id>', methods=['GET', 'POST'])
def quiz(festival_id):
    festivals = load_festival_data()
    festival = festivals.get(festival_id)
    
    if not festival:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        form_data = request.form.to_dict()
        answers = []
        for i in range(len(festival['quiz'])):
            answer = form_data.get(f'answer_{i}', '')
            answers.append(answer)
        
        correct_answers = [q['answer'] for q in festival['quiz']]
        score = sum(1 for a, c in zip(answers, correct_answers) if a == c)
        session[f'quiz_{festival_id}_score'] = score
        session[f'quiz_{festival_id}_answers'] = answers
        session.pop('selected_answers', None)  # Clear saved answers after submission
        return redirect(url_for('result', festival_id=festival_id))
    
    return render_template('quiz.html', festival=festival, festival_id=festival_id)

@app.route('/result/<festival_id>')
def result(festival_id):
    festivals = load_festival_data()
    festival = festivals.get(festival_id)
    
    if not festival:
        return redirect(url_for('home'))
    
    score = session.get(f'quiz_{festival_id}_score', 0)
    answers = session.get(f'quiz_{festival_id}_answers', [])
    
    if not answers:
        return redirect(url_for('quiz', festival_id=festival_id))
    
    return render_template('result.html', festival=festival, score=score, answers=answers)

@app.route('/quiz/all', methods=['GET', 'POST'])
def all_quiz():
    festivals = load_festival_data()
    
    if request.method == 'POST':
        all_questions = session.get('all_quiz_questions', [])
        form_data = request.form.to_dict()
        answers = []
        for i in range(len(all_questions)):
            answer = form_data.get(f'answer_{i}', '')
            answers.append(answer)
            
        correct_answers = [q['answer'] for q in all_questions]
        score = sum(1 for a, c in zip(answers, correct_answers) if a == c)
        session['all_quiz_score'] = score
        session['all_quiz_answers'] = answers
        # session['all_quiz_questions'] = all_questions  # already stored
        session.pop('selected_answers', None)  # Clear saved answers after submission
        return redirect(url_for('all_result'))
    
    # Get questions from each festival and combine them
    all_questions = []
    for fest in festivals.values():
        all_questions.extend(fest['quiz'])
    
    # Shuffle the questions to randomize the order
    random.shuffle(all_questions)
    session['all_quiz_questions'] = all_questions
    
    return render_template('all_quiz.html', questions=all_questions)

@app.route('/result/all')
def all_result():
    questions = session.get('all_quiz_questions', [])
    score = session.get('all_quiz_score', 0)
    answers = session.get('all_quiz_answers', [])
    
    if not questions or not answers:
        return redirect(url_for('all_quiz'))
    
    return render_template('all_result.html', 
                         questions=questions,
                         score=score,
                         answers=answers,
                         total_questions=len(questions))

@app.route('/api/timer')
def get_timer():
    update_timer()
    return jsonify({'time_left': session.get('time_left', 600)})

@app.route('/api/init_timer', methods=['POST'])
def init_timer_api():
    init_timer()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True) 