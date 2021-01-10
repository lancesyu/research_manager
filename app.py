from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///notecards.db'
app.config['SQLALCHEMY_BINDS'] = {
    'workscited': 'sqlite:///workscited.db'
}
db=SQLAlchemy(app)

class Notecard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.String(1000),nullable=False)
    tag = db.Column(db.String(20),nullable=False)
    source = db.Column(db.String(100),nullable=True)

class Source(db.Model):
    __bind_key__ = 'workscited'
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(50),nullable=False)
    author_first = db.Column(db.String(50),nullable=True)
    author_last = db.Column(db.String(50),nullable=True)
    title = db.Column(db.String(150),nullable=False)
    container = db.Column(db.String(150),nullable=True)
    other_contributors = db.Column(db.String(300),nullable=True)
    version = db.Column(db.String(10),nullable=True)
    number = db.Column(db.String(10),nullable=True)
    publisher = db.Column(db.String(100),nullable=True)
    date = db.Column(db.String(24),nullable=True)
    location = db.Column(db.String(100),nullable=True)

def __repr__(self):
    return '<Notecard %r>' %self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST' and "add_notecard" in request.form:
        notecard_title = request.form['title']
        notecard_content = request.form['content']
        notecard_tag = request.form['tag']
        notecard_source = request.form['source']
        new_notecard = Notecard(title=notecard_title,content=notecard_content,tag=notecard_tag,source=notecard_source)
        try:
            db.session.add(new_notecard)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the notecard'
    elif request.method == 'POST' and "add_source" in request.form:
        source_kind = request.form['kind']
        source_author_first = request.form['author_first']
        source_author_last = request.form['author_last']
        source_title = request.form['title']
        source_container = request.form['container']
        source_other_contributors = request.form['others']
        source_version = request.form['version']
        source_number = request.form['number']
        source_publisher = request.form['publisher']
        source_date = request.form['date']
        source_location = request.form['location']
        new_source = Source(kind=source_kind,author_first=source_author_first,author_last=source_author_last,title=source_title,container=source_container,other_contributors=source_other_contributors,version=source_version,number=source_number,publisher=source_publisher,date=source_date,location=source_location)
        try:
            db.session.add(new_source)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the source'
    else:
        notecards = Notecard.query.order_by(Notecard.tag).all()
        sources = Source.query.order_by(Source.author_last).all()
        return render_template('index.html', notecards=notecards, sources=sources)


@app.route('/delete/<int:id>')
def delete(id):
    notecard_to_delete = Notecard.query.get_or_404(id)
    try:
        db.session.delete(notecard_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the notecard'

@app.route('/delete_source/<int:id>')
def delete_source(id):
    source_to_delete = Source.query.get_or_404(id)
    try:
        db.session.delete(source_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the source'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    notecard = Notecard.query.get_or_404(id)
    if request.method == 'POST':
        notecard.title = request.form['title']
        notecard.content = request.form['content']
        notecard.tag = request.form['tag']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the notecard'
    else:
        return render_template('update.html',notecard_to_update = notecard)

@app.route('/update_source/<int:id>', methods=['GET', 'POST'])
def update_source(id):
    source = Source.query.get_or_404(id)
    if request.method == 'POST':
        source.author_first = request.form['author_first']
        source.author_last = request.form['author_last']
        source.title = request.form['title']
        source.container = request.form['container']
        source.other_contributors = request.form['others']
        source.version = request.form['version']
        source.number = request.form['number']
        source.publisher = request.form['publisher']
        source.date = request.form['date']
        source.location = request.form['location']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the source'
    else:
        return render_template('update_source.html',source_to_update = source)

if __name__ == "__main__":
    app.run(debug=True)