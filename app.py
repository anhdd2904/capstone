import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Book, Author

from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # GET /books
    @app.route('/books', methods=['GET'])
    @requires_auth('view:books')
    def retrieve_books(payload):
        books = Book.query.all()
        books = list(map(lambda book: book.format(), books))
        return jsonify({
            "success": True,
            "books": books
        })

    # GET /authors
    @app.route('/authors', methods=['GET'])
    @requires_auth('view:authors')
    def retrieve_authors(payload):
        authors = Author.query.all()
        authors = list(map(lambda author: author.format(), authors))
        return jsonify({
            "success": True,
            "authors": authors
        })

    # POST /books
    @app.route('/books', methods=['POST'])
    @requires_auth('post:books')
    def create_book(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        title = body.get('title', None)
        publish_date = body.get('publish_date', None)

        if title is None or publish_date is None:
            abort(400, "Missing field for Book")

        book = Book(title=title, publish_date=publish_date)
        book.insert()

        return jsonify({
            "success": True
        })

    # POST /authors
    @app.route('/authors', methods=['POST'])
    @requires_auth('post:authors')
    def create_author(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        book_id = body.get('book_id', None)

        if name is None or age is None or gender is None or book_id is None:
            abort(400, "Missing field for Author")

        author = Author(name=name, age=age, gender=gender, book_id=book_id)
        author.insert()

        return jsonify({
            "success": True
        })

    # DELETE /books/<int:book_id>
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    @requires_auth('delete:books')
    def delete_book(payload, book_id):
        book = Book.query.filter(Book.id == book_id).one_or_none()

        if book is None:
            abort(404, "No book with given id " + str(book_id) + " is found")

        book.delete()

        return jsonify({
            'success': True,
            'deleted': book_id
        })

    # DELETE /authors/<int:author_id>
    @app.route('/authors/<int:author_id>', methods=['DELETE'])
    @requires_auth('delete:authors')
    def delete_author(payload, author_id):
        author = Author.query.filter(Author.id == author_id).one_or_none()

        if author is None:
            abort(404, "No author with given id " + str(author_id) + " is found")

        author.delete()

        return jsonify({
            'success': True,
            'deleted': author_id
        })

    # PATCH /books/<book_id>
    @app.route('/books/<int:book_id>', methods=['PATCH'])
    @requires_auth('update:books')
    def update_book(payload, book_id):
        updated_book = Book.query.get(book_id)

        if not updated_book:
            abort(404, 'Book with id: ' + str(book_id) + ' could not be found.')

        body = request.get_json()

        title = body.get('title', None)
        publish_date = body.get('publish_date', None)

        if title:
            updated_book.title = title
        if publish_date:
            updated_book.publish_date = publish_date

        updated_book.update()

        return jsonify({
            "success": True,
            "updated": updated_book.format()
        })

    # PATCH /authors/<author_id>
    @app.route('/authors/<int:author_id>', methods=['PATCH'])
    @requires_auth('update:authors')
    def update_author(payload, author_id):
        updated_author = Author.query.get(author_id)

        if not updated_author:
            abort(404, 'Author with id: ' + str(author_id) + ' could not be found.')

        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        book_id = body.get('book_id', None)

        if name:
            updated_author.name = name
        if age:
            updated_author.age = age
        if gender:
            updated_author.gender = gender
        if book_id:
            updated_author.book_id = book_id

        try:
            updated_author.update()
        except BaseException:
            abort(400, "Bad formatted request due to nonexistent book id" + str(book_id))

        return jsonify({
            "success": True,
            "updated": updated_author.format()
        })

    def get_error_message(error, default_message):
        try:
            return error.description
        except BaseException:
            return default_message

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": get_error_message(error, "unprocessable"),
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": get_error_message(error, "resource not found")
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": get_error_message(error, "bad request")
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error['description']
        }), auth_error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
