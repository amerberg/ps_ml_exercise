from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from schema import Base
import json


def parse_field(resource, response):
    """Parse the JSON field, and convert keys to strings in case the user wants XML output."""
    response['most_similar'] = {"most_similar_{}".format(k): v for k, v in json.loads(response['most_similar']).items()}


app = Eve(validator=ValidatorSQL, data=SQL)
Base.metadata.bind = app.data.driver.engine
app.data.driver.Model = Base
app.on_fetched_item += parse_field

if __name__ == '__main__':
    app.run(debug=True)
