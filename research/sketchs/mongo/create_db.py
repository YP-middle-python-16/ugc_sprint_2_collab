from pymongo import MongoClient
import pymongo


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://root:example@localhost/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Connect to our database
    db = client['SeriesDB']

    # Fetch our series collection
    series_collection = db['series']

    return series_collection


def insert_document(collection, data):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    return collection.insert_one(data).inserted_id



def find_document(collection, elements, multiple=False):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    new_show = {
        "name": "FRIENDS",
        "year": 1994
    }

    ret = insert_document(dbname, new_show)
    print(ret)

    ret = find_document(dbname, {'name': 'FRIENDS'})
    print(ret)

    ret = find_document(dbname, {'name': 'FRIENDS'}, True)
    print(ret)

