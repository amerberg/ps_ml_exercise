from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from schema import Base
import json

def parse_field(resource, response):
    response['most_similar'] = {"similar_user_{}".format(k): v for k, v in json.loads(response['most_similar']).items()}


if __name__ == '__main__':
    app = Eve(validator=ValidatorSQL, data=SQL)
    Base.metadata.bind = app.data.driver.engine
    app.data.driver.Model = Base
    app.on_fetched_item += parse_field
    app.run(debug=True)
