# books-api (github.com/sidsenthilexe/books-api)
# A simple API to maintain a list of books and a list of authors

# imports
from flask import Flask, jsonify, request, abort
import json

# init flask
application = Flask(__name__)
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# init the lists of books and authors
books = []
authors = []

# Add the sample data
authors.append({'id': 1, 'name': 'Tolkien'})
authors.append({'id': 2, 'name': 'Asimov'})
books.append({'id': 1, 'title': 'The Hobbit', 'author_id': 1})
books.append({'id': 2, 'title': 'I, Robot', 'author_id': 2})

def validate_book_add(data):
    if 'title' not in data or not isinstance(data['title'], str):
        abort(400, 'Title is required to be a string. github.com/sidsenthilexe/books-api/wiki')
    if 'author_id' not in data or not isinstance(data['author_id'], int):
        abort(400, 'Author ID is required to be an integer. github.com/sidsenthilexe/books-api/wiki')

def validate_book_modify(data):
    if 'title' not in data or not isinstance(data['title'], str):
        abort(400, 'Title is required to be a string. github.com/sidsenthilexe/books-api/wiki')
    if 'id' not in data or not isinstance(data['id'], int):
        abort(400, 'ID is required to be an integer. github.com/sidsenthilexe/books-api/wiki')
    if 'author_id' not in data or not isinstance(data['author_id'], int):
        abort(400, 'Author ID is required to be an integer. github.com/sidsenthilexe/books-api/wiki')

def validate_author_add(data):
    if 'name' not in data or not isinstance(data['name'], str):
        abort(400, 'Name is required to be a string. github.com/sidsenthilexe/books-api/wiki')

def validate_author_modify(data):
    if 'name' not in data or not isinstance(data['name'], str):
        abort(400, 'Name is required to be a string. github.com/sidsenthilexe/books-api/wiki')
    if 'id' not in data or not isinstance(data['id'], int):
        abort(400, 'ID is required to be an integer. github.com/sidsenthilexe/books-api/wiki')

@application.route('/')

# GET a list of all books
@application.route('/books', methods=['GET'])
def get_books_list():
    return jsonify(books)

# GET a specific book by its id
@application.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((book for book in books if book['id'] == id), None)
    if book is None:
        return jsonify({'error': 'Book not found. If you want to add a book, use /book-add.', 'documentation': 'github.com/sidsenthilexe/books-api/wiki'}), 404
    
    # find info about the author
    author = next((author for author in authors if author['id'] == book['author_id']), None)

    # compile the output with information about the book as well as the author
    book_with_author = {
        'id': book['id'],
        'title': book['title'],
        'author_id': book['author_id'],
        'author': author['name'] if author else 'Unknown'
    }
    return jsonify(book_with_author)
    

# POST a new book
@application.route('/book-add', methods=['POST'])
def add_book():
    try:
        new_book = request.json
        if isinstance(new_book, list):
            new_book = new_book[0]
        new_book['id'] = len(books) + 1
        validate_book_add(new_book)
        books.append(new_book)
        return jsonify(new_book), 201
    except Exception as exception:
        return jsonify({'error': str(exception)})

# PUT - modify an exisiting book by its id
@application.route('/book-modify/<int:id>', methods=['PUT'])
def update_book(id):
    book = next((book for book in books if book['id'] == id), None)
    if book is None:
        return jsonify({'error': 'Book not found. If you want to add a book, use /book-add.', 'documentation': 'github.com/sidsenthilexe/books-api/wiki'}), 404
    book_update = request.json
    validate_book_modify(book_update)
    book.update(book_update)
    return jsonify(book)
    

# DELETE an existing book by its id
@application.route('/book-delete/<int:id>', methods=['DELETE'])
def delete_book(id):
    global books
    books = [book for book in books if book['id'] != id]
    return jsonify({'message': f'Deleted book {id}'}), 201

# GET a list of all authors
@application.route('/authors', methods=['GET'])
def get_authors_list():
    return jsonify(authors)

# GET a specific author by their id
@application.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
    author = next((author for author in authors if author['id'] == id), None)
    if author is None:
        return jsonify({'error': 'Author not found. If you want to add an author, use /author-add.', 'documentation': 'github.com/sidsenthilexe/books-api/wiki'}), 404
    
    # find the number of books from this author
    book_count = sum(1 for book in books if book['author_id'] == id)
    
    # compile the output with information about the author + book count
    author_with_book_count = {
        'id': author['id'],
        'name': author['name'],
        'book_count': book_count
    }
    return jsonify(author_with_book_count)

# POST a new author
@application.route('/author-add', methods=['POST'])
def add_author():
    try:
        new_author = request.json
        if isinstance(new_author, list):
            new_author = new_author[0]
        new_author['id'] = len(authors)+1
        validate_author_add(new_author)
        authors.append(new_author)
        return jsonify(new_author), 201
    except Exception as exception:
        return jsonify({'error': str(exception)})

# PUT - modify an existing author by their id
@application.route('/author-modify/<int:id>', methods=['PUT'])
def update_author(id):
    author = next((author for author in authors if author['id'] == id), None)
    if author is None:
        return jsonify({'error': 'Author not found. If you want to add an author, use /author-add.', 'documentation': 'github.com/sidsenthilexe/books-api/wiki'}), 404
    author_update = request.json
    author.update(author_update)
    return jsonify(author)

# DELETE an existing author by their id
@application.route('/author-delete/<int:id>', methods=['DELETE'])
def delete_author(id):
    global authors
    authors = [author for author in authors if author['id'] != id]
    return jsonify({'message': f'Deleted author {id}'}), 201

if __name__ == '__main__':
    application.run(debug=True, host='localhost', port=39617)
    