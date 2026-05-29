from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite Db
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://flaskuser:flaskpass@db:5432/flaskdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    notes = Note.query.all()
    return render_template("index.html", notes=notes)

# CREATE
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        note = Note(title=title, body=body)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

# 編集 UPDATE
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    note = Note.query.get_or_404(id)

    if request.method == "POST":
        note.title = request.form["title"]
        note.body = request.form["body"]

        db.session.commit()

        return redirect(url_for("index"))

    return render_template("edit.html", note=note)

# 削除 DELETE
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    note = Note.query.get_or_404(id)

    db.session.delete(note)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

