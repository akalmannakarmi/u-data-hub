import os
import logging

os.makedirs('logs/',exist_ok=True)
os.makedirs('instance/',exist_ok=True)

db_logger = logging.getLogger('database')
db_handler = logging.FileHandler('logs/database.log')
db_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
db_logger.addHandler(db_handler)
db_logger.setLevel(logging.INFO)