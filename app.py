from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:12345@localhost:5432/todoapp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable = False, default = False)

    def __repr__(self):
        return f'<Todo id={self.id} description={self.description}>'

#db.create_all()


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all())

@app.route('/create', methods=['POST'])
def create():
    error = False
    #For debugging purpose only: Delete all items in the list: db.session.query(Todo).delete()
    new_description = (request.get_json())['description']
    try:
        todo = Todo(description=new_description)
        db.session.add(todo)
        db.session.commit()
        todoId = todo.id
    except:
        db.session.rollback()
        error = True
        print('error from server: ' + sys.exc_info())
    finally:
        db.session.close()
        if error:
            abort (400)
        else:
            return {'description' : new_description, 'completed' : False, 'id' : todoId}
            #return redirect(url_for('index'))

@app.route('/<item_id>/set-completed', methods=['POST'])
def set_completed(item_id):
    error = False
    new_completed = request.get_json()['completed']
    try:
        todo = Todo.query.get(item_id)
        todo.completed = new_completed
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print('error from server: ' + sys.exc_info())
    finally:
        db.session.close()
        if error:
            abort (400)
        else:
            return redirect(url_for('index'))

@app.route('/<item_id>/delete', methods=['POST'])
def delete(item_id):
    error = False
    try:
        todo = Todo.query.get(item_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print('error from server: ' + sys.exc_info())
    finally:
        db.session.close()
        if error:
            abort (400)
        else:
            return redirect(url_for('index'))
