from flask import Flask, jsonify, request

application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

books = []
authors = []

authors.append({'id': 1, 'name': 'Tolkien'})
authors.append({'id': 2, 'name': 'Asimov'})
books.append({'id': 1, 'title': 'The Hobbit', 'author_id': 1})
books.append({'id': 2, 'title': 'I, Robot', 'author_id': 2})

@application.route('/')

@application.route('/books', methods=['GET'])
def get_books_list():
    return jsonify(books)

@application.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((book for book in books if book['id'] == id), None)
    if book is None:
        return jsonify({'error': 'Book not found. If you want to add a book, use /book-add'}), 404
    return jsonify(book)

@application.route('/authors', methods=['GET'])
def get_authors():
    return jsonify(authors)

@application.route('/book-add', methods=['POST'])
def add_book():
    try:
        new_book = request.json
        if isinstance(new_book, list):
            new_book = new_book[0]
        new_book['id'] = len(books) + 1
        books.append(new_book)
        return jsonify(new_book), 201
    except Exception as exception:
        return jsonify({'error': str(exception)})

@application.route('/author-add', methods=['POST'])
def add_author():
    try:
        new_author = request.json
        if isinstance(new_author, list):
            new_author = new_author[0]
        new_author['id'] = len(authors)+1
        authors.append(new_author)
        return jsonify(new_author), 201
    except Exception as exception:
        return jsonify({'error': str(exception)})


if __name__ == '__main__':
    application.run()