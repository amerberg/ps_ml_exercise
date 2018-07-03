from sqlalchemy import create_engine
from argparse import ArgumentParser
import os

from schema import Base
from similarity import SimilarityCalculator


if __name__ == "__main__":
    db_url = os.environ['USER_SIMILARITY_DB_URL']
    parser = ArgumentParser(description='install the database schema and populate data')
    parser.add_argument('data_dir', help='the directory in which the data is located')
    args = parser.parse_args()
    
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    
    sc = SimilarityCalculator(args.data_dir)
    summaries = sc.all_summaries
    summaries.to_sql('users', engine, index=False, if_exists='append')
