from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)