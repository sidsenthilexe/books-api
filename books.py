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
    print(jsonify(books))

@application.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = ((book for book in books if book['id'] == id), None)
    if book is None:
        return jsonify({'error': 'Book not found. If you want to add a book, use /book-add'}), 404
    return jsonify(book)

    
@application.route('/authors', methods=['GET'])
def get_authors():
    return jsonify(authors)

@application.route('/book-add', methods=['POST'])
def add_book():
    new_book = request.json
    new_book['id'] = len(books) + 1
    books.append(new_book)
    return jsonify(new_book), 201

if __name__ == '__main__':
    application.run()