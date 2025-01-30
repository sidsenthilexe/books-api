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

@application.route('/book-add/<string:name>/<int:author_id>', methods=['POST'])
def add_book(name, author_id):
    new_book = {
        'id': len(books) + 1,
        'name': name,
        'author_id': author_id
    }
    books.append(new_book)
    return jsonify(new_book), 201

@application.route('/author-add/<string:author_name>', methods=['POST'])
def add_author(author_name):
    new_author = {
        'id': len(authors) + 1,
        'name': author_name
    }
    authors.append(new_author)
    return jsonify(new_author), 201

if __name__ == '__main__':
    application.run()