from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from pymongo import MongoClient


app = FlaskAPI(__name__)

@app.route("/", methods=['GET'])

def pipeline1():
    mongo_uri = "mongodb://mongos:27017"

    client = MongoClient(mongo_uri)
    db = client.prac2
    collection = db.books
 
    # Obtiene los libros del autor con _id = A20, y regresa los registros ordenados descendientemente por el numero de paginas de los libros
    pipeline = [{"$match":{"author" : "A20"}},{"$sort":{"pages":+1}},{"$limit":500}]

    cursor = collection.aggregate(pipeline)

    books = []

    for book in cursor:
        # Se adicionó para poder manejar ObjectID
        book['_id'] = str(book['_id'])
        books.append(book)

    return books


def pipeline2():
    mongo_uri = "mongodb://mongos:27017"

    client = MongoClient(mongo_uri)
    db = client.prac2
    collection = db.books

    # Obtiene los autores en orden alfabetico y las fechas de nacimiento, con un limite a 300 registros
    pipeline = [{"$sort":{"name":-1}}, {"$limit": 300}, {"$project":{"_id":0,"$name":1,"$awards":1,"$date_birth":1}}]

    cursor = collection.aggregate(pipeline)

    authors = []

    for author in cursor:
        # Se adicionó para poder manejar ObjectID
        author['_id'] = str(author['_id'])
        authors.append(book)

    return authors

def pipeline3():
    mongo_uri = "mongodb://mongos:27017"

    client = MongoClient(mongo_uri)
    db = client.prac2
    collection = db.books

    # Obtiene los libros publicados especificamente por el publisher con id = P1356, ordenando las paginas ascendientemente 
    pipeline = [{
		"$match":{"publisher" : "P1356"}}, {
		"$sort":{"pages":-1}}, {
		"$limit":300}
	]

    cursor = collection.aggregate(pipeline)

    books = []

    for book in cursor:
        # Se adicionó para poder manejar ObjectID
        book['_id'] = str(book['_id'])
        books.append(book)

    return books


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
