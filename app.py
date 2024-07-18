from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, String

app = Flask(__name__)

# Set the path for the SQLite database inside the database directory
db_path = os.path.join(os.path.dirname(__file__), 'database', 'dev.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class StudentDatabase(db.Model):
    __tablename__ = 'studentdatabase'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    mobile_number = Column(Integer, unique=True)
    city = Column(String)
    code = Column(String)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify/<string:code>')
def verify(code):
    data = db.session.query(StudentDatabase).filter_by(code=code).first()
    return render_template('verify.html', data={'entry': True, "name": data.first_name, "batch": "June 2024", "course": "Excel", "code": code})

# Ensure the application context is pushed
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
