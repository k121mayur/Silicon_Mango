from flask import Flask, render_template, url_for, request, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, String, Boolean
import hashlib
from flask_migrate import Migrate
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

import io


def generate_identifier(name, mobile, batch="June 2024",  length=13):
    # Concatenate the input values
    input_str = f"{name}{batch}{mobile}"
    
    # Create a SHA-256 hash of the concatenated string
    hash_object = hashlib.sha256(input_str.encode())
    
    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()
    
    # Truncate or pad the hash to the desired length
    fixed_length_id = hex_dig[:length]
    
    return fixed_length_id




def generate_certificate(name, mobile, code):
    date = datetime.now().strftime("%d-%b-%Y")
    cert_path = "./static/certificate.jpg"
    cert = Image.open(cert_path)

    draw = ImageDraw.Draw(cert)
    font_path = "./static/TIMES.TTF"
    font = ImageFont.truetype(font_path, 300)

    draw.text((730, 2500), name, fill=(0, 0, 0), font=font)

    font = ImageFont.truetype(font_path, 150)
    draw.text((730, 1570), "20/07/2024", fill=(0, 0, 0), font=font)
    
    code = generate_identifier(name, mobile)

    font = ImageFont.truetype(font_path, 100)
    draw.text((5100, 4900), f"www.siliconmango.com/verify/{code}", fill=(0, 0, 238), font=font)

    img_io = io.BytesIO()
    cert.save(img_io, 'PNG')
    img_io.seek(0)  # Move the pointer to the beginning of the in-memory file

    return img_io

app = Flask(__name__)


# Set the path for the SQLite database inside the database directory
db_path = os.path.join(os.path.dirname(__file__), 'database', 'dev.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

base_dir = os.path.dirname(os.path.abspath(__file__))

class StudentDatabase(db.Model):
    __tablename__ = 'studentdatabase'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    mobile_number = Column(Integer, unique=True)
    city = Column(String)
    status = Column(Boolean, default=False)
    code = Column(String)








@app.route('/')
def index():
    return render_template('index.html')



@app.route('/verify/<string:code>')
def verify(code):
    if len(code) != 13 :
        return "Invalid code Try again"
    else:
        data = db.session.query(StudentDatabase).filter_by(code=code).first()
        if data is None:
            return render_template('verify.html', data={'entry': False})
        else:
            return render_template('verify.html', data={'entry': True, "name": data.first_name + " " + data.last_name, "batch": "June 2024", "course": "Excel Mastery Course for Beginners", "code": code})

@app.route('/certificate', methods=['POST', 'GET'])
def certificate():
    global base_dir
    if request.method == 'POST':
        email = request.form['email']
        details = db.session.query(StudentDatabase).filter_by(email=email).first()
        if details is None:
            return "It seems that you have not completed the course. Please complete all the quizzes and assignments and try again. Thank you!"
        else:
            file_name = f"{details.first_name} {details.last_name}.png"
            # file_path = os.path.join(base_dir, 'static', 'generated_certificate', file_name)
            code = generate_identifier(name=details.first_name + " " + details.last_name, batch="June 2024", mobile=details.mobile_number)
        
            certificate = generate_certificate(name=details.first_name + " " + details.last_name, mobile=details.mobile_number, code=code)
            
            # file_name = f"{details.first_name} {details.last_name}.png"
            # file_path = os.path.join(base_dir, 'static', 'generated_certificate', file_name)

            
            # return send_file(file_path, as_attachment=True)
            return send_file(certificate, mimetype='image/png', as_attachment=True, download_name=f"{file_name}")
    if request.method == 'GET':
        return render_template('get_certificate.html')
        

@app.route("/createAll")
def createAll():
    all_data = db.session.query(StudentDatabase).all()
    for data in all_data:
        code = generate_identifier(data.first_name  + " " + data.last_name, data.mobile_number)
        data.code = code
        db.session.commit()
    return "Done"


# Ensure the application context is pushed
with app.app_context():
    db.create_all()




if __name__ == '__main__':
    app.run()
    
    
