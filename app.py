from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html ', tasks = tasks)

@app.route('/create', methods=['POST'])
def crete():
    content = request.form['content']
    if len(content):
        task = Task(content = request.form['content'], done=False)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))
    else: 
        e = "error"
        mail(e)
        abort(500)


@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<id>')
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

def mail(msg):
    message = msg
    subject = "Excepcion encontrada"

    message = 'Subject: {}\n\n{}'.format(subject, message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('hramonbf@gmail.com', 'clzqmbayjodeslci')

    server.sendmail('hramonbf@gmail.com', 'hbarruetaf97@gmail.com', message)

    server.quit()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=argv[1])