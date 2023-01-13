import os

db_config = {
    'user': 'graph-node',
    'password': os.environ['DB_PASSWORD'],
    'host': 'localhost',
    'port': '5432',
    'options': '-c search_path=sgd10'
}
