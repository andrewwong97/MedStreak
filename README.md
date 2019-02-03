# MedStreak

## Setup

Using Python 2.7

1. Make sure you have `virtualenv` installed
2. `virtualenv env`
3. In base directory: run `source env/bin/activate` to activate the virtual environment. You can later run `deactivate` to exit the venv.
4. Run `pip install -r requirements.txt` to install project requirements inside the venv.
5. Run `python api.py` inside `medstreak/` and `curl http://127.0.0.1:5000/api/user` to test response

## Stack

Flask-Restful to parse and return structured requests and responses using REST.
Pymongo as Mongo driver for any db requests
