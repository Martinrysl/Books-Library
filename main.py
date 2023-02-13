from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/martin/PycharmProjects/Starting+Files+-+library-start/new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


all_books = []


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    review = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Title %r>' % self.title


app.app_context().push()
#db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    bookies = Book.query.all()
    return render_template('index.html', bookies=bookies)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']
        info = {'name': title, 'author': author, 'rating': rating}
        all_books.append(info)
        new_book = Book(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        print(all_books)
        return redirect(url_for('home'))

    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.review = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit.html", data=book_selected)


@app.route("/delete/<int:id>")
def delete(id):
    data = Book.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
