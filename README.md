# Setup
To set up the database, run

```
USER_SIMILARITY_DB_URL=[db_url]
python setup.py path_to_data
```
Here `[db_url]` can be replaced with any valid SQLALchemy
[database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) (an easy approach is to use SQLite, e.g. sqlite:///example.sqlite) and
`path_to_data` is a path to a local folder containing the data file.

# Using the API
The API can be deployed on port 5000 using the Flask built-in web server by running
```
USER_SIMILARITY_DB_URL=[db_url]
python app.py
```
Then, for instance, one can request http://127.0.0.1:5000/user/1.

# Requirements
This repository has been tested using python 3.6 with the following packages:

   + eve 0.6.4
   + sqlalchemy
   + eve-sqlalchemy 0.5.0
   + pandas 0.19.2
   + numpy 1.11.3
   + scikit-learn 0.18.1

# Testing
A very limited number of tests are included. They can be executed by running `pytest` from the repository root.