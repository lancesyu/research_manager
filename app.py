from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Notecard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.String(1000),nullable=False)
    tag = db.Column(db.String(20),nullable=False)

def __repr__(self):
    return '<Notecard %r>' %self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        notecard_title = request.form['title']
        notecard_content = request.form['content']
        notecard_tag = request.form['tag']
        new_notecard = Notecard(title=notecard_title,content=notecard_content,tag=notecard_tag)
        try:
            db.session.add(new_notecard)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the notecard'
    else:
        notecards = Notecard.query.order_by(Notecard.title).all()

        return render_template('index.html', notecards=notecards)
    
@app.route('/delete/<int:id>')
def delete(id):
    notecard_to_delete = Notecard.query.get_or_404(id)
    try:
        db.session.delete(notecard_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the notecard'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    notecard_to_update = Notecard.query.get_or_404(id)
    if request.method == 'POST':
        notecard_to_update.title = request.form['title']
        notecard_to_update.content = request.form['content']
        notecard_to_update.tag = request.form['tag']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the notecard'
    else:
        return render_template('update.html',notecard_to_update = notecard_to_update)

if __name__ == "__main__":
    app.run(debug=True)