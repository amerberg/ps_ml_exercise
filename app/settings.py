from eve_sqlalchemy.config import DomainConfig, ResourceConfig
import os
from schema import User


SQLALCHEMY_DATABASE_URI = os.environ['USER_SIMILARITY_DB_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
DOMAIN = DomainConfig({
    'user': ResourceConfig(User)
}).render()