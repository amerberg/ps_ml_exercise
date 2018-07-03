# Setup
To set up the database, install the dependencies using `pip` and then cd to the `app` directory and run

```
export USER_SIMILARITY_DB_URL=[db_url]
python setup.py path_to_data
```
Here `[db_url]` can be replaced with any valid SQLALchemy
[database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) and
`path_to_data` is a path to a local folder containing the data file.
An easy approach is to use SQLite for storage, e.g. sqlite:////path/to/database.sqlite.
(I have only been successful in using absolute paths in the database URL.)

This loads the raw data, computes the similarity score matrix, and stores the most similar users for each user.
On my 4+-year old computer, this takes about 90 seconds.

# Using the API
The API can be deployed on port 5000 using the Flask built-in web server by running
```
export USER_SIMILARITY_DB_URL=[db_url]
python run.py
```
Then, for instance, one can request http://127.0.0.1:5000/user/1. Like any Flask app, the API can also be deployed on a production server, e.g. gunicorn.

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

# About
The similarity score used here is the cosine similarity of a vector space representation of the users.
The users are represented by merging 3 kinds of data:

   + boolean indicators of interest (or lack thereof) in a subject
   + normalized assessment scores (missing scores are replaced with the average value average)
   + normalized time spent viewing courses on each topic (I have not incorporated course difficulty at all)
   
In principle, it would be worthwhile to think about how these three kinds of data should be weighted against each other, 
but I have not had time to do so.

I chose the cosine similarity measure largely because it's easy to calculate. We can compute the cosine similarity for all of our users
just by doing basic matrix operations, which are implemented in existing libraries in highly optimized forms.
Moreover, existing sparse implementations of these matrix operations would make it relatively easy to scale to a larger dataset.

This approach does have some limitations. 
Notably, imputing the average value when a user hasn't taken a particular assessment is clearly suspect.
Moreover, the vector space representation assumes that all of the various features are orthogonal, which probably isn't warranted.
Sometimes different interests are closely related, and users who have taken courses should do better on assessments related to those courses.

At larger scale, we would probably want to represent our matrices as sparse matrices. 
We might also choose to discard some features that have very few nonzero values to reduce the amount of computation needed.
In practice, this would be accomplished by dropping the uncommon interests/assessments/tags before pivoting the respective tables.

I would expect an API like this might be used for making recommendations to users. 
For instance, we might recommend courses that similar users had taken, or interests that similar users were interested in.
It would potentially be useful to incorporate temporal information into our similarity score, so that we could account for the order in
which courses, assessment scores, and interests arose.
This information is already available, but I haven't had time to consider it yet.

Here are a few other kinds of data that might be useful:

   + A course dependency graph (which courses are pre-requisites for other courses?)
   + A mapping between interests, assessments, and video tags (obviously, these are all related, but we've been assuming they're entirely different)
   + career information (current position, aspirations, employer, etc.)






  