from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class School(db.Model):
    __tablename__ = 'school'

    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    students = db.relationship('Student', backref='school')
    notices = db.relationship('Notice', backref='school')
    resources = db.relationship('Resource', backref='school')


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    student_uid = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(20), nullable=False)

    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    marks = db.relationship('Marks', backref='student')


class Notice(db.Model):
    __tablename__ = 'notice'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)

    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)


class Marks(db.Model):
    __tablename__ = 'marks'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)



@app.route("/")
def Home():
    return render_template("login.html")

@app.route("/newschool")
def newSchool():
    return render_template("new.html")

@app.route("/addschool",methods=["POST","GET"]) #C
def addSchool():
    if request.method=="POST":
        id = request.form["Sid"]
        name = request.form["Sname"]
        email = request.form["email"]
        password = request.form["password"]
        cpassword = request.form["cpassword"]

        if password != cpassword:
            return redirect("/newschool")
        
        
        db.session.add(School(id=id,school_name=name,email=email,password=password))
        db.session.commit()
        return render_template("success.html")


@app.route("/school")
def dashboardSchool():
    return render_template("school/dashboard.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)