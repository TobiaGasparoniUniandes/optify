import flask
from flask import request, jsonify, redirect, url_for

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'},
    {'id': 3,
     'title': 'Other title',
     'author': 'Vernor Vingp',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'published': '1992'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books/<book_id>', methods=['GET'])
def api_id(book_id):
    book_id = int(book_id)
    
    chosen = None
    
    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == book_id:
            chosen = jsonify([book])
    
    return chosen

@app.route('/api/v1/resources/books', methods=['GET'])
def api_params():
    
    # array => request.args
    # value arg => request.args['id']
    
    # Si no hay argumentos
    if len(list(request.args.keys())) == 0:
        return redirect(url_for('api_all'))

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested params.
    for book in books:
        all_args = True
        for arg in request.args:
            if arg == 'id':
                return 'Error: The parameter "id" cannot be used to look for several books.'
            if arg not in book.keys():
                return 'Error: The parameter "{}" does not belong to books.'.format(arg)
            elif request.args[arg] != book[arg]:
                all_args = False
        if all_args:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()
