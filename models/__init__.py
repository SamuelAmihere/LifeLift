#!/usr/bin/python3
"""create a unique FileStorage instance for your application"""
import os
from models.engine.db_storage import DBStorage
from dotenv import load_dotenv

load_dotenv()

storage_type = os.getenv('LIFELIFT_TYPE_STORAGE')

if storage_type == 'db':
    storage = DBStorage()
    storage.reload()
else:
    raise Exception("Invalid storage type")

# Path: web_flask/models/engine/db_storage.py
# Compare this snippet from web_flask/models/engine/db_storage.py: