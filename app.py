from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///notecards.db'
app.config['SQLALCHEMY_BINDS'] = {
    'workscited': 'sqlite:///workscited.db'
}
db=SQLAlchemy(app)
citation_style="MLA" # citation format is MLA by default

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
    # the two below are to make it more convenient when displaying the citation on the page
    citation_author = db.Column(db.String(100), nullable=True) # combine the author's first and last name
    # in between will be title and container
    citation_everything_else = db.Column(db.String(500), nullable=True) # combine everything else after title/container

def __repr__(self):
    return '<Notecard %r>' %self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST' and "add_notecard" in request.form: # make a new notecard from the user's entry
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
    elif request.method == 'POST' and "add_source" in request.form: # make a new source from the user's entry
        source_kind = request.form['kind']
        source_author_first = request.form['author_first']
        source_author_last = request.form['author_last']
        source_title = request.form['title']
        source_container = request.form['container']
        source_other_contributors = request.form['other_contributors']
        source_version = request.form['version']
        source_number = request.form['number']
        source_publisher = request.form['publisher']
        source_date = request.form['date']
        source_location = request.form['location']
        source_author = ""
        source_everything_else = ""
        # combine the author's names
        if len(source_author_last) > 0:
            source_author += source_author_last
            if len(source_author_first) > 0:
                source_author = source_author + ", " + source_author_first + "."
        else:
            if len(source_author_first) > 0:
                source_author = source_author + source_author_first + "."
        # combine all the elements of the citation that come after the container
        if len(source_other_contributors) > 0:
            source_everything_else = source_everything_else + ", " + source_other_contributors
        if len(source_version) > 0:
            source_everything_else = source_everything_else + ", " + source_version
        if len(source_number) > 0:
            source_everything_else = source_everything_else + ", " + source_number
        if len(source_publisher) > 0:
            source_everything_else = source_everything_else + ", " + source_publisher
        if len(source_date) > 0:
            source_everything_else = source_everything_else + ", " + source_date
        if len(source_location) > 0:
            source_everything_else = source_everything_else + ", " + source_location
        if len(source_everything_else) != 0:
            source_everything_else += "."
        

        new_source = Source(kind=source_kind,author_first=source_author_first,author_last=source_author_last,title=source_title,container=source_container,other_contributors=source_other_contributors,version=source_version,number=source_number,publisher=source_publisher,date=source_date,location=source_location,citation_author=source_author,citation_everything_else=source_everything_else)
        try:
            db.session.add(new_source)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the source'
    else:
        notecards = Notecard.query.order_by(Notecard.tag).all()
        sources = Source.query.order_by(Source.citation_author).all()
        return render_template('index.html', notecards=notecards, sources=sources)

@app.route('/compact')
def compact():
    notecards = Notecard.query.order_by(Notecard.tag).all()
    sources = Source.query.order_by(Source.citation_author).all()
    return render_template('compact.html',notecards=notecards, sources=sources)

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
        source.kind = request.form['kind']
        source.author_first = request.form['author_first']
        source.author_last = request.form['author_last']
        source.title = request.form['title']
        source.container = request.form['container']
        source.other_contributors = request.form['other_contributors']
        source.version = request.form['version']
        source.number = request.form['number']
        source.publisher = request.form['publisher']
        source.date = request.form['date']
        source.location = request.form['location']
        source.citation_author = ""
        source.citation_everything_else = ""
        # combine the author's names
        if len(source.author_last) > 0:
            source.citation_author += source.author_last
            if len(source.author_first) > 0:
                source.citation_author = source.citation_author + ", " + source.author_first + "."
        else:
            if len(source.author_first) > 0:
                source.citation_author = source.citation_author + source.author_first + "."
        # combine all the elements of the citation that come after the container
        if len(source.other_contributors) > 0:
            source.citation_everything_else = source.citation_everything_else + ", " + source.other_contributors
        if len(source.version) > 0:
            source.citation_everything_else = source.citation_everything_else + ", " + source.version
        if len(source.number) > 0:
            source.citation_everything_else = source.citation_everything_else + ", " + source.number
        if len(source.publisher) > 0:
            source.citation_everything_else = source.citation_everything_else + ", " + source.publisher
        if len(source.date) > 0:
            source.citation_everything_else = source.citation_everything_else + ", " + source.date
        if len(source.location) > 0:
            source.citation_everything_else = source.citation_everything_else + ", " + source.location
        if len(source.citation_everything_else) != 0:
            source.citation_everything_else += "."
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the source'
    else:
        return render_template('update_source.html',source_to_update = source)

if __name__ == "__main__":
    app.run(debug=True)