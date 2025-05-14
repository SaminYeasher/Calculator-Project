# cgpa_calculator_app.py

import utils.transport
import utils.session
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define courses per program with editable credits
PROGRAM_COURSES = {
    'CSE': [
        {'code': 'CSE 111', 'title': 'Computer Fundamentals', 'credit': 3},
        {'code': 'CSE 112', 'title': 'Programming Lab', 'credit': 1.5},
        {'code': 'AA 099', 'title': 'Academic Reading and Writing', 'credit': 3},
    ],
    'EEE': [
        {'code': 'EEE 101', 'title': 'Basic Electrical Engineering', 'credit': 3},
        {'code': 'EEE 102', 'title': 'Electrical Lab', 'credit': 1.5},
        {'code': 'EEE 001', 'title': 'Non-Credit Course', 'credit': 3},
    ],
    'BBA': [
        {'code': 'BBA 101', 'title': 'Principles of Management', 'credit': 3},
        {'code': 'BBA 102', 'title': 'Intro to Business', 'credit': 3},
        {'code': 'BBA 099', 'title': 'English Foundation', 'credit': 3},
    ]
}

NON_CREDIT_COURSES = {
    'CSE': ['AA 099'],
    'EEE': ['EEE 001'],
    'BBA': ['BBA 099']
}

@app.route('/')
def home():
    return render_template('program_select.html', programs=PROGRAM_COURSES.keys())

@app.route('/courses', methods=['POST'])
def courses():
    program = request.form['program']
    courses = PROGRAM_COURSES.get(program, [])
    return render_template('courses.html', program=program, courses=courses)

@app.route('/calculate', methods=['POST'])
def calculate():
    program = request.form['program']
    excluded_courses = NON_CREDIT_COURSES.get(program, [])

    total_credit = 0.0
    total_weighted_gp = 0.0

    course_codes = request.form.getlist('course_code')
    credits = list(map(float, request.form.getlist('credit')))
    gps = list(map(float, request.form.getlist('gp')))

    for code, credit, gp in zip(course_codes, credits, gps):
        if code not in excluded_courses:
            total_credit += credit
            total_weighted_gp += credit * gp

    cgpa = total_weighted_gp / total_credit if total_credit > 0 else 0.0
    return render_template('result.html', cgpa=round(cgpa, 2))

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

if __name__ == '__main__':
    app.run(debug=True)
