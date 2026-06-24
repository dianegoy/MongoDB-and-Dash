# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'ashleymaple' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None: 
            result = self.database.animals.insert_one(data)  # data should be dictionary   
            return result.acknowledged
        else: 
            return False
            

    # Create method to implement the R in CRUD.
    def read(self, query):
        if query is not None:
            return list(self.database.animals.find(query))
        else: 
            return []
        
    # Create an update method to implement the U in CRUD
    def update(self, query, update_data):
        if query is not None:
            result = self.database.animals.update_many(query, update_data)
            return result.modified_count
        else: 
            return False
        
    # Create a delete method to implement the D in CRUD
    def delete(self, query):
        if query is not None:
            result = self.database.animals.delete_many(query)
            return result.deleted_count
        else:
            return False
    