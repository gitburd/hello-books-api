from app import db
from app.models.book import Book
from flask import request, Blueprint, make_response, jsonify
books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("/", methods=["GET", "POST"])
def handle_books():

    if request.method == "GET":
        title_query = request.args.get("title")
        if title_query:
            books = Book.query.filter(Book.title.ilike(f'%{title_query}%'))
        else:
            books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return make_response(jsonify(books_response), 200)

    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title=request_body["title"],
                        description=request_body["description"])

        try:
            db.session.add(new_book)
            db.session.commit()
            book_response = {"book": {
                "id": new_book.id,
                "title": new_book.title,
                "description": new_book.description
            }}
            return make_response(book_response, 201)
        except Exception as e:
            print(e)
            return make_response(f"Book was not created. Title and description are required.", 400)


@ books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return make_response(f"Book #{book_id} Not Found", 404)

    if request.method == "GET":
        book_response = {"book": {
            "id": book.id,
            "title": book.title,
            "description": book.description
        }}
        return make_response(book_response, 200)

    elif request.method == "PUT":
        form_data = request.get_json()

        book.title = form_data["title"]
        book.description = form_data["description"]
        db.session.commit()
        book_response = {"book": {
            "id": book.id,
            "title": book.title,
            "description": book.description
        }}
        return make_response(book_response, 200)
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book # {book.id} successfully deleted", 200)
