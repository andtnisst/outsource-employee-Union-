
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'union-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///union.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    employer = db.Column(db.String(100))
    outsourcing_type = db.Column(db.String(100))

class Grievance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    details = db.Column(db.Text)
    document = db.Column(db.String(200))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/membership", methods=["GET", "POST"])
def membership():
    if request.method == "POST":
        new_member = Member(
            name=request.form['name'],
            contact=request.form['contact'],
            employer=request.form['employer'],
            outsourcing_type=request.form['outsourcing_type']
        )
        db.session.add(new_member)
        db.session.commit()
        flash("सदस्यता सफलतापूर्वक सबमिट की गई।")
        return redirect(url_for('membership'))
    return render_template("membership.html")

@app.route("/grievance", methods=["GET", "POST"])
def grievance():
    if request.method == "POST":
        file = request.files['document']
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        new_grievance = Grievance(
            type=request.form['type'],
            details=request.form['details'],
            document=filename
        )
        db.session.add(new_grievance)
        db.session.commit()
        flash("शिकायत दर्ज हो गई है।")
        return redirect(url_for('grievance'))
    return render_template("grievance.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
