# MedStreak

## Setup

Using Python 2.7

1. Make sure you have `virtualenv` installed
2. In base directory: run `source env/bin/activate` to activate the virtual environment. You can later run `deactivate` to exit the venv.
3. Run `pip install -r requirements.txt` to install project requirements inside the venv.
4. Run `python api.py` inside `medstreak/` and `curl http://127.0.0.1:5000/users` to test response

## Stack

Flask-Restful to parse and return structured requests and responses using REST.
Flask-Mongoengine to act as an ORM between MongoDB and Flask controllers. 

## MongoDB Connection Settings

```python
app.config['MONGODB_SETTINGS'] = {
    'db': 'MedStreak-Dev',
    'host': 'mongodb://medstreak:medstreak@medstreak-dev-shard-00-00-8ghe7.mongodb.net:27017,medstreak-dev-shard-00-01-8ghe7.mongodb.net:27017,medstreak-dev-shard-00-02-8ghe7.mongodb.net:27017/test?ssl=true&replicaSet=MedStreak-Dev-shard-0&authSource=admin&retryWrites=true'
}
```
