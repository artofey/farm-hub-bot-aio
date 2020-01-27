import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# DB_CONNECT = 'postgresql://postgres:1@localhost/farm_bot'
DB_CONNECT = os.environ.get('DATABASE_URL')

engine = create_engine(DB_CONNECT, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
