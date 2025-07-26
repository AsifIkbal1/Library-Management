from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'admin123'

students = []
books = []
issued_books = []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '12345':
        session['user'] = username
        return redirect('/dashboard')
    return 'Invalid credentials'

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    now = datetime.now()
    return render_template('dashboard.html', time=now)

@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        students.append(request.form.to_dict())
        return redirect('/dashboard')
    return render_template('create_student.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        books.append(request.form.to_dict())
        return redirect('/dashboard')
    return render_template('add_book.html')

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        data = request.form.to_dict()
        data['issue_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        issued_books.append(data)
        return redirect('/dashboard')
    return render_template('issue_book.html', students=students, books=books)

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        data = request.form.to_dict()
        data['return_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        issued_books.append(data)
        return redirect('/dashboard')
    return render_template('return_book.html', students=students, books=books)

@app.route('/list')
def show_list():
    if 'user' not in session:
        return redirect('/')
    return render_template('list.html', students=students, books=books, issued=issued_books)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
