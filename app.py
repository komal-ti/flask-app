from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Flask app initialization
app = Flask(__name__)

# Base directory and database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'todo.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Database model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} (Created: {self.date_created})"

# Home route with form handling
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title.strip():  # Simple validation for title
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

# About route
@app.route("/about")
def about():
    return render_template('about.html')

# Update route
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get(sno)  # Fetch by primary key
    if not todo:
        return "Todo not found!", 404

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/")
    return render_template('update.html', todo=todo)

# Delete route
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get(sno)
    if not todo:
        return "Todo not found!", 404

    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Main function with database creation
if __name__ == "__main__":
    try:
        # Ensure database is created before running the app
        with app.app_context():
            db.create_all()
            print("Database created successfully.")
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting the application: {e}")






