from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:12345@localhost:5432/todoapp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo id={self.id} description={self.description}>'

db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/create', methods=['POST'])
def create():
    new_description = request.form.get('description')
    db.session.add(Todo(description=new_description))
    db.session.commit()
    return redirect(url_for('index'))