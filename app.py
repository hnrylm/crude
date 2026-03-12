from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

# Helper: Load tasks from the JSON file
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Helper: Save tasks to the JSON file
def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    content = request.form.get('content')
    priority = request.form.get('priority')
    
    if content:
        tasks = load_tasks()
        # The "Smart" part: Adding priority and status
        tasks.append({'content': content, 'priority': priority, 'done': False})
        save_tasks(tasks)
    
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id) # Remove the task at that index
        save_tasks(tasks)
    return redirect('/')

