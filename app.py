"""
Run app with: python app.py
"""
import json
import random
import logging
from flask import Flask, jsonify, request
from functools import lru_cache

"""
Initializing flask app
"""
app = Flask(__name__)


"""
Creates a logger to track history of the app usage.
Logs to app.log
"""
def setup_logging(log_file='app.log'):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


logger = setup_logging()


"""
Loads facts in from facts.json in read mode
"""
def load_facts():
    logger.info("Facts loaded successfully.")
    with open('facts.json', 'r') as f:
        return json.load(f)


"""
Opens facts.json in write mode
"""
def save_facts(new_facts):
    logger.info("Facts saved successfully.")
    with open('facts.json', 'w') as f:
        json.dump(new_facts, f)


facts = load_facts()


"""
API Routes
"""


# http://127.0.0.1:5000/fact
@app.route('/fact', methods=['GET'])
@lru_cache(maxsize=128)
def get_random_fact():
    logger.info("Retrieving random fact.")
    random_fact = random.choice(facts)
    return jsonify({'fact': random_fact})


# http://127.0.0.1:5000/facts
@app.route('/facts', methods=['GET'])
@lru_cache(maxsize=128)
def get_all_facts():
    logger.info("Retrieving all facts.")
    return jsonify({'facts': facts})


# http://127.0.0.1:5000/add_facts
@app.route('/add_facts', methods=['POST'])
def add_fact():
    logger.info("Adding new fact.")
    new_fact = request.json['fact']
    facts.append(new_fact)
    save_facts(facts)
    return jsonify({'message': 'Added new fact!'}), 201


if __name__ == '__main__':
    app.run(debug=True)
