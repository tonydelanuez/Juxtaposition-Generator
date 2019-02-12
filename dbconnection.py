from pymongo import MongoClient

def get_db():
    MONGO_HOST = os.getenv('MONGO_HOST')
    MONGO_PORT = os.getenv('MONGO_PORT')
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASS = os.getenv('MONGO_PASS')
    connection = MongoClient(MONGO_HOST, MONGO_PORT)
    db = connection['juxtaposition']
    db.authenticate(MONGO_USER, MONGO_PASS)
    return db.comments
